import os

LOG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "sample_logs",
    "application.log"
)


def read_logs():
    """
    Read the entire log file.
    """
    with open(LOG_FILE, "r") as file:
        return file.read()


def search_logs(keyword: str):
    """
    Search logs for a keyword.
    """
    matches = []

    with open(LOG_FILE, "r") as file:
        for line in file:
            if keyword.lower() in line.lower():
                matches.append(line.strip())

    return matches


def count_log_level(level: str):
    """
    Count INFO/WARN/ERROR entries.
    """
    count = 0

    with open(LOG_FILE, "r") as file:
        for line in file:
            if level.upper() in line:
                count += 1

    return {
        "level": level.upper(),
        "count": count
    }


def tail_logs(lines: int = 10):
    """
    Return the last N lines from the log file.
    """
    with open(LOG_FILE, "r") as file:
        content = file.readlines()

    return [line.strip() for line in content[-lines:]]