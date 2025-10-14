"""
Batch Performance Test for Bill Generator V03
Tests response time and performance with multiple batch runs
"""

import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from enhanced_bill_generator import EnhancedBillGenerator

def create_test_data():
    """Create comprehensive test data for batch testing"""
    return {
        'title': {
            'project_name': 'Government Office Complex Construction',
            'contractor_name': 'ABC Construction Ltd.',
            'agreement_no': 'GOV/2024/001',
            'work_order_no': 'WO/2024/001',
            'bill_no': 'BILL/2024/001',
            'date': '2024-09-22'
        },
        'extra_items': [
            {
                'serial_no': 1,
                'description': 'Additional electrical wiring for conference hall',
                'unit': 'Mtr',
                'quantity': 150.0,
                'rate': 125.50,
                'amount': 18825.00,
                'remarks': 'As per site requirement'
            },
            {
                'serial_no': 2,
                'description': 'Extra marble flooring in entrance lobby',
                'unit': 'Sqm',
                'quantity': 45.0,
                'rate': 850.00,
                'amount': 38250.00,
                'remarks': 'Premium grade marble'
            },
            {
                'serial_no': 3,
                'description': 'Additional HVAC ducting for server room',
                'unit': 'Mtr',
                'quantity': 75.0,
                'rate': 275.00,
                'amount': 20625.00,
                'remarks': 'Fire-resistant ducting'
            },
            {
                'serial_no': 4,
                'description': 'Extra waterproofing for basement',
                'unit': 'Sqm',
                'quantity': 200.0,
                'rate': 450.00,
                'amount': 90000.00,
                'remarks': 'Waterproof membrane'
            },
            {
                'serial_no': 5,
                'description': 'Additional security system installation',
                'unit': 'Nos',
                'quantity': 10.0,
                'rate': 5000.00,
                'amount': 50000.00,
                'remarks': 'CCTV and access control'
            }
        ],
        'totals': {
            'grand_total': 217700.00,
            'tender_premium_percent': 0.10,
            'tender_premium': 21770.00,
            'total_executed': 239470.00
        }
    }

def run_batch_test(batch_number, test_data):
    """Run a single batch test"""
    print(f"\n🚀 BATCH {batch_number} - Starting Test")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # Initialize generator with batch-specific output directory
        output_dir = f"batch_test_outputs_{batch_number}"
        generator = EnhancedBillGenerator(output_dir)
        
        # Generate extra items package
        result = generator.generate_extra_items_package(
            extra_items_data=test_data,
            project_name=test_data['title']['project_name'],
            contractor_name=test_data['title']['contractor_name']
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Analyze results
        if result['errors']:
            print(f"❌ Batch {batch_number} - Errors found:")
            for error in result['errors']:
                print(f"   - {error}")
            return False, response_time, 0, 0
        
        # Count generated files
        html_files = len(result.get('html_files', {}))
        pdf_files = len(result.get('pdf_files', {}))
        
        print(f"✅ Batch {batch_number} - SUCCESS")
        print(f"⏱️  Response Time: {response_time:.2f} seconds")
        print(f"📄 HTML Files: {html_files}")
        print(f"📑 PDF Files: {pdf_files}")
        print(f"📁 Output Directory: {output_dir}")
        
        return True, response_time, html_files, pdf_files
        
    except Exception as e:
        end_time = time.time()
        response_time = end_time - start_time
        print(f"❌ Batch {batch_number} - FAILED: {str(e)}")
        return False, response_time, 0, 0

def main():
    """Main batch testing function"""
    print("🔬 BATCH PERFORMANCE TEST - BILL GENERATOR V03")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Objective: Test response time and performance with 3 batch runs")
    print("=" * 60)
    
    # Create test data
    test_data = create_test_data()
    print(f"📊 Test Data: {len(test_data['extra_items'])} extra items")
    print(f"💰 Total Value: ₹{test_data['totals']['grand_total']:,.2f}")
    
    # Run 3 batch tests
    results = []
    total_start_time = time.time()
    
    for batch_num in range(1, 4):
        success, response_time, html_files, pdf_files = run_batch_test(batch_num, test_data)
        results.append({
            'batch': batch_num,
            'success': success,
            'response_time': response_time,
            'html_files': html_files,
            'pdf_files': pdf_files
        })
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    # Calculate statistics
    successful_batches = sum(1 for r in results if r['success'])
    response_times = [r['response_time'] for r in results if r['success']]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    
    total_html_files = sum(r['html_files'] for r in results)
    total_pdf_files = sum(r['pdf_files'] for r in results)
    
    # Display comprehensive results
    print("\n" + "=" * 60)
    print("📊 BATCH TEST RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"🎯 Total Batches: 3")
    print(f"✅ Successful: {successful_batches}")
    print(f"❌ Failed: {3 - successful_batches}")
    print(f"📈 Success Rate: {(successful_batches/3)*100:.1f}%")
    
    print(f"\n⏱️  RESPONSE TIME ANALYSIS:")
    print(f"   Average: {avg_response_time:.2f} seconds")
    print(f"   Fastest: {min_response_time:.2f} seconds")
    print(f"   Slowest: {max_response_time:.2f} seconds")
    print(f"   Total Time: {total_time:.2f} seconds")
    
    print(f"\n📄 FILE GENERATION:")
    print(f"   HTML Files: {total_html_files}")
    print(f"   PDF Files: {total_pdf_files}")
    print(f"   Total Files: {total_html_files + total_pdf_files}")
    
    # Performance assessment
    print(f"\n🏆 PERFORMANCE ASSESSMENT:")
    if successful_batches == 3:
        if avg_response_time < 5.0:
            print("   🌟 EXCELLENT: All batches successful, fast response times")
        elif avg_response_time < 10.0:
            print("   ✅ GOOD: All batches successful, acceptable response times")
        else:
            print("   ⚠️  ACCEPTABLE: All batches successful, but slower response times")
    elif successful_batches >= 2:
        print("   ⚠️  PARTIAL: Most batches successful, some issues detected")
    else:
        print("   ❌ POOR: Multiple batch failures, significant issues")
    
    # Detailed batch results
    print(f"\n📋 DETAILED BATCH RESULTS:")
    for result in results:
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        print(f"   Batch {result['batch']}: {status} - {result['response_time']:.2f}s")
    
    print("\n" + "=" * 60)
    print("🎯 BATCH TEST COMPLETED")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    results = main()
