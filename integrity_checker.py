#!/usr/bin/env python3
"""
Integrity Checker Module
Verifies file integrity using checksums and various validation methods.
"""

import hashlib
import os


def calculate_hash(file_path, algorithm='sha256'):
    """
    Calculate the hash of a file.
    
    Args:
        file_path (str): Path to the file
        algorithm (str): Hash algorithm to use (md5, sha1, sha256, sha512)
        
    Returns:
        str: Hex digest of the file hash
    """
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return None


def verify_hash(file_path, expected_hash, algorithm='sha256'):
    """
    Verify if a file's hash matches the expected hash.
    
    Args:
        file_path (str): Path to the file
        expected_hash (str): Expected hash value
        algorithm (str): Hash algorithm used
        
    Returns:
        bool: True if hash matches, False otherwise
    """
    actual_hash = calculate_hash(file_path, algorithm)
    return actual_hash == expected_hash if actual_hash else False


def check_file_corruption(file_path):
    """
    Check for common signs of file corruption.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: Corruption indicators
    """
    try:
        file_size = os.path.getsize(file_path)
        
        # Try to read the file
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            readable = True
        except:
            readable = False
        
        # Check for null bytes which might indicate corruption
        null_byte_count = data.count(b'\x00') if readable else -1
        
        # Check entropy (simplified)
        entropy = -1
        if readable and len(data) > 0:
            from collections import Counter
            counts = Counter(data)
            total = len(data)
            entropy = sum(-(count/total) * (count/total).__hash__() for count in counts.values() if count > 0)
        
        return {
            'file_size': file_size,
            'is_readable': readable,
            'null_byte_count': null_byte_count,
            'likely_corrupted': not readable or (null_byte_count > file_size * 0.1 if null_byte_count > 0 else False),
        }
    except Exception as e:
        print(f"Error checking file corruption: {e}")
        return None


def compare_checksums(file_path1, file_path2, algorithm='sha256'):
    """
    Compare checksums of two files.
    
    Args:
        file_path1 (str): Path to first file
        file_path2 (str): Path to second file
        algorithm (str): Hash algorithm to use
        
    Returns:
        dict: Comparison results
    """
    hash1 = calculate_hash(file_path1, algorithm)
    hash2 = calculate_hash(file_path2, algorithm)
    
    if not hash1 or not hash2:
        return None
    
    return {
        'file1_hash': hash1,
        'file2_hash': hash2,
        'match': hash1 == hash2,
        'algorithm': algorithm,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        corruption_check = check_file_corruption(sys.argv[1])
        if corruption_check:
            for key, value in corruption_check.items():
                print(f"{key}: {value}")
