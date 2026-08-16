import re
import json
from collections import Counter

from core.ui import title, success, error, info


def word_counter():
    title("WORD COUNTER")

    text = input("\nMasukkan teks: ").strip()

    if not text:
        error("Teks kosong.")
        return

    words = re.findall(r"\b[\w'-]+\b", text)

    characters = len(text)
    characters_no_space = len(text.replace(" ", ""))
    word_count = len(words)
    lines = len(text.splitlines()) or 1

    print()
    print(f"Characters          : {characters}")
    print(f"Characters no space : {characters_no_space}")
    print(f"Words               : {word_count}")
    print(f"Lines               : {lines}")

    success("Text analysis complete.")


def text_case_converter():
    title("CASE CONVERTER")

    text = input("\nText: ")

    if not text:
        error("Teks kosong.")
        return

    print("""
[1] UPPERCASE
[2] lowercase
[3] Title Case
[4] Capitalize
[5] Swap Case
[0] Back
""")

    choice = input("CASE > ").strip()

    if choice == "1":
        result = text.upper()

    elif choice == "2":
        result = text.lower()

    elif choice == "3":
        result = text.title()

    elif choice == "4":
        result = text.capitalize()

    elif choice == "5":
        result = text.swapcase()

    elif choice == "0":
        return

    else:
        error("Pilihan tidak valid.")
        return

    print("\nRESULT")
    print("────────────────────────────────")
    print(result)

    success("Conversion complete.")


def character_frequency():
    title("CHARACTER FREQUENCY")

    text = input("\nText: ")

    if not text:
        error("Teks kosong.")
        return

    characters = Counter(
        char.lower()
        for char in text
        if not char.isspace()
    )

    print("\nFREQUENCY")
    print("────────────────────────────────")

    for char, count in characters.most_common():
        display = "[space]" if char == " " else char
        print(f"{display:10} : {count}")

    success("Frequency analysis complete.")


def word_frequency():
    title("WORD FREQUENCY")

    text = input("\nText: ").strip()

    if not text:
        error("Teks kosong.")
        return

    words = re.findall(r"\b[\w'-]+\b", text.lower())

    if not words:
        info("Tidak ada kata yang ditemukan.")
        return

    frequency = Counter(words)

    print("\nWORD FREQUENCY")
    print("────────────────────────────────")

    for word, count in frequency.most_common():
        print(f"{word:20} : {count}")

    success("Word frequency analysis complete.")


def remove_extra_spaces():
    title("TEXT CLEANER")

    text = input("\nText: ")

    if not text:
        error("Teks kosong.")
        return

    cleaned = re.sub(r"[ \t]+", " ", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()

    print("\nCLEAN RESULT")
    print("────────────────────────────────")
    print(cleaned)

    success("Text cleaned successfully.")


def json_formatter():
    title("JSON FORMATTER")

    print("\nMasukkan JSON satu baris.")
    raw = input("JSON > ").strip()

    if not raw:
        error("JSON kosong.")
        return

    try:
        data = json.loads(raw)

        formatted = json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        )

        print("\nFORMATTED JSON")
        print("────────────────────────────────")
        print(formatted)

        success("JSON berhasil diformat.")

    except json.JSONDecodeError as exc:
        error(f"JSON tidak valid: {exc}")


def text_lab():
    while True:
        title("TEXT & DATA LAB")

        print("""
[1] Word counter
[2] Case converter
[3] Character frequency
[4] Word frequency
[5] Text cleaner
[6] JSON formatter
[0] Back
""")

        choice = input("TEXTLAB > ").strip()

        if choice == "1":
            word_counter()

        elif choice == "2":
            text_case_converter()

        elif choice == "3":
            character_frequency()

        elif choice == "4":
            word_frequency()

        elif choice == "5":
            remove_extra_spaces()

        elif choice == "6":
            json_formatter()

        elif choice == "0":
            break

        else:
            error("Pilihan tidak valid.")

        input("\nENTER untuk kembali...")
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
