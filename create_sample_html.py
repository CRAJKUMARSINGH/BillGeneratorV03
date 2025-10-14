import json
from pathlib import Path

# Create sample processed data
sample_data = {
    "title": {
        "project_name": "Sample Infrastructure Project",
        "contractor_name": "Sample Contractor Ltd",
        "work_order_no": "WO-2025-001",
        "location": "Sample Location",
        "agreement_no": "AG-2025-001"
    },
    "work_order": [
        {
            "serial_no": "1",
            "description": "Earthwork Excavation",
            "unit": "Cum",
            "quantity": 100.0,
            "rate": 500.0,
            "amount": 50000.0,
            "remark": "As per specifications"
        },
        {
            "serial_no": "2",
            "description": "Concrete Work M20",
            "unit": "Cum",
            "quantity": 50.0,
            "rate": 2500.0,
            "amount": 125000.0,
            "remark": "RCC work"
        }
    ],
    "bill_quantity": [
        {
            "serial_no": "1",
            "description": "Earthwork Excavation",
            "unit": "Cum",
            "quantity": 95.0,
            "rate": 500.0,
            "amount": 47500.0,
            "remark": "Executed quantity"
        },
        {
            "serial_no": "2",
            "description": "Concrete Work M20",
            "unit": "Cum",
            "quantity": 52.0,
            "rate": 2500.0,
            "amount": 130000.0,
            "remark": "Executed quantity"
        }
    ],
    "extra_items": [
        {
            "serial_no": "1",
            "description": "Additional Concrete Work",
            "unit": "Cum",
            "quantity": 5.0,
            "rate": 2600.0,
            "amount": 13000.0,
            "approval_ref": "APR-2025-001",
            "remark": "Extra work approved"
        }
    ],
    "totals": {
        "bill_quantity_total": 177500.0,
        "extra_items_total": 13000.0,
        "grand_total": 190500.0,
        "gst_rate": 18.0,
        "gst_amount": 34290.0,
        "total_with_gst": 224790.0,
        "net_payable": 224790.0
    }
}

# Save sample data
with open("sample_processed_data.json", "w") as f:
    json.dump(sample_data, f, indent=2)

print("Sample processed data saved to sample_processed_data.json")

# Create a simple HTML file for demonstration
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Bill Document</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .header { text-align: center; margin-bottom: 20px; }
        .total { font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Sample Infrastructure Project</h1>
        <h2>Contractor Bill</h2>
    </div>
    
    <table>
        <tr>
            <th>Item No.</th>
            <th>Description</th>
            <th>Unit</th>
            <th>Quantity</th>
            <th>Rate</th>
            <th>Amount</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Earthwork Excavation</td>
            <td>Cum</td>
            <td>95.00</td>
            <td>500.00</td>
            <td>47,500.00</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Concrete Work M20</td>
            <td>Cum</td>
            <td>52.00</td>
            <td>2,500.00</td>
            <td>130,000.00</td>
        </tr>
        <tr>
            <td colspan="5" class="total">Total:</td>
            <td class="total">177,500.00</td>
        </tr>
    </table>
    
    <p><strong>Generated on:</strong> October 14, 2025</p>
</body>
</html>
"""

with open("sample_bill_document.html", "w") as f:
    f.write(html_content)

print("Sample HTML document saved to sample_bill_document.html")
print("✅ Sample output files created successfully!")