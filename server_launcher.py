#!/usr/bin/env python3
"""
Windows-compatible server launcher for IT Helpdesk Professional
This module provides Windows-compatible server startup functionality
"""

import sys
import os
import platform
from pathlib import Path

def run_server(host="0.0.0.0", port=5000, debug=False):
    """
    Run the IT Helpdesk server with Windows compatibility
    """
    try:
        # Set UTF-8 encoding for Windows
        if platform.system() == "Windows":
            import locale
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except:
                try:
                    locale.setlocale(locale.LC_ALL, 'C.UTF-8')
                except:
                    pass  # Use default locale if UTF-8 not available
        
        # Ensure we're in the correct directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Add current directory to Python path
        if str(script_dir) not in sys.path:
            sys.path.insert(0, str(script_dir))
        
        # Import the Flask app
        from main import app
        
        print("Starting IT Helpdesk Professional Server", flush=True)
        print(f"Host: {host}", flush=True)
        print(f"Port: {port}", flush=True)
        print(f"Debug Mode: {debug}", flush=True)
        print(f"Platform: {platform.system()} {platform.release()}", flush=True)
        print(f"Working Directory: {os.getcwd()}", flush=True)
        print("=" * 50, flush=True)
        
        # Configure Flask app for Windows
        app.config.update({
            'SEND_FILE_MAX_AGE_DEFAULT': 0 if debug else 31536000,
            'TEMPLATES_AUTO_RELOAD': debug,
            'EXPLAIN_TEMPLATE_LOADING': debug
        })
        
        # Run the Flask development server
        print("Server starting...", flush=True)
        app.run(
            host=host,
            port=int(port),
            debug=debug,
            threaded=True,
            use_reloader=debug,
            use_debugger=debug
        )
        
    except ImportError as e:
        print(f"Import Error: {e}", flush=True)
        print("Please ensure all dependencies are installed:", flush=True)
        print("pip install flask flask-sqlalchemy flask-wtf flask-login", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"Server Error: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="IT Helpdesk Professional Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    run_server(args.host, args.port, args.debug)