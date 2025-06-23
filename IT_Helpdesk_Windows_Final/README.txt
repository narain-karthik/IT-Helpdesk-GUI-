IT Helpdesk System - Windows Application

INSTALLATION:
1. Run "Install_IT_Helpdesk.bat" as Administrator
2. Desktop shortcut will be created automatically
3. Start Menu entry will be added

USAGE:
1. Double-click "IT Helpdesk" desktop shortcut
2. Configure PostgreSQL database in "Database Config" tab:
   - Host: Your PostgreSQL server (localhost for local)
   - Port: 5432 (default PostgreSQL port)
   - Database: Your database name
   - Username: Database username  
   - Password: Database password
3. Click "Test Connection" to verify settings
4. Go to "Server Management" tab
5. Click "Start Server" to launch the web application
6. Click "Open in Browser" to access the helpdesk

FEATURES:
- GUI database configuration interface
- Real-time server status monitoring
- Built-in web server management
- System dashboard with statistics
- Live server logs viewer
- One-click browser access

REQUIREMENTS:
- Windows 10/11
- Python 3.11+ (guided installation if missing)
- PostgreSQL database access
- 4GB RAM, 500MB disk space

FIRST TIME SETUP:
1. Ensure PostgreSQL is installed and running
2. Create a database for the helpdesk system
3. Note your database connection details
4. Launch IT Helpdesk and configure in the GUI
5. Default login: superadmin / superadmin123

TROUBLESHOOTING:
- If Python not found: Install from python.org with "Add to PATH"
- If database connection fails: Check PostgreSQL service is running
- If port in use: Change port in Server Management tab
- For help: See main README.md for detailed documentation

This application functions like traditional Windows software with
modern web-based helpdesk capabilities.