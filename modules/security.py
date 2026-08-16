import hashlib
import os
import re
import secrets
import string

from core.ui import title, success, error, info


# ==============================
# FILE HASH ANALYZER
# ==============================

def hash_file(algorithm):
    title(f"{algorithm.upper()} FILE HASH")

    path = input("\nFile path: ").strip()

    if not os.path.isfile(path):
        error("File tidak ditemukan.")
        return

    try:
        hasher = hashlib.new(algorithm)

        with open(path, "rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                hasher.update(chunk)

        print()
        print(f"File   : {os.path.abspath(path)}")
        print(f"Size   : {os.path.getsize(path)} bytes")
        print(f"{algorithm.upper():<7}: {hasher.hexdigest()}")

        success("Hash berhasil dihitung.")

    except Exception as exc:
        error(str(exc))


# ==============================
# HASH COMPARE
# ==============================

def hash_compare():
    title("HASH COMPARE")

    first = input("\nHash pertama : ").strip().lower()
    second = input("Hash kedua   : ").strip().lower()

    if not first or not second:
        error("Hash tidak boleh kosong.")
        return

    print()

    if first == second:
        success("HASH MATCH — nilainya sama.")
    else:
        error("HASH MISMATCH — nilainya berbeda.")


# ==============================
# PASSWORD STRENGTH
# ==============================

def password_strength():
    title("PASSWORD STRENGTH ANALYZER")

    password = input("\nPassword: ")

    if not password:
        error("Password kosong.")
        return

    score = 0
    checks = []

    if len(password) >= 8:
        score += 1
        checks.append("✓ Minimal 8 karakter")
    else:
        checks.append("✗ Minimal 8 karakter")

    if len(password) >= 12:
        score += 1
        checks.append("✓ Minimal 12 karakter")
    else:
        checks.append("• 12+ karakter akan lebih baik")

    if re.search(r"[a-z]", password):
        score += 1
        checks.append("✓ Huruf kecil")
    else:
        checks.append("✗ Huruf kecil")

    if re.search(r"[A-Z]", password):
        score += 1
        checks.append("✓ Huruf besar")
    else:
        checks.append("✗ Huruf besar")

    if re.search(r"\d", password):
        score += 1
        checks.append("✓ Angka")
    else:
        checks.append("✗ Angka")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
        checks.append("✓ Simbol")
    else:
        checks.append("✗ Simbol")

    if score <= 2:
        level = "WEAK"
    elif score <= 4:
        level = "MEDIUM"
    else:
        level = "STRONG"

    print()
    print(f"Score : {score}/6")
    print(f"Level : {level}")
    print()

    for check in checks:
        print(check)

    info(
        "Analisis dilakukan secara lokal."
    )


# ==============================
# SECRET / TOKEN DETECTOR
# ==============================

SECRET_PATTERNS = {
    "Generic API Key": re.compile(
        r"(?i)(api[_-]?key|apikey)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}"
    ),
    "Generic Secret": re.compile(
        r"(?i)(secret|client_secret)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}"
    ),
    "Password Assignment": re.compile(
        r"(?i)(password|passwd|pwd)\s*[:=]\s*[\"'][^\"']{4,}[\"']"
    ),
    "Bearer Token": re.compile(
        r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*"
    ),
}


def scan_file_for_secrets(path):
    findings = []

    try:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            content = file.read()

    except Exception:
        return findings

    for name, pattern in SECRET_PATTERNS.items():

        for match in pattern.finditer(content):
            line_number = (
                content[:match.start()].count("\n") + 1
            )

            findings.append({
                "type": name,
                "line": line_number
            })

    return findings


def secret_detector():
    title("SECRET / TOKEN DETECTOR")

    root = input(
        "\nFolder/file to scan: "
    ).strip()

    if not os.path.exists(root):
        error("Path tidak ditemukan.")
        return

    files_to_scan = []

    if os.path.isfile(root):
        files_to_scan.append(root)

    else:
        for current_root, dirs, files in os.walk(root):

            # Skip common generated folders.
            dirs[:] = [
                directory
                for directory in dirs
                if directory not in {
                    ".git",
                    "__pycache__",
                    "node_modules"
                }
            ]

            for filename in files:
                path = os.path.join(
                    current_root,
                    filename
                )

                if os.path.getsize(path) <= 2 * 1024 * 1024:
                    files_to_scan.append(path)

    print()
    print(
        f"Scanning {len(files_to_scan)} file(s)..."
    )
    print()

    total = 0

    for path in files_to_scan:

        findings = scan_file_for_secrets(path)

        for finding in findings:

            print(
                f"[WARNING
