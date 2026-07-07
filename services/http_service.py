import time
import requests


def check_http_endpoint(url: str):
    """
    Check if an HTTP endpoint is reachable.
    """

    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=5)

        end = time.perf_counter()

        return {
            "url": url,
            "reachable": True,
            "status_code": response.status_code,
            "response_time_ms": round((end - start) * 1000, 2)
        }

    except Exception as e:

        end = time.perf_counter()

        return {
            "url": url,
            "reachable": False,
            "status_code": None,
            "response_time_ms": round((end - start) * 1000, 2),
            "error": str(e)
        }