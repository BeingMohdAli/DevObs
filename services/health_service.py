from services.cpu_service import get_cpu_usage
from services.memory_service import get_memory_usage
from services.disk_service import get_disk_usage
from services.uptime_service import get_uptime


def get_system_health():
    """
    Generate an overall health report.
    """

    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    uptime = get_uptime()

    report = {
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "uptime": uptime,
        "overall_status": "Healthy"
    }

    return report