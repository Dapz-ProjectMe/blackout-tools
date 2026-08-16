import os

from core.ui import title, success, error, info


def get_processes():
    processes = []

    proc_path = "/proc"

    try:
        for pid in os.listdir(proc_path):
            if not pid.isdigit():
                continue

            status_path = os.path.join(proc_path, pid, "status")

            try:
                name = "Unknown"
                state = "Unknown"

                with open(status_path, "r") as file:
                    for line in file:
                        if line.startswith("Name:"):
                            name = line.split(":", 1)[1].strip()

                        elif line.startswith("State:"):
                            state = line.split(":", 1)[1].strip()

                processes.append({
                    "pid": pid,
                    "name": name,
                    "state": state
                })

            except (PermissionError, FileNotFoundError):
                continue

    except Exception as e:
        error(str(e))
        return []

    return sorted(
        processes,
        key=lambda x: int(x["pid"])
    )


def list_processes():
    title("RUNNING PROCESSES")

    processes = get_processes()

    if not processes:
        info("Tidak dapat membaca daftar proses.")
        return

    print()
    print(f"{'PID':<8} {'STATE':<20} NAME")
    print("─" * 55)

    for process in processes:
        print(
            f"{process['pid']:<8} "
            f"{process['state']:<20} "
            f"{process['name']}"
        )

    print()
    success(f"{len(processes)} proses ditemukan.")


def search_process():
    title("SEARCH PROCESS")

    query = input("\nNama proses: ").strip().lower()

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
        info("Proses tidak ditemukan.")
        return

    print(f"{'PID':<8} {'STATE':<20} NAME")
    print("─" * 55)

    for process in results:
        print(
            f"{process['pid']:<8} "
            f"{process['state']:<20} "
            f"{process['name']}"
        )

    print()
    success(f"{len(results)} proses cocok.")


def process_information():
    title("PROCESS INFORMATION")

    pid = input("\nPID: ").strip()

    if not pid.isdigit():
        error("PID tidak valid.")
        return

    status_path = f"/proc/{pid}/status"

    if not os.path.exists(status_path):
        error("Proses tidak ditemukan.")
        return

    try:
        print()

        with open(status_path, "r") as file:
            data = file.read()

        print(data)

    except PermissionError:
        error("Tidak memiliki izin membaca proses.")

    except Exception as e:
        error(str(e))


def process_center():
    while True:
        title("PROCESS CENTER")

        print("""
[1] List processes
[2] Search process
[3] Process information
[0] Back
""")

        choice = input("PROCESS > ").strip()

        if choice == "1":
            list_processes()

        elif choice == "2":
            search_process()

        elif choice == "3":
            process_information()

        elif choice == "0":
            break

        else:
            error("Pilihan tidak valid.")

        input("\nENTER untuk kembali...")
