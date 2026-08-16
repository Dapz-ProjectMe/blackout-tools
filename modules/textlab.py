import base64
import hashlib
import json

from core.ui import title, success, error, info


def text_statistics():
    title("TEXT STATISTICS")

    text = input("\nMasukkan text: ")

    characters = len(text)
    characters_no_space = len(text.replace(" ", ""))
    words = len(text.split())
    lines = len(text.splitlines()) if text else 0

    print()
    print(f"Characters          : {characters}")
    print(f"Characters no space : {characters_no_space}")
    print(f"Words               : {words}")
    print(f"Lines               : {lines}")

    success("Statistics complete.")


def word_counter():
    title("WORD COUNTER")

    text = input("\nMasukkan text: ").strip()

    if not text:
        error("Text kosong.")
        return

    words = text.split()

    print(f"\nTotal words : {len(words)}")

    success("Word counting complete.")


def line_counter():
    title("LINE COUNTER")

    print("\nMasukkan text.")
    print("Ketik END pada baris terakhir.\n")

    lines = []

    while True:
        line = input()

        if line == "END":
            break

        lines.append(line)

    print(f"\nTotal lines : {len(lines)}")

    success("Line counting complete.")


def json_formatter():
    title("JSON FORMATTER")

    print("\nMasukkan JSON dalam satu baris.")
    print('Contoh: {"name":"BLACKOUT","version":2}\n')

    raw = input("JSON > ").strip()

    if not raw:
        error("JSON kosong.")
        return

    try:
        data = json.loads(raw)

        print("\nFormatted JSON:")
        print(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            )
        )

        success("JSON valid.")

    except json.JSONDecodeError as e:
        error(f"Invalid JSON: {e}")


def base64_encode():
    title("BASE64 ENCODE")

    text = input("\nText: ")

    if not text:
        error("Text kosong.")
        return

    encoded = base64.b64encode(
        text.encode("utf-8")
    ).decode("utf-8")

    print(f"\nEncoded:\n{encoded}")

    success("Encoding complete.")


def base64_decode():
    title("BASE64 DECODE")

    encoded = input("\nBase64: ").strip()

    if not encoded:
        error("Input kosong.")
        return

    try:
        decoded = base64.b64decode(
            encoded,
            validate=True
        ).decode("utf-8")

        print(f"\nDecoded:\n{decoded}")

        success("Decoding complete.")

    except Exception:
        error("Base64 tidak valid.")


def hash_text():
    title("HASH TEXT")

    text = input("\nText: ")

    if not text:
        error("Text kosong.")
        return

    data = text.encode("utf-8")

    print()
    print(f"MD5    : {hashlib.md5(data).hexdigest()}")
    print(f"SHA1   : {hashlib.sha1(data).hexdigest()}")
    print(f"SHA256 : {hashlib.sha256(data).hexdigest()}")

    success("Hash generation complete.")


def case_converter():
    title("TEXT CASE CONVERTER")

    text = input("\nText: ")

    if not text:
        error("Text kosong.")
        return

    print()
    print(f"UPPERCASE : {text.upper()}")
    print(f"lowercase : {text.lower()}")
    print(f"Title Case: {text.title()}")
    print(f"Swap Case : {text.swapcase()}")

    success("Conversion complete.")


def text_lab():
    while True:
        title("TEXT & DATA LAB")

        print("""
[1] Text statistics
[2] Word counter
[3] Line counter
[4] JSON formatter
[5] Base64 encode
[6] Base64 decode
[7] Hash text
[8] Text case converter
[0] Back
""")

        choice = input("TEXTLAB > ").strip()

        if choice == "1":
            text_statistics()

        elif choice == "2":
            word_counter()

        elif choice == "3":
            line_counter()

        elif choice == "4":
            json_formatter()

        elif choice == "5":
            base64_encode()

        elif choice == "6":
            base64_decode()

        elif choice == "7":
            hash_text()

        elif choice == "8":
            case_converter()

        elif choice == "0":
            break

        else:
            error("Pilihan tidak valid.")

        input("\nENTER untuk kembali...")
