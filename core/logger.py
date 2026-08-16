import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "blackout.log")


def init_logger():
    os.makedirs(LOG_DIR, exist_ok=True)


def log(message):
    init_logger()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"[{timestamp}] {message}\n")
