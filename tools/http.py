from services.http_service import check_http_endpoint


def endpoint_health(url: str):
    return check_http_endpoint(url)