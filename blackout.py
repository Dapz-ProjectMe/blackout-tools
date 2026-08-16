from core.ui import (
    banner,
    menu,
    title,
    info,
    pause
)

from core.config import load_config
from core.logger import init_logger, log

from modules.system import show_system_info
from modules.files import file_manager
from modules.textlab import text_lab
from modules.network import network_diagnostics
from modules.process import process_center
from modules.security import security_utilities
from modules.automation import automation


def main():
    config = load_config()

    init_logger()
    log("BLACKOUT started")

    banner()

    print(f"Version : {config['version']}")
    print(f"Author  : {config['author']}")

    pause()

    while True:
        banner()
        menu()

        choice = input("\nBLACKOUT > ").strip()

        if choice == "1":
            show_system_info()
            pause()

        elif choice == "2":
            file_manager()

        elif choice == "3":
            text_lab()

        elif choice == "4":
            network_diagnostics()

        elif choice == "5":
            security_utilities()

        elif choice == "6":
            process_center()

        elif choice == "7":
          from modules.project_generator import project_generator
            project_generator()

        elif choice == "8":
            title("SETTINGS")
            info("Settings akan dipasang pada tahap berikutnya.")
            pause()

        elif choice == "0":
            log("BLACKOUT stopped")
            print("\nBLACKOUT shutting down...")
            break

        else:
            print("\nCommand tidak dikenal.")
            pause()


if __name__ == "__main__":
    main()
