#!/usr/bin/env python3
"""
Quick server startup script for testing the completed CSS/JS separation implementation.
"""

import subprocess
import sys
import os

def start_server():
    print("🚀 Starting Django Development Server")
    print("📋 Testing Complete CSS/JS Separation Implementation")
    print("=" * 60)
    print()
    print("🔍 What to test:")
    print("   • MCQ List: http://127.0.0.1:8000/staff/questions/")
    print("   • Add MCQ: http://127.0.0.1:8000/staff/questions/add/")
    print("   • Bulk Upload: http://127.0.0.1:8000/staff/questions/bulk-upload/")
    print("   • Edit MCQ: Click any edit button from the list")
    print()
    print("✅ All pages now use:")
    print("   • External CSS files (no inline styles)")
    print("   • External JS files (no inline scripts)")
    print("   • Event delegation (no inline event handlers)")
    print()
    print("🧪 Test these interactions:")
    print("   • Bulk actions (select MCQs and use bulk buttons)")
    print("   • Add/remove options in add/edit forms")
    print("   • File upload drag & drop")
    print("   • Toggle status and delete buttons")
    print("   • Format guide toggle")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n✅ Server stopped. CSS/JS separation testing complete!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == '__main__':
    start_server()
