# Python Data Recovery Toolkit

A comprehensive toolkit for recovering, analyzing, and verifying data from corrupted or damaged files.

## Files

- `file_recovery.py`: Main data recovery script that extracts readable text from binary files. Supports ZIP recovery and multiple encoding attempts.
- `metadata_analyzer.py`: Extracts and analyzes file metadata, file headers, and file type detection.
- `integrity_checker.py`: Verifies file integrity using checksums (MD5, SHA1, SHA256, SHA512) and detects corruption signs.
- `corrupted_file_detector.py`: Scans directories to identify potentially corrupted files with detailed analysis reports.
- `requirements.txt`: Project dependencies and optional packages.

## Usage

### File Recovery

To recover text from a file:

```bash
python file_recovery.py <file_path> [--min-length <int>] [--output <output_file>] [--try-zip] [--try-encodings]
```

Example:

```bash
python file_recovery.py corrupted_file.bin --try-zip --try-encodings --output recovered.txt
```

### Metadata Analysis

Analyze file metadata:

```bash
python -c "from metadata_analyzer import get_file_metadata; import json; print(json.dumps(get_file_metadata('your_file.bin'), indent=2, default=str))"
```

### Integrity Checking

Verify file integrity:

```bash
python -c "from integrity_checker import calculate_hash; print(calculate_hash('your_file.bin'))"
```

### Corruption Detection

Scan directory for corrupted files:

```bash
python -c "from corrupted_file_detector import scan_directory; results = scan_directory('.', recursive=True); print(f'Found {len(results)} potentially corrupted files')"
```

## Features

### File Recovery

- Extracts sequences of printable characters from binary files
- Attempts to recover data from ZIP archives
- Tries different text encodings (UTF-8, Latin-1, CP1252, ISO-8859-1)
- Configurable minimum length for text sequences
- Option to save recovered text to a file

### Metadata Analysis

- File header analysis and file type detection
- File signature verification
- Metadata extraction (size, timestamps, permissions)
- File comparison utilities

### Integrity Checking

- Multiple hash algorithm support (MD5, SHA1, SHA256, SHA512)
- Hash verification
- Corruption detection and analysis
- Checksum comparison between files

### Corruption Detection

- Directory scanning with recursive option
- Corruption probability analysis
- Null byte detection
- Detailed file analysis reports
- Batch file corruption checking

## Installation

No external dependencies required. All modules use Python standard library.

For optional functionality (future):

```bash
pip install -r requirements.txt
```

## Future Improvements

- Support for more file formats (PDF, DOCX, etc.)
- Advanced encoding detection
- GUI interface
- Recovery of structured data (JSON, XML, etc.)
- Batch processing for multiple files
- Integration with file system recovery tools
- Machine learning-based file type detection
