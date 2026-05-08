#!/usr/bin/env python3
"""
Corrupted File Detector Module
Scans directories and identifies potentially corrupted files.
"""

import os
from pathlib import Path
from metadata_analyzer import analyze_file_header, get_file_metadata
from integrity_checker import check_file_corruption


def scan_directory(directory_path, recursive=True):
    """
    Scan a directory for potentially corrupted files.
    
    Args:
        directory_path (str): Path to directory to scan
        recursive (bool): Whether to scan subdirectories
        
    Returns:
        list: List of potentially corrupted files
    """
    corrupted_files = []
    
    try:
        path = Path(directory_path)
        
        if recursive:
            files = path.rglob('*')
        else:
            files = path.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                result = check_file_corruption(str(file_path))
                if result and result.get('likely_corrupted'):
                    corrupted_files.append({
                        'path': str(file_path),
                        'status': result,
                    })
    except Exception as e:
        print(f"Error scanning directory: {e}")
    
    return corrupted_files


def detect_corrupted_files(file_list):
    """
    Check a list of files for corruption.
    
    Args:
        file_list (list): List of file paths to check
        
    Returns:
        list: List of corrupted file information
    """
    corrupted = []
    
    for file_path in file_list:
        if os.path.isfile(file_path):
            result = check_file_corruption(file_path)
            if result and result.get('likely_corrupted'):
                corrupted.append({
                    'path': file_path,
                    'details': result,
                })
    
    return corrupted


def analyze_suspicious_file(file_path):
    """
    Perform detailed analysis on a suspicious file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: Detailed analysis results
    """
    try:
        metadata = get_file_metadata(file_path)
        header_analysis = analyze_file_header(file_path)
        corruption_check = check_file_corruption(file_path)
        
        return {
            'metadata': metadata,
            'header_analysis': header_analysis,
            'corruption_check': corruption_check,
        }
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None


def generate_corruption_report(files_data):
    """
    Generate a report on files and their corruption status.
    
    Args:
        files_data (list): List of file analysis data
        
    Returns:
        str: Formatted report
    """
    report = "=" * 60 + "\n"
    report += "CORRUPTION DETECTION REPORT\n"
    report += "=" * 60 + "\n\n"
    
    total_files = len(files_data)
    corrupted_count = sum(1 for f in files_data if f.get('likely_corrupted'))
    
    report += f"Total Files Scanned: {total_files}\n"
    report += f"Potentially Corrupted: {corrupted_count}\n"
    report += f"Corruption Rate: {(corrupted_count/total_files*100):.2f}%\n\n"
    
    report += "Corrupted Files:\n"
    report += "-" * 60 + "\n"
    
    for file_data in files_data:
        if file_data.get('likely_corrupted'):
            report += f"File: {file_data.get('path')}\n"
            report += f"  Size: {file_data.get('file_size')} bytes\n"
            report += f"  Readable: {file_data.get('is_readable')}\n"
            report += f"  Null Bytes: {file_data.get('null_byte_count')}\n\n"
    
    return report


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analysis = analyze_suspicious_file(sys.argv[1])
        if analysis:
            print("File Analysis:")
            print(analysis)
