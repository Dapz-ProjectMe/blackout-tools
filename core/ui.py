import os
import time

RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
DIM = "\033[2m"


def clear():
    os.system("clear")


def slow(text, delay=0.01):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)

    print()


def banner():
    clear()

    print(CYAN + BOLD + r"""
╔══════════════════════════════════════════════╗
║                                              ║
║       ██████╗ ██╗      █████╗  ██████╗      ║
║       ██╔══██╗██║     ██╔══██╗██╔════╝      ║
║       ██████╔╝██║     ███████║██║           ║
║       ██╔══██╗██║     ██╔══██║██║           ║
║       ██████╔╝███████╗██║  ██║╚██████╗      ║
║       ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝      ║
║                                              ║
║          D I G I T A L   T O O L K I T      ║
║                    V 2 . 0                   ║
║                                              ║
╚══════════════════════════════════════════════╝
""" + RESET)


def menu():
    print(CYAN + """
╔══════════════════════════════════════════════╗
║                 MAIN MENU                    ║
╠══════════════════════════════════════════════╣
║  [1] SYSTEM INTELLIGENCE                     ║
║  [2] FILE MANAGER                            ║
║  [3] TEXT & DATA LAB                         ║
║  [4] NETWORK DIAGNOSTICS                     ║
║  [5] SECURITY UTILITIES                      ║
║  [6] PROCESS CENTER                          ║
║  [7] AUTOMATION                              ║
║  [8] SETTINGS                                ║
║  [0] EXIT                                    ║
╚══════════════════════════════════════════════╝
""" + RESET)


def title(text):
    print(
        "\n"
        + MAGENTA
        + BOLD
        + f"═══ {text} ═══"
        + RESET
    )


def success(text):
    print(f"{GREEN}[✓] {text}{RESET}")


def error(text):
    print(f"{RED}[!] {text}{RESET}")


def info(text):
    print(f"{CYAN}[i] {text}{RESET}")


def warning(text):
    print(f"{YELLOW}[!] {text}{RESET}")


def pause():
    input(
        f"\n{DIM}"
        "Press ENTER to continue..."
        f"{RESET}"
)
