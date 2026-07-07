import psutil
import time


def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    return {
        "uptime_seconds": uptime_seconds
    }