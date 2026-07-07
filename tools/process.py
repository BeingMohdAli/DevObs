from services.process_service import get_top_cpu_processes
from services.process_service import (
    get_top_cpu_processes,
    get_top_memory_processes,
    search_process as search_process_service
)


def top_cpu_processes():
    return get_top_cpu_processes()




def top_cpu_processes():
    return get_top_cpu_processes()


def top_memory_processes():
    return get_top_memory_processes()

def search_process(name: str):
    return search_process_service(name)