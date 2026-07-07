from typing import Optional

from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from tools.cpu import cpu_usage
from tools.memory import memory_usage
from tools.disk import disk_usage
from tools.uptime import uptime
from tools.http import endpoint_health
from tools.health import system_health

from tools.process import (
    top_cpu_processes,
    top_memory_processes,
    search_process
)
from tools.docker import (
    list_containers,
    container_status,
    container_logs,
    restart,
    stop,
    start,
    container_stats,
    create_container
)
from tools.network import (
    network_usage,
    network_interfaces,
    port_status,
    hostname_lookup,
    remote_port_status
)
from tools.logs import (
    read_application_logs,
    search_application_logs,
    count_logs,
    tail_application_logs
)

mcp = FastMCP("DevOps Observability Server")


@mcp.tool
def get_cpu_usage():
    """Get CPU usage."""
    return cpu_usage()


@mcp.tool
def get_memory_usage():
    """Get memory usage."""
    return memory_usage()


@mcp.tool
def get_top_cpu_processes():
    """Returns top CPU consuming processes."""
    return top_cpu_processes()


@mcp.tool
def get_disk_usage():
    """Get disk usage."""
    return disk_usage()


@mcp.tool
def get_uptime():
    """Get system uptime."""
    return uptime()


@mcp.tool
def get_top_memory_processes():
    """Returns the top memory consuming processes."""
    return top_memory_processes()


@mcp.tool
def find_process(name: str):
    """Search for a running process by name."""
    return search_process(name)


@mcp.tool
def get_network_usage():
    """Returns network usage statistics."""
    return network_usage()


@mcp.tool
def get_network_interfaces():
    """Returns all network interfaces."""
    return network_interfaces()


@mcp.tool
def check_local_port(port: int):
    """Check whether a local TCP port is open."""
    return port_status(port)


@mcp.tool
def resolve_host(hostname: str):
    """Resolve a hostname to an IP address."""
    return hostname_lookup(hostname)


@mcp.tool
def check_remote_port(host: str, port: int):
    """Check whether a TCP port is open on another machine."""
    return remote_port_status(host, port)


@mcp.tool
def read_logs():
    """Read the application log."""
    return read_application_logs()


@mcp.tool
def search_logs(keyword: str):
    """Search logs."""
    return search_application_logs(keyword)


@mcp.tool
def count_log_entries(level: str):
    """Count INFO/WARN/ERROR."""
    return count_logs(level)


@mcp.tool
def tail_logs(lines: int = 10):
    """Show last N log lines."""
    return tail_application_logs(lines)


@mcp.tool
def get_system_health():
    """Returns an overall health report."""
    return system_health()


@mcp.tool
def check_http_endpoint(url: str):
    """Check whether an HTTP endpoint is reachable."""
    return endpoint_health(url)


@mcp.tool
def get_docker_containers():
    """List all Docker containers."""
    return list_containers()


@mcp.tool
def get_container_status(container_name: str):
    """Get detailed information about a Docker container."""
    return container_status(container_name)


@mcp.tool
def get_container_logs(container_name: str, lines: int = 50):
    """Get the last N log lines from a Docker container."""
    return container_logs(container_name, lines)


@mcp.tool
def restart_container(container_name: str):
    """Restart a Docker container."""
    return restart(container_name)


@mcp.tool
def stop_container(container_name: str):
    """Stop a Docker container."""
    return stop(container_name)


@mcp.tool
def start_container(container_name: str):
    """Start a Docker container."""
    return start(container_name)


@mcp.tool
def get_container_stats(container_name: str):
    """Get CPU, memory, and network statistics for a Docker container."""
    return container_stats(container_name)


@mcp.tool
def start_or_create_container(
    image: str,
    container_name: str,
    ports: Optional[dict] = None,
    volumes: Optional[dict] = None,
    environment: Optional[dict] = None,
    command: Optional[str] = None,
    network: Optional[str] = None,
    restart_policy: Optional[str] = None,
    detach: bool = True
):
    """
    Start a container if it already exists; otherwise pull the image
    and create + start it.

    Args:
        image: Docker image name, e.g. "nginx:latest"
        container_name: Name of the container to find or create
        ports: e.g. {"80/tcp": 8080}
        volumes: e.g. {"/host/path": {"bind": "/container/path", "mode": "rw"}}
        environment: e.g. {"ENV": "production"}
        command: Optional override command
        network: Docker network to attach to
        restart_policy: "always" | "unless-stopped" | "on-failure" | "no"
        detach: Run in background (default True)
    """
    return create_container(
        image=image,
        container_name=container_name,
        ports=ports,
        volumes=volumes,
        environment=environment,
        command=command,
        network=network,
        restart_policy=restart_policy,
        detach=detach
    )


app = mcp.http_app(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # fine for local dev; restrict in production
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=["mcp-protocol-version", "mcp-session-id", "Authorization", "Content-Type"],
            expose_headers=["mcp-session-id"],
        )
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)