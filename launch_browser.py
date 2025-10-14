import webbrowser
import os
import sys
from pathlib import Path
import threading
import time
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler

def find_free_port():
    """Find a free port to run the server on"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def start_server():
    """Start a simple HTTP server"""
    server = None
    try:
        port = find_free_port()
        server = HTTPServer(('', port), SimpleHTTPRequestHandler)
        print(f"🌍 Server started at http://localhost:{port}")
        print("📁 Serving files from:", os.getcwd())
        print("❌ Press Ctrl+C to stop the server")
        
        # Open browser
        webbrowser.open(f"http://localhost:{port}/sample_bill_document.html")
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        if server:
            server.shutdown()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        if server:
            server.shutdown()

if __name__ == "__main__":
    print("🚀 Launching HTML Document Viewer")
    print("=" * 40)
    
    # Check if sample file exists
    if os.path.exists("sample_bill_document.html"):
        print("✅ Found sample HTML document")
        start_server()
    else:
        print("❌ Sample HTML document not found")
        print("Please run create_sample_html.py first")
        sys.exit(1)