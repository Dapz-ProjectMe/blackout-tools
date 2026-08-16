import os
import time

from core.ui import title, success, error, info


def read_file(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except (OSError, IOError):
        return None


def get_processes():
    processes = []

    proc_path = "/proc"

    try:
        entries = os.listdir(proc_path)
    except OSError as exc:
        error(str(exc))
        return []

    for pid in entries:
        if not pid.isdigit():
            continue

        status_path = os.path.join(
            proc_path,
            pid,
            "status"
        )

        data = read_file(status_path)

        if not data:
            continue

        name = "Unknown"
        state = "Unknown"
        memory = "Unknown"

        for line in data.splitlines():

            if line.startswith("Name:"):
                name = line.split(
                    ":", 1
                )[1].strip()

            elif line.startswith("State:"):
                state = line.split(
                    ":", 1
                )[1].strip()

            elif line.startswith("VmRSS:"):
                memory = line.split(
                    ":", 1
                )[1].strip()

        processes.append({
            "pid": pid,
            "name": name,
            "state": state,
            "memory": memory
        })

    return sorted(
        processes,
        key=lambda process: int(
            process["pid"]
        )
    )


def list_processes():
    title("RUNNING PROCESSES")

    processes = get_processes()

    if not processes:
        info(
            "Tidak dapat membaca "
            "daftar proses."
        )
        return

    print()
    print(
        f"{'PID':<8}"
        f"{'STATE':<20}"
        f"{'MEMORY':<14}"
        f"NAME"
    )

    print("─" * 70)

    for process in processes:
        print(
            f"{process['pid']:<8}"
            f"{process['state'][:18]:<20}"
            f"{process['memory']:<14}"
            f"{process['name']}"
        )

    print()
    success(
        f"{len(processes)} proses ditemukan."
    )


def search_process():
    title("SEARCH PROCESS")

    query = input(
        "\nNama proses: "
    ).strip().lower()

    if not query:
        error("Nama proses kosong.")
        return

    processes = get_processes()

    results = [
        process
        for process in processes
        if query in process["name"].lower()
    ]

    print()

    if not results:
        info(
            "Proses tidak ditemukan."
        )
        return

    print(
        f"{'PID':<8}"
        f"{'STATE':<20}"
        f"{'MEMORY':<14}"
        f"NAME"
    )

    print("─" * 70)

    for process in results:
        print(
            f"{process['pid']:<8}"
            f"{process['state'][:18]:<20}"
            f"{process['memory']:<14}"
            f"{process['name']}"
        )

    print()

    success(
        f"{len(results)} proses cocok."
    )


def process_information():
    title("PROCESS INFORMATION")

    pid = input(
        "\nPID: "
    ).strip()

    if not pid.isdigit():
        error("PID tidak valid.")
        return

    status_path = (
        f"/proc/{pid}/status"
    )

    if not os.path.exists(status_path):
        error(
            "Proses tidak ditemukan."
        )
        return

    data = read_file(status_path)

    if not data:
        error(
            "Tidak dapat membaca "
            "informasi proses."
        )
        return

    print()
    print(data)

    success(
        "Process information loaded."
    )


def process_statistics():
    title("PROCESS STATISTICS")

    processes = get_processes()

    if not processes:
        error(
            "Tidak dapat membaca "
            "proses."
        )
        return

    total = len(processes)

    running = 0
    sleeping = 0
    stopped = 0
    zombie = 0

    for process in processes:

        state = process["state"]

        if state.startswith("R"):
            running += 1

        elif state.startswith("S"):
            sleeping += 1

        elif state.startswith("T"):
            stopped += 1

        elif state.startswith("Z"):
            zombie += 1

    print()

    print(
        f"TOTAL PROCESSES : {total}"
    )

    print(
        f"RUNNING         : {running}"
    )

    print(
        f"SLEEPING        : {sleeping}"
    )

    print(
        f"STOPPED         : {stopped}"
    )

    print(
        f"ZOMBIE          : {zombie}"
    )

    print()

    success(
        "Process statistics complete."
    )


def current_process():
    title("CURRENT PROCESS")

    pid = os.getpid()

    print()

    print(
        f"PID          : {pid}"
    )

    print(
        f"Parent PID   : {os.getppid()}"
    )

    print(
        f"Working Dir  : {os.getcwd()}"
    )

    print(
        f"User ID      : {os.getuid()}"
    )

    print(
        f"Process Name : BLACKOUT"
    )

    print()

    success(
        "Current process information loaded."
    )


def process_center():

    while True:

        title("PROCESS CENTER")

        print("""
[1] List processes
[2] Search process
[3] Process information
[4] Process statistics
[5] Current process
[0] Back
""")

        choice = input(
            "PROCESS > "
        ).strip()

        if choice == "1":
            list_processes()

        elif choice == "2":
            search_process()

        elif choice == "3":
            process_information()

        elif choice == "4":
            process_statistics()

        elif choice == "5":
            current_process()

        elif choice == "0":
            break

        else:
            error(
                "Pilihan tidak valid."
            )

        input(
            "\nENTER untuk kembali..."
        )
