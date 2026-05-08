# Data Recovery Project

This project provides tools for recovering data from corrupted or damaged files.

## Files

- `recover.py`: Main data recovery script that attempts to extract readable text from binary files.
- `data.py`: Sample corrupted file for testing.

## Usage

To recover text from a file:

```bash
python recover.py <file_path> [--min-length <int>] [--output <output_file>] [--try-zip] [--try-encodings]
```

Example:

```bash
python recover.py data.py --try-zip --try-encodings --output recovered.txt
```

## Features

- Extracts sequences of printable characters from binary files.
- Attempts to recover data from ZIP archives.
- Tries different text encodings (UTF-8, Latin-1, CP1252, ISO-8859-1).
- Configurable minimum length for text sequences.
- Option to save recovered text to a file.

## Future Improvements

- Support for more file formats (PDF, DOCX, etc.)
- Advanced encoding detection
- GUI interface
- Recovery of structured data (JSON, XML, etc.)
- Checksum verification and file integrity checks
- Batch processing for multiple files
