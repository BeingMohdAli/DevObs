from services.network_service import (
    get_network_usage,
    list_network_interfaces,
    check_port,
    resolve_hostname,
    check_remote_port

)


def network_usage():
    return get_network_usage()


def remote_port_status(host: str, port: int):
    return check_remote_port(host, port)


def network_interfaces():
    return list_network_interfaces()


def port_status(port: int):
    return check_port(port)


def hostname_lookup(hostname: str):
    return resolve_hostname(hostname)