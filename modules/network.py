import os
import socket
import subprocess
import urllib.error
import urllib.request

from core.ui import title, success, error, info


USER_AGENT = "BLACKOUT-Network-Diagnostics/2.1"


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        return result.stdout.strip(), result.stderr.strip()

    except FileNotFoundError:
        return "", f"Command tidak tersedia: {command[0]}"

    except subprocess.TimeoutExpired:
        return "", "Command timeout."

    except Exception as exc:
        return "", str(exc)


def network_interfaces():
    title("NETWORK INTERFACES")

    output, error_message = run_command(["ip", "addr"])

    if output:
        print()
        print(output)
        success("Interface information loaded.")
    else:
        error(
            error_message
            or "Tidak dapat membaca network interface."
        )


def dns_lookup():
    title("DNS LOOKUP")

    hostname = input("\nHostname/domain: ").strip()

    if not hostname:
        error("Hostname kosong.")
        return

    try:
        results = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )

        addresses = sorted({
            result[4][0]
            for result in results
        })

        if not addresses:
            error("Tidak ditemukan alamat IP.")
            return

        print()

        for address in addresses:
            print(f"[FOUND] {address}")

        success(
            f"{len(addresses)} address ditemukan."
        )

    except socket.gaierror:
        error("DNS lookup gagal.")

    except Exception as exc:
        error(str(exc))


def ping_host():
    title("PING HOST")

    host = input("\nHost/IP: ").strip()

    if not host:
        error("Host kosong.")
        return

    output, error_message = run_command(
        ["ping", "-c", "4", host]
    )

    print()

    if output:
        print(output)
        success("Ping selesai.")
    else:
        error(
            error_message
            or "Ping gagal."
        )


def http_check():
    title("HTTP CONNECTIVITY")

    url = input(
        "\nURL "
        "(contoh: https://example.com): "
    ).strip()

    if not url:
        error("URL kosong.")
        return

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    try:
        request = urllib.request.Request(
            url,
            method="HEAD",
            headers={
                "User-Agent": USER_AGENT
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:

            print()
            print(f"URL       : {url}")
            print(f"Status    : {response.status}")
            print(f"Reason    : {response.reason}")
            print(f"Final URL : {response.geturl()}")

            success("HTTP connectivity OK.")

    except urllib.error.HTTPError as exc:
        print()
        print(f"URL       : {url}")
        print(f"Status    : {exc.code}")
        print(f"Reason    : {exc.reason}")

        info(
            "Server merespons, tetapi "
            "status HTTP menunjukkan error."
        )

    except urllib.error.URLError as exc:
        error(
            f"Koneksi gagal: {exc.reason}"
        )

    except Exception as exc:
        error(str(exc))


def local_ip_information():
    title("LOCAL IP INFORMATION")

    try:
        hostname = socket.gethostname()

        print(f"\nHostname : {hostname}")

        addresses = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_UNSPEC,
            socket.SOCK_DGRAM
        )

        ips = sorted({
            item[4][0]
            for item in addresses
            if item[4][0]
        })

        if ips:
            print("\nIP Addresses:")

            for ip in ips:
                print(f"  • {ip}")

        else:
            info(
                "Tidak ada alamat IP "
                "yang ditemukan."
            )

        success(
            "Local IP information loaded."
        )

    except Exception as exc:
        error(str(exc))


def connection_diagnostics():
    title("CONNECTION DIAGNOSTICS")

    targets = [
        (
            "Cloudflare",
            "https://1.1.1.1"
        ),
        (
            "Google",
            "https://www.google.com"
        ),
        (
            "GitHub",
            "https://github.com"
        )
    ]

    print()

    success_count = 0

    for name, url in targets:

        try:
            request = urllib.request.Request(
                url,
                method="HEAD",
                headers={
                    "User-Agent": USER_AGENT
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=5
            ) as response:

                print(
                    f"[OK]   "
                    f"{name:<12} "
                    f"HTTP {response.status}"
                )

                success_count += 1

        except Exception:
            print(
                f"[FAIL] "
                f"{name:<12} "
                f"No connection"
            )

    print()

    if success_count == len(targets):

        success(
            "Internet connectivity "
            "looks healthy."
        )

    elif success_count > 0:

        info(
            f"{success_count}/"
            f"{len(targets)} "
            "target dapat diakses."
        )

    else:

        error(
            "Tidak ada target "
            "yang dapat diakses."
        )


def network_summary():
    title("NETWORK SUMMARY")

    print()

    hostname = socket.gethostname()

    print(f"Hostname : {hostname}")

    try:
        local_ip = socket.gethostbyname(
            hostname
        )

        print(f"Local IP : {local_ip}")

    except Exception:
        print("Local IP : Unknown")

    print()
    print("Connectivity test:")

    try:
        request = urllib.request.Request(
            "https://www.google.com",
            method="HEAD",
            headers={
                "User-Agent":
                    "BLACKOUT/2.1"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            print("Internet : ONLINE")
            print(
                f"HTTP     : {response.status}"
            )

    except Exception:
        print("Internet : OFFLINE")

    success(
        "Network summary complete."
    )


def network_diagnostics():
    while True:

        title("NETWORK DIAGNOSTICS")

        print("""
[1] Network interfaces
[2] DNS lookup
[3] Ping host
[4] HTTP connectivity
[5] Local IP information
[6] Connection diagnostics
[7] Network summary
[0] Back
""")

        choice = input(
            "NETWORK > "
        ).strip()

        if choice == "1":
            network_interfaces()

        elif choice == "2":
            dns_lookup()

        elif choice == "3":
            ping_host()

        elif choice == "4":
            http_check()

        elif choice == "5":
            local_ip_information()

        elif choice == "6":
            connection_diagnostics()

        elif choice == "7":
            network_summary()

        elif choice == "0":
            break

        else:
            error("Pilihan tidak valid.")

        input(
            "\nENTER untuk kembali..."
        )
