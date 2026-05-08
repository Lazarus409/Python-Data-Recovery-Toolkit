#!/usr/bin/env python3
"""
Metadata Analyzer Module
Analyzes and extracts metadata from files for recovery and analysis purposes.
"""

import os
from datetime import datetime


def get_file_metadata(file_path):
    """
    Extract metadata information from a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: Dictionary containing file metadata
    """
    try:
        stat_info = os.stat(file_path)
        metadata = {
            'file_name': os.path.basename(file_path),
            'file_path': os.path.abspath(file_path),
            'file_size': stat_info.st_size,
            'created_time': datetime.fromtimestamp(stat_info.st_ctime),
            'modified_time': datetime.fromtimestamp(stat_info.st_mtime),
            'accessed_time': datetime.fromtimestamp(stat_info.st_atime),
            'permissions': oct(stat_info.st_mode)[-3:],
            'is_file': os.path.isfile(file_path),
            'is_dir': os.path.isdir(file_path),
        }
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None


def analyze_file_header(file_path, bytes_to_read=512):
    """
    Analyze the file header to detect file type and corruption.
    
    Args:
        file_path (str): Path to the file
        bytes_to_read (int): Number of bytes to read from the beginning
        
    Returns:
        dict: File type information and hex header
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(bytes_to_read)
        
        hex_header = header.hex()
        
        # Common file signatures
        signatures = {
            'PDF': b'%PDF',
            'ZIP': b'PK\x03\x04',
            'JPEG': b'\xff\xd8\xff',
            'PNG': b'\x89PNG',
            'GIF': b'GIF8',
            'GZIP': b'\x1f\x8b',
            'EXE': b'MZ',
            'ELF': b'\x7fELF',
        }
        
        detected_types = []
        for file_type, sig in signatures.items():
            if header.startswith(sig):
                detected_types.append(file_type)
        
        return {
            'detected_types': detected_types if detected_types else ['Unknown'],
            'header_hex': hex_header[:64],  # First 32 bytes in hex
            'is_readable': all(b < 128 for b in header[:100] if header[:100])
        }
    except Exception as e:
        print(f"Error analyzing file header: {e}")
        return None


def compare_metadata(file_path1, file_path2):
    """
    Compare metadata of two files.
    
    Args:
        file_path1 (str): Path to first file
        file_path2 (str): Path to second file
        
    Returns:
        dict: Comparison results
    """
    meta1 = get_file_metadata(file_path1)
    meta2 = get_file_metadata(file_path2)
    
    if not meta1 or not meta2:
        return None
    
    return {
        'file1': meta1,
        'file2': meta2,
        'same_size': meta1['file_size'] == meta2['file_size'],
        'size_difference': abs(meta1['file_size'] - meta2['file_size']),
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        metadata = get_file_metadata(sys.argv[1])
        if metadata:
            for key, value in metadata.items():
                print(f"{key}: {value}")
