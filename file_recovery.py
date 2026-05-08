#!/usr/bin/env python3
"""
Data Recovery Tool
This script attempts to recover readable text from corrupted or binary files.
"""

import sys
import os
import argparse
import zipfile
import io

def recover_text(file_path, min_length=4):
    """
    Attempt to recover readable text from a binary file.
    Extracts sequences of printable characters.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    recovered = []
    current = []

    for byte in data:
        char = chr(byte)
        if char.isprintable() and not char.isspace():
            current.append(char)
        else:
            if len(current) >= min_length:
                recovered.append(''.join(current))
            current = []

    # Don't forget the last sequence
    if len(current) >= min_length:
        recovered.append(''.join(current))

    return recovered

def try_zip_recovery(file_path):
    """
    Try to recover data if the file is a ZIP archive.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            for name in zf.namelist():
                with zf.open(name) as f:
                    content = f.read()
                    try:
                        text = content.decode('utf-8')
                        return f"Recovered from ZIP: {name}\n{text}"
                    except UnicodeDecodeError:
                        return f"Recovered binary from ZIP: {name}"
    except zipfile.BadZipFile:
        return None
    except Exception as e:
        print(f"Error in ZIP recovery: {e}")
        return None

def try_encoding_recovery(file_path):
    """
    Try different encodings to decode the file.
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    recovered = []
    for enc in encodings:
        try:
            text = data.decode(enc)
            recovered.append(f"Decoded with {enc}:\n{text}")
        except UnicodeDecodeError:
            continue
    return recovered

def main():
    parser = argparse.ArgumentParser(description='Recover text from corrupted files.')
    parser.add_argument('file', help='Path to the corrupted file')
    parser.add_argument('--min-length', type=int, default=4, help='Minimum length of text sequences to recover')
    parser.add_argument('--output', help='Output file to save recovered text')
    parser.add_argument('--try-zip', action='store_true', help='Try to recover as ZIP file')
    parser.add_argument('--try-encodings', action='store_true', help='Try different encodings')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File {args.file} does not exist.")
        return

    all_recovered = []

    # Try ZIP recovery
    if args.try_zip:
        zip_result = try_zip_recovery(args.file)
        if zip_result:
            all_recovered.append(zip_result)

    # Try encoding recovery
    if args.try_encodings:
        enc_results = try_encoding_recovery(args.file)
        all_recovered.extend(enc_results)

    # Default text recovery
    text_recovered = recover_text(args.file, args.min_length)
    if text_recovered:
        all_recovered.append("Printable text sequences:\n" + '\n'.join(text_recovered))

    if not all_recovered:
        print("No recoverable data found.")
        return

    print("Recovered data:")
    for item in all_recovered:
        print(item)
        print("-" * 50)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_recovered))
        print(f"Recovered data saved to {args.output}")

if __name__ == "__main__":
    main()
