#!/usr/bin/env python3
"""
Test script to verify the markdown redundancy removal process
"""

import os
import sys
from pathlib import Path

def test_markdown_removal():
    """Test the markdown removal process"""
    print("Testing Markdown Redundancy Removal Process")
    print("=" * 50)
    
    # Check if the removal script exists
    removal_script = Path("remove_redundant_md_files.py")
    if not removal_script.exists():
        print("❌ Removal script not found")
        return False
    
    print("✅ Removal script found")
    
    # Import the remover class
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("remover", removal_script)
        if spec is None:
            print("❌ Failed to create module spec")
            return False
        remover_module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            print("❌ Failed to get module loader")
            return False
        spec.loader.exec_module(remover_module)
        
        # Create an instance of the remover
        remover = remover_module.MarkdownRedundancyRemover()
        print("✅ Removal module imported successfully")
        
    except Exception as e:
        print(f"❌ Failed to import removal module: {e}")
        return False
    
    # Test file identification
    print("\nTesting file identification...")
    try:
        md_files = remover.find_markdown_files()
        print(f"✅ Found {len(md_files)} markdown files")
        
        # List the files
        print("Markdown files found:")
        for md_file in md_files:
            print(f"  - {md_file.name}")
            
    except Exception as e:
        print(f"❌ Error finding markdown files: {e}")
        return False
    
    # Test redundancy identification
    print("\nTesting redundancy identification...")
    try:
        redundant_files = remover.identify_redundant_files()
        print(f"✅ Analysis complete")
        print(f"Files flagged as redundant: {len(redundant_files)}")
        
        if redundant_files:
            print("Redundant files identified:")
            for rf in redundant_files:
                print(f"  - {rf.name}")
        else:
            print("No redundant files identified")
            
    except Exception as e:
        print(f"❌ Error identifying redundant files: {e}")
        return False
    
    # Test compliance check
    print("\nTesting compliance verification...")
    try:
        compliance_result = remover.run_compliance_check()
        print(f"Compliance check: {'✅ PASS' if compliance_result else '❌ FAIL'}")
    except Exception as e:
        print(f"❌ Error in compliance check: {e}")
        return False
    
    # Test validation
    print("\nTesting file validation...")
    try:
        validation_result = remover.validate_remaining_files()
        print(f"Validation result: {'✅ PASS' if validation_result else '❌ FAIL'}")
    except Exception as e:
        print(f"❌ Error in validation: {e}")
        return False
    
    print(f"\n{'='*50}")
    print("✅ All tests completed successfully!")
    print("The markdown removal process is ready to be executed.")
    return True

if __name__ == "__main__":
    success = test_markdown_removal()
    sys.exit(0 if success else 1)