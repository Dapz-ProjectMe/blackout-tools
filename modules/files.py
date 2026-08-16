import os
import shutil
import datetime

from core.ui import title, success, error, info


def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def list_files():
    title("BROWSE FILES")

    current = os.getcwd()

    print(f"\nLocation: {current}\n")

    try:
        items = sorted(os.listdir(current))

        if not items:
            info("Folder kosong.")
            return

        for index, item in enumerate(items, 1):
            path = os.path.join(current, item)

            try:
                if os.path.isdir(path):
                    print(f"  {index:02}. [DIR]  {item}")
                else:
                    size = human_size(os.path.getsize(path))
                    print(f"  {index:02}. [FILE] {item} ({size})")
            except OSError:
                print(f"  {index:02}. [????] {item}")

    except PermissionError:
        error("Tidak memiliki izin untuk membaca folder.")

    except OSError as e:
        error(str(e))


def search_files():
    title("SEARCH FILES")

    query = input("\nNama file yang dicari: ").strip()

    if not query:
        error("Nama pencarian kosong.")
        return

    found = 0

    print()

    for root, dirs, files in os.walk(os.getcwd()):
        for filename in files:

            if query.lower() in filename.lower():
                path = os.path.join(root, filename)

                print(f"[FOUND] {path}")
                found += 1

    if found == 0:
        info("Tidak ditemukan.")
    else:
        success(f"{found} file ditemukan.")


def file_information():
    title("FILE INFORMATION")

    path = input("\nPath file: ").strip()

    if not os.path.exists(path):
        error("File tidak ditemukan.")
        return

    if os.path.isdir(path):
        error("Path tersebut adalah folder.")
        return

    try:
        size = os.path.getsize(path)
        modified = os.path.getmtime(path)

        modified_time = datetime.datetime.fromtimestamp(
            modified
        ).strftime("%Y-%m-%d %H:%M:%S")

        print()
        print(f"Name       : {os.path.basename(path)}")
        print(f"Path       : {os.path.abspath(path)}")
        print(f"Size       : {human_size(size)}")
        print(f"Modified   : {modified_time}")
        print(f"Extension  : {os.path.splitext(path)[1] or 'None'}")

    except OSError as e:
        error(str(e))


def create_folder():
    title("CREATE FOLDER")

    name = input("\nNama folder: ").strip()

    if not name:
        error("Nama folder kosong.")
        return

    if os.path.exists(name):
        error("Folder/file dengan nama tersebut sudah ada.")
        return

    try:
        os.mkdir(name)
        success(f"Folder '{name}' berhasil dibuat.")

    except OSError as e:
        error(str(e))


def rename_item():
    title("RENAME")

    old = input("\nNama/path lama: ").strip()
    new = input("Nama/path baru: ").strip()

    if not os.path.exists(old):
        error("File/folder tidak ditemukan.")
        return

    if os.path.exists(new):
        error("Tujuan sudah ada.")
        return

    try:
        os.rename(old, new)
        success("Berhasil diubah namanya.")

    except OSError as e:
        error(str(e))


def copy_item():
    title("COPY")

    source = input("\nSource: ").strip()
    destination = input("Destination: ").strip()

    if not os.path.exists(source):
        error("Source tidak ditemukan.")
        return

    if os.path.exists(destination):
        error("Destination sudah ada.")
        return

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

        success("Copy berhasil.")

    except OSError as e:
        error(str(e))


def move_item():
    title("MOVE")

    source = input("\nSource: ").strip()
    destination = input("Destination: ").strip()

    if not os.path.exists(source):
        error("Source tidak ditemukan.")
        return

    if os.path.exists(destination):
        error("Destination sudah ada.")
        return

    try:
        shutil.move(source, destination)
        success("Move berhasil.")

    except OSError as e:
        error(str(e))


def delete_item():
    title("DELETE")

    path = input("\nFile/folder yang ingin dihapus: ").strip()

    if not os.path.exists(path):
        error("Tidak ditemukan.")
        return

    print(f"\nTarget: {os.path.abspath(path)}")

    confirmation = input(
        "Ketik DELETE untuk menghapus: "
    ).strip()

    if confirmation != "DELETE":
        info("Penghapusan dibatalkan.")
        return

    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

        success("Berhasil dihapus.")

    except OSError as e:
        error(str(e))


def storage_analyzer():
    title("STORAGE ANALYZER")

    root = os.getcwd()

    total_size = 0
    file_count = 0
    folder_count = 0

    print("\nAnalyzing...\n")

    for current_root, dirs, files in os.walk(root):
        folder_count += len(dirs)

        for filename in files:
            try:
                path = os.path.join(current_root, filename)
                total_size += os.path.getsize(path)
                file_count += 1
            except OSError:
                pass

    print(f"Root         : {root}")
    print(f"Files        : {file_count}")
    print(f"Folders      : {folder_count}")
    print(f"Total size   : {human_size(total_size)}")

    success("Analysis complete.")


def file_manager():
    while True:
        title("FILE MANAGER")

        print("""
[1] Browse files
[2] Search files
[3] File information
[4] Create folder
[5] Rename
[6] Copy
[7] Move
[8] Delete
[9] Storage analyzer
[0] Back
""")

        choice = input("FILEMANAGER > ").strip()

        if choice == "1":
            list_files()

        elif choice == "2":
            search_files()

        elif choice == "3":
            file_information()

        elif choice == "4":
            create_folder()

        elif choice == "5":
            rename_item()

        elif choice == "6":
            copy_item()

        elif choice == "7":
            move_item()

        elif choice == "8":
            delete_item()

        elif choice == "9":
            storage_analyzer()

        elif choice == "0":
            break

        else:
            error("Pilihan tidak valid.")

        input("\nENTER untuk kembali...")
