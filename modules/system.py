import os
import platform
import shutil
import socket

from core.ui import title, success, error


def read_file(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except (OSError, IOError):
        return None


def get_memory():
    data = read_file("/proc/meminfo")

    if not data:
        return None, None

    total = 0
    available = 0

    for line in data.splitlines():
        if line.startswith("MemTotal:"):
            total = int(line.split()[1])

        elif line.startswith("MemAvailable:"):
            available = int(line.split()[1])

    if total:
        used = total - available

        return (
            round(total / 1024 / 1024, 2),
            round(used / 1024 / 1024, 2)
        )

    return None, None


def get_uptime():
    data = read_file("/proc/uptime")

    if not data:
        return "Unknown"

    try:
        seconds = int(float(data.split()[0]))

        days = seconds // 86400
        seconds %= 86400

        hours = seconds // 3600
        seconds %= 3600

        minutes = seconds // 60

        return f"{days}d {hours}h {minutes}m"

    except (ValueError, IndexError):
        return "Unknown"


def get_storage():
    try:
        total, used, free = shutil.disk_usage("/")

        return (
            round(total / 1024**3, 2),
            round(used / 1024**3, 2),
            round(free / 1024**3, 2)
        )

    except OSError:
        return None, None, None


def get_cpu():
    try:
        return os.cpu_count() or "Unknown"
    except Exception:
        return "Unknown"


def get_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "Unknown"


def show_system_info():
    title("SYSTEM INTELLIGENCE")

    memory_total, memory_used = get_memory()
    storage_total, storage_used, storage_free = get_storage()

    print()

    print("DEVICE")
    print("────────────────────────────────")

    print(f"OS             : {platform.system()}")
    print(f"OS VERSION     : {platform.release()}")
    print(f"ARCHITECTURE   : {platform.machine()}")
    print(f"PYTHON         : {platform.python_version()}")
    print(f"HOSTNAME       : {get_hostname()}")

    print()

    print("PROCESSOR")
    print("────────────────────────────────")
    print(f"CPU CORES      : {get_cpu()}")

    print()

    print("MEMORY")
    print("────────────────────────────────")

    if memory_total is not None:
        memory_percent = (memory_used / memory_total) * 100

        print(f"TOTAL          : {memory_total} GB")
        print(f"USED           : {memory_used} GB")
        print(f"USAGE          : {memory_percent:.1f}%")
    else:
        print("Memory information unavailable.")

    print()

    print("STORAGE")
    print("────────────────────────────────")

    if storage_total is not None:
        storage_percent = (storage_used / storage_total) * 100

        print(f"TOTAL          : {storage_total} GB")
        print(f"USED           : {storage_used} GB")
        print(f"FREE           : {storage_free} GB")
        print(f"USAGE          : {storage_percent:.1f}%")
    else:
        print("Storage information unavailable.")

    print()

    print("SYSTEM")
    print("────────────────────────────────")
    print(f"UPTIME         : {get_uptime()}")
    print(f"CURRENT DIR    : {os.getcwd()}")

    print()

    success("System analysis complete.")
