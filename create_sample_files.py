#!/usr/bin/env python3
"""
Sample Excel File Generator for Infrastructure Billing System
Creates comprehensive test files with realistic data
"""

import pandas as pd
import os
from datetime import datetime

def create_sample_excel_file():
    """Create a sample Excel file with all required sheets"""
    
    # Ensure directory exists
    output_dir = 'Input_Files_for_tests'
    os.makedirs(output_dir, exist_ok=True)
    
    # Title Sheet Data
    title_data = {
        'Field': [
            'Project Name', 
            'Contractor Name', 
            'Agreement No', 
            'Work Order No', 
            'Location', 
            'Division', 
            'Estimated Cost', 
            'Start Date', 
            'Completion Date'
        ],
        'Value': [
            'Construction of Rural Road Network Phase II', 
            'ABC Construction Pvt. Ltd.', 
            'AGR/2024/001', 
            'WO/2024/RRN/001', 
            'Village Khemnagar, Udaipur', 
            'PWD Division Udaipur', 
            '5000000', 
            '01/01/2024', 
            '31/12/2024'
        ]
    }
    
    # Work Order Sheet Data
    work_order_data = {
        'S.No.': [1, 2, 3, 4, 5],
        'Item Description': [
            'Excavation in ordinary soil',
            'Providing and laying cement concrete 1:2:4',
            'Providing and laying bituminous concrete',
            'Construction of side drains',
            'Road marking and signage'
        ],
        'Unit': ['Cum', 'Cum', 'Cum', 'Rmt', 'Sqm'],
        'Quantity': [500, 200, 150, 1000, 50],
        'Rate': [150.0, 4500.0, 6500.0, 200.0, 250.0],
        'Amount': [75000, 900000, 975000, 200000, 12500]
    }
    
    # Bill Quantity Sheet Data
    bill_quantity_data = {
        'S.No.': [1, 2, 3, 4, 5],
        'Item Description': [
            'Excavation in ordinary soil',
            'Providing and laying cement concrete 1:2:4',
            'Providing and laying bituminous concrete',
            'Construction of side drains',
            'Road marking and signage'
        ],
        'Unit': ['Cum', 'Cum', 'Cum', 'Rmt', 'Sqm'],
        'Executed Quantity': [480, 195, 145, 980, 48],
        'Rate': [150.0, 4500.0, 6500.0, 200.0, 250.0],
        'Amount': [72000, 877500, 942500, 196000, 12000]
    }
    
    # Extra Items Sheet Data
    extra_items_data = {
        'S.No.': [1, 2],
        'Item Description': [
            'Additional culvert construction',
            'Extra retaining wall work'
        ],
        'Unit': ['Each', 'Sqm'],
        'Quantity': [2, 50],
        'Rate': [25000.0, 1200.0],
        'Amount': [50000, 60000]
    }
    
    # Create Excel file with multiple sheets
    filename = os.path.join(output_dir, 'sample_infrastructure_bill.xlsx')
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        pd.DataFrame(title_data).to_excel(writer, sheet_name='Title', index=False)
        pd.DataFrame(work_order_data).to_excel(writer, sheet_name='Work Order', index=False)
        pd.DataFrame(bill_quantity_data).to_excel(writer, sheet_name='Bill Quantity', index=False)
        pd.DataFrame(extra_items_data).to_excel(writer, sheet_name='Extra Items', index=False)
    
    print(f"✅ Sample file created: {filename}")
    return filename

def create_minimal_test_file():
    """Create a minimal test file for basic functionality testing"""
    
    output_dir = 'Input_Files_for_tests'
    os.makedirs(output_dir, exist_ok=True)
    
    # Minimal Title Data
    title_data = {
        'Field': ['Project Name', 'Contractor Name'],
        'Value': ['Test Road Project', 'Test Contractor Ltd.']
    }
    
    # Minimal Work Order Data
    work_order_data = {
        'S.No.': [1, 2],
        'Item Description': ['Excavation work', 'Concrete work'],
        'Unit': ['Cum', 'Cum'],
        'Quantity': [100, 50],
        'Rate': [150.0, 4500.0],
        'Amount': [15000, 225000]
    }
    
    # Minimal Bill Quantity Data
    bill_quantity_data = {
        'S.No.': [1, 2],
        'Item Description': ['Excavation work', 'Concrete work'],
        'Unit': ['Cum', 'Cum'],
        'Executed Quantity': [95, 48],
        'Rate': [150.0, 4500.0],
        'Amount': [14250, 216000]
    }
    
    filename = os.path.join(output_dir, 'minimal_test_file.xlsx')
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        pd.DataFrame(title_data).to_excel(writer, sheet_name='Title', index=False)
        pd.DataFrame(work_order_data).to_excel(writer, sheet_name='Work Order', index=False)
        pd.DataFrame(bill_quantity_data).to_excel(writer, sheet_name='Bill Quantity', index=False)
    
    print(f"✅ Minimal test file created: {filename}")
    return filename

if __name__ == "__main__":
    print("Creating sample Excel files for testing...")
    
    # Create comprehensive sample file
    comprehensive_file = create_sample_excel_file()
    
    # Create minimal test file
    minimal_file = create_minimal_test_file()
    
    print("\n📋 Sample files created successfully!")
    print(f"📁 Comprehensive sample: {comprehensive_file}")
    print(f"📁 Minimal test file: {minimal_file}")
    print("\n🎯 These files can be used to test the infrastructure billing system.")