#!/usr/bin/env python3
"""
Simple HTTP server for local development.
Serves the learn-html-css application.

Usage:
    python3 server.py [port]

Default port: 8000
"""

import http.server
import socketserver
import sys
import os

# Get port from command line or use default
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set up handler
Handler = http.server.SimpleHTTPRequestHandler

# Enable CORS for development
class CORSRequestHandler(Handler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

# Start server
with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print("=" * 80)
    print("✅ Server running!")
    print("=" * 80)
    print(f"\n📂 Serving from: {os.getcwd()}")
    print(f"🌐 URL: http://localhost:{PORT}")
    print(f"\n👉 Open this URL in your browser: http://localhost:{PORT}")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 80)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped.")
        sys.exit(0)

