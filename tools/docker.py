"""
MCP-facing Docker tool functions.

Thin wrappers around services/docker_service.py. main.py imports these
short, tool-shaped names; the real Docker SDK logic lives in the service
layer so it stays testable and independent of MCP.
"""

from services.docker_service import (
    get_all_containers,
    get_container_status,
    get_container_logs,
    restart_container,
    stop_container,
    start_container,
    get_container_stats,
    create_or_start_container
)


def list_containers():
    return get_all_containers()


def container_status(container_name):
    return get_container_status(container_name)


def container_logs(container_name, lines=50):
    return get_container_logs(container_name, lines)


def restart(container_name):
    return restart_container(container_name)


def stop(container_name):
    return stop_container(container_name)


def start(container_name):
    return start_container(container_name)


def container_stats(container_name):
    return get_container_stats(container_name)


def create_container(
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
    Starts the container if it already exists, otherwise pulls the image
    and creates + starts a new one with the given arguments.
    """
    return create_or_start_container(
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