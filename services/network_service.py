import psutil
import socket

import socket
def get_network_usage():
    """
    Returns bytes sent and received since boot.
    """

    net = psutil.net_io_counters()

    return {
        "bytes_sent": net.bytes_sent,
        "bytes_received": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_received": net.packets_recv
    }


def list_network_interfaces():
    """
    Returns all network interfaces with their IP addresses.
    """

    interfaces = []

    for interface, addresses in psutil.net_if_addrs().items():

        ips = []

        for addr in addresses:

            if addr.family == socket.AF_INET:

                ips.append(addr.address)

        interfaces.append(
            {
                "interface": interface,
                "ipv4": ips
            }
        )

    return interfaces


def check_port(port: int):
    """
    Check if a TCP port is listening on localhost.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex(("127.0.0.1", port))

    s.close()

    return {
        "port": port,
        "status": "OPEN" if result == 0 else "CLOSED"
    }


def resolve_hostname(hostname: str):
    """
    Resolve a hostname to an IP address.
    """

    try:
        ip = socket.gethostbyname(hostname)

        return {
            "hostname": hostname,
            "ip": ip
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    

def check_remote_port(host: str, port: int, timeout: int = 3):
    """
    Check whether a TCP port is open on a remote host.
    """

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {
                "host": host,
                "port": port,
                "status": "OPEN"
            }

    except Exception as e:
        return {
            "host": host,
            "port": port,
            "status": "CLOSED",
            "reason": str(e)
        
        }