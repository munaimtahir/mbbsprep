#!/usr/bin/env python
"""
Quick test to start server and demonstrate the new subjects management page
"""
import subprocess
import webbrowser
import time
import os

def start_server_and_test():
    """Start the Django server and open the subjects page"""
    print("🚀 Starting Django development server...")
    
    # Change to the project directory
    os.chdir(r'd:\PMC\Exam-Prep-Site')
    
    try:
        # Start the server
        server_process = subprocess.Popen(
            ['python', 'manage.py', 'runserver'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        print("🌐 Opening subjects management page...")
        print("📍 URL: http://localhost:8000/staff/subjects/")
        
        # Open the browser
        webbrowser.open('http://localhost:8000/staff/subjects/')
        
        print("\n✅ Server started successfully!")
        print("📝 Features available:")
        print("  • Modern table-based subjects listing")
        print("  • Add/Edit subjects with modal forms")
        print("  • Archive/Restore functionality")
        print("  • Inline topic management")
        print("  • Search and filtering")
        print("  • Professional color scheme matching admin panel")
        print("  • Fully responsive design")
        print("  • AJAX-powered interactions")
        print("\n🎨 Color scheme:")
        print("  • Primary: #0057A3 (Blue)")
        print("  • Archive: #FF7043 (Orange)")
        print("  • Active Status: #43B284 (Green)")
        print("  • Background: #F5F7FA (Light gray)")
        print("\n⌨️  Press Ctrl+C to stop the server")
        
        # Wait for user to stop
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    start_server_and_test()
