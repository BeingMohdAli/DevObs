"""
Docker service layer.

This module talks directly to the Docker daemon via the docker SDK and
returns plain dicts/strings. It has no knowledge of MCP — that glue lives
in tools/docker.py.
"""

import docker

client = docker.from_env()


def get_all_containers():
    """Returns all Docker containers (running and stopped)."""
    containers = client.containers.list(all=True)

    result = []
    for c in containers:
        result.append({
            "id": c.short_id,
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "Unknown"
        })

    return result


def get_container_status(container_name):
    """Returns detailed information about a single container."""
    try:
        container = client.containers.get(container_name)

        return {
            "id": container.short_id,
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else "Unknown",
            "started_at": container.attrs["State"]["StartedAt"],
            "ports": container.attrs["NetworkSettings"]["Ports"]
        }

    except docker.errors.NotFound:
        return {"error": f"Container '{container_name}' not found."}


def get_container_logs(container_name, lines=50):
    """Returns the last N log lines from a container."""
    try:
        container = client.containers.get(container_name)
        return container.logs(tail=lines).decode("utf-8")

    except docker.errors.NotFound:
        return {"error": f"Container '{container_name}' not found."}


def restart_container(container_name):
    """Restarts a Docker container."""
    try:
        container = client.containers.get(container_name)
        container.restart()
        return {
            "status": "success",
            "message": f"Container '{container_name}' restarted successfully."
        }

    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"Container '{container_name}' not found."
        }


def stop_container(container_name):
    """Stops a running Docker container."""
    try:
        container = client.containers.get(container_name)
        container.stop()
        return {
            "status": "success",
            "message": f"Container '{container_name}' stopped successfully."
        }

    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"Container '{container_name}' not found."
        }


def start_container(container_name):
    """Starts an existing, stopped Docker container."""
    try:
        container = client.containers.get(container_name)
        container.start()
        return {
            "status": "success",
            "message": f"Container '{container_name}' started successfully."
        }

    except docker.errors.NotFound:
        return {
            "status": "error",
            "message": f"Container '{container_name}' not found."
        }


def get_container_stats(container_name):
    """Returns live CPU, memory, and network statistics for a container."""
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)

        memory_usage = stats["memory_stats"].get("usage", 0)
        memory_limit = stats["memory_stats"].get("limit", 0)

        cpu_total = stats["cpu_stats"]["cpu_usage"]["total_usage"]
        precpu_total = stats["precpu_stats"]["cpu_usage"]["total_usage"]

        system_cpu = stats["cpu_stats"].get("system_cpu_usage", 0)
        presystem_cpu = stats["precpu_stats"].get("system_cpu_usage", 0)

        cpu_percent = 0.0
        cpu_delta = cpu_total - precpu_total
        system_delta = system_cpu - presystem_cpu

        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (
                cpu_delta / system_delta
            ) * len(
                stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [])
            ) * 100.0

        networks = stats.get("networks", {})
        rx = sum(net.get("rx_bytes", 0) for net in networks.values())
        tx = sum(net.get("tx_bytes", 0) for net in networks.values())

        return {
            "container": container.name,
            "cpu_percent": round(cpu_percent, 2),
            "memory_usage_mb": round(memory_usage / (1024 * 1024), 2),
            "memory_limit_mb": round(memory_limit / (1024 * 1024), 2),
            "network_rx_mb": round(rx / (1024 * 1024), 2),
            "network_tx_mb": round(tx / (1024 * 1024), 2)
        }

    except docker.errors.NotFound:
        return {"error": f"Container '{container_name}' not found."}


def create_or_start_container(
    image,
    container_name,
    ports=None,
    volumes=None,
    environment=None,
    command=None,
    network=None,
    restart_policy=None,
    detach=True
):
    """
    If a container named `container_name` already exists:
        - starts it if it's stopped
        - reports it as already running if it's running
    If it doesn't exist:
        - pulls `image`
        - creates a new container with the given arguments
        - starts it

    ports format:       {"80/tcp": 8080}
    volumes format:     {"/host/path": {"bind": "/container/path", "mode": "rw"}}
    environment format: {"ENV_VAR": "value"}
    restart_policy:     "always" | "unless-stopped" | "on-failure" | "no"
    """
    # 1. Does the container already exist?
    try:
        container = client.containers.get(container_name)

        if container.status == "running":
            return {
                "status": "success",
                "action": "already_running",
                "message": f"Container '{container_name}' is already running."
            }

        container.start()
        return {
            "status": "success",
            "action": "started_existing",
            "message": f"Existing container '{container_name}' started successfully."
        }

    except docker.errors.NotFound:
        pass  # doesn't exist yet, fall through to pull + create
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Docker API error while checking container: {str(e)}"
        }

    # 2. Pull the image
    try:
        client.images.pull(image)
    except docker.errors.ImageNotFound:
        return {"status": "error", "message": f"Image '{image}' not found."}
    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to pull image '{image}': {str(e)}"
        }

    # 3. Create and start the new container
    try:
        run_kwargs = {
            "image": image,
            "name": container_name,
            "detach": detach,
        }
        if ports:
            run_kwargs["ports"] = ports
        if volumes:
            run_kwargs["volumes"] = volumes
        if environment:
            run_kwargs["environment"] = environment
        if command:
            run_kwargs["command"] = command
        if network:
            run_kwargs["network"] = network
        if restart_policy:
            run_kwargs["restart_policy"] = {"Name": restart_policy}

        new_container = client.containers.run(**run_kwargs)

        return {
            "status": "success",
            "action": "created_new",
            "message": f"Image '{image}' pulled and container '{container_name}' created & started.",
            "container_id": new_container.short_id
        }

    except docker.errors.APIError as e:
        return {
            "status": "error",
            "message": f"Failed to create container '{container_name}': {str(e)}"
        }