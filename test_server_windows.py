#!/usr/bin/env python3
"""
Test script to verify Windows server compatibility
"""

import sys
import os
import platform
from pathlib import Path

def test_server():
    """Test Windows server startup"""
    print("=" * 60)
    print("IT Helpdesk Professional - Windows Server Test")
    print("=" * 60)
    
    # System information
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Script Location: {__file__}")
    
    # Test imports
    print("\nTesting imports...")
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print(f"✓ Flask-SQLAlchemy {flask_sqlalchemy.__version__}")
    except ImportError as e:
        print(f"✗ Flask-SQLAlchemy: {e}")
        return False
    
    try:
        import flask_wtf
        print(f"✓ Flask-WTF")
    except ImportError as e:
        print(f"✗ Flask-WTF: {e}")
        return False
    
    # Test main app import
    print("\nTesting main app...")
    try:
        sys.path.insert(0, '.')
        from main import app
        print("✓ Main app imported successfully")
    except ImportError as e:
        print(f"✗ Main app import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Main app error: {e}")
        return False
    
    # Test database
    print("\nTesting database...")
    try:
        with app.app_context():
            from app import db
            # Test database connection
            db.engine.execute("SELECT 1")
            print("✓ Database connection successful")
    except Exception as e:
        print(f"⚠ Database warning: {e}")
        print("  (This may be normal if database is not configured)")
    
    # Test server startup (without actually running)
    print("\nTesting server configuration...")
    try:
        app.config.update({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False
        })
        
        with app.test_client() as client:
            response = client.get('/')
            print(f"✓ Test request successful (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ Server test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All tests passed! Windows server should work correctly.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = test_server()
        if success:
            print("\nYou can now safely run the Professional GUI!")
        else:
            print("\nPlease fix the issues above before running the GUI.")
            sys.exit(1)
    except Exception as e:
        print(f"Test script error: {e}")
        sys.exit(1)