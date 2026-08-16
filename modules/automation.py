import json
import os
import shutil
import subprocess
import time

from core.ui import title, success, error, info


TASK_FILE = "automation_tasks.json"


# ==============================
# TASK STORAGE
# ==============================

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return []


def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w") as file:
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as exc:
        error(str(exc))


# ==============================
# RUN COMMAND
# ==============================

def run_command():
    title("RUN COMMAND")

    command = input("\nCommand: ").strip()

    if not command:
        error("Command kosong.")
        return

    confirm = input(
        "Jalankan command? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        info("Dibatalkan.")
        return

    try:
        result = subprocess.run(
            command,
            shell=True
        )

        if result.returncode == 0:
            success("Command selesai.")
        else:
            error(
                f"Exit code: {result.returncode}"
            )

    except Exception as exc:
        error(str(exc))


# ==============================
# REPEAT COMMAND
# ==============================

def repeat_command():
    title("REPEAT COMMAND")

    command = input("\nCommand: ").strip()

    if not command:
        error("Command kosong.")
        return

    try:
        count = int(
            input("Jumlah pengulangan: ")
        )

        if count < 1 or count > 100:
            error(
                "Jumlah harus 1-100."
            )
            return

        delay = float(
            input("Delay (detik): ")
        )

        if delay < 0 or delay > 3600:
            error(
                "Delay harus 0-3600 detik."
            )
            return

    except ValueError:
        error("Input tidak valid.")
        return

    for index in range(1, count + 1):

        print(
            f"\n===== RUN {index}/{count} ====="
        )

        try:
            subprocess.run(
                command,
                shell=True
            )

        except Exception as exc:
            error(str(exc))
            break

        if index < count:
            time.sleep(delay)

    success("Repeat command selesai.")


# ==============================
# CREATE TASK
# ==============================

def create_task():
    title("CREATE TASK")

    name = input("\nNama task: ").strip()

    if not name:
        error("Nama task kosong.")
        return

    command = input("Command: ").strip()

    if not command:
        error("Command kosong.")
        return

    tasks = load_tasks()

    if any(
        task["name"].lower() == name.lower()
        for task in tasks
    ):
        error("Task sudah ada.")
        return

    tasks.append({
        "name": name,
        "command": command
    })

    save_tasks(tasks)

    success(
        f"Task '{name}' dibuat."
    )


# ==============================
# VIEW TASKS
# ==============================

def view_tasks():
    title("TASK LIST")

    tasks = load_tasks()

    if not tasks:
        info("Belum ada task.")
        return

    print()

    for index, task in enumerate(
        tasks,
        start=1
    ):
        print(
            f"[{index}] {task['name']}"
        )
        print(
            f"    {task['command']}"
        )

    print()

    success(
        f"{len(tasks)} task tersedia."
    )


# ==============================
# RUN TASK
# ==============================

def run_task():
    title("RUN TASK")

    tasks = load_tasks()

    if not tasks:
        info("Belum ada task.")
        return

    for index, task in enumerate(
        tasks,
        start=1
    ):
        print(
            f"[{index}] {task['name']}"
        )

    choice = input(
        "\nPilih task: "
    ).strip()

    if not choice.isdigit():
        error("Pilihan tidak valid.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(tasks):
        error("Task tidak ditemukan.")
        return

    task = tasks[index]

    print(
        f"\nCommand: {task['command']}"
    )

    confirm = input(
        "Jalankan? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        info("Dibatalkan.")
        return

    try:
        result = subprocess.run(
            task["command"],
            shell=True
        )

        if result.returncode == 0:
            success("Task selesai.")
        else:
            error(
                f"Exit code: {result.returncode}"
            )

    except Exception as exc:
        error(str(exc))


# ==============================
# DELETE TASK
# ==============================

def delete_task():
    title("DELETE TASK")

    tasks = load_tasks()

    if not tasks:
        info("Belum ada task.")
        return

    for index, task in enumerate(
        tasks,
        start=1
    ):
        print(
            f"[{index}] {task['name']}"
        )

    choice = input(
        "\nPilih task: "
    ).strip()

    if not choice.isdigit():
        error("Pilihan tidak valid.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(tasks):
        error("Task tidak ditemukan.")
        return

    task = tasks[index]

    confirm = input(
        f"Ketik DELETE untuk menghapus "
        f"'{task['name']}': "
    ).strip()

    if confirm != "DELETE":
        info("Dibatalkan.")
        return

    tasks.pop(index)
    save_tasks(tasks)

    success("Task dihapus.")


# ==============================
# FILE ORGANIZER
# ==============================

def file_organizer():
    title("FILE ORGANIZER")

    folder = input(
        "\nFolder: "
    ).strip()

    if not os.path.isdir(folder):
        error("Folder tidak ditemukan.")
        return

    categories = {
        "Images": [
            ".jpg", ".jpeg", ".png",
            ".gif", ".webp", ".svg"
        ],
        "Documents": [
            ".pdf", ".doc", ".docx",
            ".txt", ".md"
        ],
        "Archives": [
            ".zip", ".rar", ".7z",
            ".tar", ".gz"
        ],
        "Audio": [
            ".mp3", ".wav", ".m4a",
            ".ogg"
        ],
        "Video": [
            ".mp4", ".mkv", ".avi",
            ".mov", ".webm"
        ],
        "Code": [
            ".py", ".js", ".html",
            ".css", ".java", ".cpp"
        ]
    }

    operations = []

    for filename in os.listdir(folder):

        source = os.path.join(
            folder,
            filename
        )

        if not os.path.isfile(source):
            continue

        extension = os.path.splitext(
            filename
        )[1].lower()

        category = None

        for name, extensions in categories.items():
            if extension in extensions:
                category = name
                break

        if not category:
            continue

        destination_dir = os.path.join(
            folder,
            category
        )

        destination = os.path.join(
            destination_dir,
            filename
        )

        operations.append(
            (source, destination)
        )

    if not operations:
        info(
            "Tidak ada file yang perlu "
            "diorganisasi."
        )
        return

    print()

    for source, destination in operations:
        print(
            f"{os.path.basename(source)}"
            f" -> "
            f"{os.path.dirname(destination)}"
        )

    confirm = input(
        "\nLanjutkan? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        info("Dibatalkan.")
        return

    moved = 0

    for source, destination in operations:

        try:
            os.makedirs(
                os.path.dirname(destination),
                exist_ok=True
            )

            if os.path.exists(destination):
                info(
                    f"Skip: {destination}"
                )
                continue

            shutil.move(
                source,
                destination
            )

            moved += 1

        except Exception as exc:
            error(str(exc))

    success(
        f"{moved} file berhasil "
        "diorganisasi."
    )


# ==============================
# BACKUP FOLDER
# ==============================

def backup_folder():
    title("BACKUP FOLDER")

    source = input(
        "\nSource folder: "
    ).strip()

    if not os.path.isdir(source):
        error("Source tidak ditemukan.")
        return

    destination = input(
        "Backup destination: "
    ).strip()

    if not destination:
        error("Destination kosong.")
        return

    source_abs = os.path.abspath(source)
    destination_abs = os.path.abspath(
        destination
    )

    if destination_abs.startswith(
        source_abs + os.sep
    ):
        error(
            "Destination tidak boleh "
            "berada di dalam source."
        )
        return

    print(
        f"\nSource : {source_abs}"
    )
    print(
        f"Backup : {destination_abs}"
    )

    confirm = input(
        "Buat backup? [y/N]: "
    ).strip().lower()

    if confirm != "y":
        info("Dibatalkan.")
        return

    try:
        shutil.copytree(
            source_abs,
            destination_abs,
            dirs_exist_ok=True
        )

        success(
            "Backup berhasil dibuat."
        )

    except Exception as exc:
        error(str(exc))


# ==============================
# PROJECT GENERATOR
# ==============================

def project_generator():
    title("PROJECT GENERATOR")

    name = input(
        "\nProject name: "
    ).strip()

    if not name:
        error("Nama project kosong.")
        return

    print("""
[1] HTML
[2] Python
[3] JavaScript
""")

    choice = input(
        "Template: "
    ).strip()

    if choice not in {
        "1", "2", "3"
    }:
        error("Template tidak valid.")
        return

    if os.path.exists(name):
        error(
            "Folder project sudah ada."
        )
        return

    try:
        os.makedirs(name)

        if choice == "1":

            with open(
                os.path.join(
                    name,
                    "index.html"
                ),
                "w"
            ) as file:
                file.write(
                    """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width,
                   initial-scale=1.0">
    <title>Project</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
"""
                )

        elif choice == "2":

            with open(
                os.path.join(
                    name,
                    "main.py"
                ),
                "w"
            ) as file:
                file.write(
                    'print("Hello World")\n'
                )

        elif choice == "3":

            with open(
                os.path.join(
                    name,
                    "index.js"
                ),
                "w"
            ) as file:
                file.write(
                    'console.log("Hello World");\n'
                )

        with open(
            os.path.join(
                name,
                "README.md"
            ),
            "w"
        ) as file:
            file.write(
                f"# {name}\n\n"
                "Generated by BLACKOUT.\n"
            )

        success(
            f"Project '{name}' berhasil dibuat."
        )

    except Exception as exc:
        error(str(exc))


# ==============================
# ENVIRONMENT CHECKER
# ==============================

def environment_checker():
    title("ENVIRONMENT CHECKER")

    commands = [
        "python",
        "git",
        "node",
        "npm",
        "pip",
        "curl",
        "wget"
    ]

    print()

    available = 0

    for command in commands:

        path = shutil.which(command)

        if path:
            print(
                f"[OK]   {command:<8} {path}"
            )
            available += 1

        else:
            print(
                f"[----] {command:<8} Not found"
            )

    print()

    success(
        f"{available}/{len(commands)} "
        "tools tersedia."
    )


# ==============================
# AUTOMATION MENU
# ==============================

def automation():

    while True:

        title("AUTOMATION")

        print("""
[1] Run Command
[2] Repeat Command
[3] Create Task
[4] View Tasks
[5] Run Task
[6] Delete Task
[7] File Organizer
[8] Backup Folder
[9] Project Generator
[10] Environment Checker
[0] Back
""")

        choice = input(
            "AUTOMATION > "
        ).strip()

        if choice == "1":
            run_command()

        elif choice == "2":
            repeat_command()

        elif choice == "3":
            create_task()

        elif choice == "4":
            view_tasks()

        elif choice == "5":
            run_task()

        elif choice == "6":
            delete_task()

        elif choice == "7":
            file_organizer()

        elif choice == "8":
            backup_folder()

        elif choice == "9":
            project_generator()

        elif choice == "10":
            environment_checker()

        elif choice == "0":
            break

        else:
            error("Pilihan tidak valid.")

        input(
            "\nENTER untuk kembali..."
        )
