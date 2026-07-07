import psutil


def get_top_cpu_processes(limit=5):
    """
    Returns the top CPU consuming processes.
    """

    # Prime CPU counters
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except Exception:
            pass

    psutil.cpu_percent(interval=1)

    processes = []

    for p in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent']
    ):
        try:
            info = p.info
            processes.append(info)
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            pass

    processes.sort(
        key=lambda x: x["cpu_percent"],
        reverse=True
    )

    return processes[:limit]

def get_top_memory_processes(limit=5):
    """
    Returns the top memory consuming processes.
    """

    processes = []

    for p in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent']
    ):
        try:
            processes.append(p.info)
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            pass

    processes.sort(
        key=lambda x: x["memory_percent"],
        reverse=True
    )

    return processes[:limit]

def search_process(name: str):
    """
    Search running processes by name.
    """

    results = []

    for p in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent']
    ):
        try:
            process_name = p.info["name"] or ""

            if name.lower() in process_name.lower():
                results.append(p.info)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            pass

    return results