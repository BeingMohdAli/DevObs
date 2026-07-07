from services.log_service import (
    read_logs,
    search_logs,
    count_log_level,
    tail_logs
)


def read_application_logs():
    return read_logs()


def search_application_logs(keyword: str):
    return search_logs(keyword)


def count_logs(level: str):
    return count_log_level(level)


def tail_application_logs(lines: int):
    return tail_logs(lines)