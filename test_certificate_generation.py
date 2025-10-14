#!/usr/bin/env python3
"""
Test script to verify that certificate templates are working correctly
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from document_generator import DocumentGenerator

# Create sample data
sample_data = {
    'title': {
        'project_name': 'Sample Infrastructure Project',
        'contractor_name': 'Sample Contractor Ltd',
        'measurement_officer': 'John Doe',
        'measurement_date': '30/04/2025',
        'measurement_book_page': '123',
        'measurement_book_no': 'MB-001',
        'officer_name': 'Jane Smith',
        'officer_designation': 'Project Manager',
        'authorising_officer_name': 'Robert Johnson',
        'authorising_officer_designation': 'Chief Engineer'
    },
    'totals': {
        'grand_total': 1120175,
        'net_payable': 952147,
        'total_deductions': 168028
    }
}

def test_certificate_generation():
    """Test that certificates are generated correctly"""
    print("Testing certificate generation...")
    
    # Create document generator
    generator = DocumentGenerator(sample_data)
    
    # Test Certificate II generation
    print("\n1. Testing Certificate II generation:")
    try:
        cert_ii = generator.generate_certificate_ii()
        print("   ✓ Certificate II generated successfully")
        print(f"   Length: {len(cert_ii)} characters")
        # Check if it contains expected elements
        if 'CERTIFICATE AND SIGNATURES' in cert_ii:
            print("   ✓ Contains correct title")
        else:
            print("   ✗ Missing title")
    except Exception as e:
        print(f"   ✗ Error generating Certificate II: {e}")
    
    # Test Certificate III generation
    print("\n2. Testing Certificate III generation:")
    try:
        cert_iii = generator.generate_certificate_iii()
        print("   ✓ Certificate III generated successfully")
        print(f"   Length: {len(cert_iii)} characters")
        # Check if it contains expected elements
        if 'MEMORANDUM OF PAYMENTS' in cert_iii:
            print("   ✓ Contains correct title")
        else:
            print("   ✗ Missing title")
    except Exception as e:
        print(f"   ✗ Error generating Certificate III: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_certificate_generation()