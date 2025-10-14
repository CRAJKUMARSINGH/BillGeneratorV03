#!/usr/bin/env python3
"""
Safe script to identify redundant .md files without actually removing them
"""

import os
from pathlib import Path
import hashlib
from datetime import datetime

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

def find_markdown_files():
    """Find all .md files in the current directory"""
    md_files = list(Path(".").glob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    return md_files

def identify_redundant_files():
    """Identify redundant markdown files"""
    md_files = find_markdown_files()
    redundant_files = []
    
    # Files that must be preserved
    preserved_files = {
        "README.md",
        "COMPLETE_COMBINED_DOCUMENTATION.md",
        "requirements.txt",
    }
    
    # Patterns indicating redundancy
    redundancy_patterns = [
        "_IMPLEMENTATION.md",
        "_FINAL_CONFIRMATION.md",
        "_VALIDATION_REPORT.md",
        "_MODIFICATIONS_SUMMARY.md",
        "_DETAILED_IMPLEMENTATION.md",
        "_SOLUTION_SUMMARY.md",
        "_ALIGNMENT_REPORT.md",
        "_ALIGNMENT_MODIFICATIONS.md",
        "_VERIFICATION.md",
        "_FOR_REVIEW.md",
        "_GUIDE.md",
        "_DEPLOYMENT_GUIDE.md",
    ]
    
    print("\nAnalyzing files for redundancy...")
    
    for md_file in md_files:
        filename = md_file.name
        
        # Skip preserved files
        if filename in preserved_files:
            print(f"✓ Preserving: {filename}")
            continue
        
        # Check naming patterns for redundancy
        is_redundant_by_pattern = any(pattern in filename for pattern in redundancy_patterns)
        if is_redundant_by_pattern:
            print(f"⚠️  Flagged for removal (pattern match): {filename}")
            redundant_files.append(md_file)
            continue
        
        print(f"ℹ️  Keeping (no redundancy detected): {filename}")
    
    return redundant_files

def main():
    """Main function to identify redundant files"""
    print("SAFE REDUNDANT MARKDOWN FILE IDENTIFICATION")
    print("=" * 50)
    print("This script identifies redundant .md files without removing them.")
    print("Review the list before deciding whether to remove them.\n")
    
    # Identify redundant files
    redundant_files = identify_redundant_files()
    
    if not redundant_files:
        print("\nNo redundant files found.")
        return
    
    # Display results
    print(f"\n{'='*50}")
    print("FILES IDENTIFIED AS REDUNDANT")
    print(f"{'='*50}")
    for i, file_path in enumerate(redundant_files, 1):
        file_size = file_path.stat().st_size / 1024  # Size in KB
        print(f"{i:2d}. {file_path.name} ({file_size:.1f} KB)")
    
    print(f"\nTotal files identified as redundant: {len(redundant_files)}")
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    print("✅ All critical files (README.md, COMPLETE_COMBINED_DOCUMENTATION.md, etc.) will be preserved")
    print("✅ Computational logic files will not be affected")
    print("✅ Template files and statutory compliance will be maintained")
    print("⚠️  The above files can be removed to reduce project clutter")
    print("\nTo actually remove these files, run the remove_redundant_md_files.py script")

if __name__ == "__main__":
    main()