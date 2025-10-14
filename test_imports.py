"""
Test script to verify that all imports in streamlit_app.py work correctly
"""
import sys
from pathlib import Path

# Add src to Python path for imports
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

try:
    from excel_processor import ExcelProcessor
    print("✅ excel_processor import successful")
except ImportError as e:
    print(f"❌ excel_processor import failed: {e}")

try:
    from latex_generator import LaTeXGenerator
    print("✅ latex_generator import successful")
except ImportError as e:
    print(f"❌ latex_generator import failed: {e}")

try:
    from utils import validate_excel_file, get_timestamp, sanitize_filename
    print("✅ utils import successful")
except ImportError as e:
    print(f"❌ utils import failed: {e}")

print("Import test completed.")