# IT Helpdesk System

A comprehensive web-based IT support ticket management system with GUI launcher for Windows deployment.

## Overview

The IT Helpdesk System is a modern Flask-based web application designed for managing IT support tickets in organizations. It features role-based access control, automatic system detection, complete ticket lifecycle management, and includes a Windows GUI launcher for easy deployment.

## Quick Start

### For Windows Users
1. Download `IT_Helpdesk_Complete_Windows.zip`
2. Extract and run `Install_IT_Helpdesk.bat` as Administrator
3. Use the desktop shortcut to launch the application
4. Configure your database and start the server through the GUI

### For Developers/Linux Users
1. Clone or download the project
2. Install Python 3.11+ and PostgreSQL
3. Run: `pip install -r requirements.txt`
4. Start: `python main.py`

## System Features

### Multi-Role Access Control
- **Super Admin**: Complete system management, user administration, all ticket access
- **Admin**: Ticket management, assignment capabilities, department oversight  
- **User**: Create tickets, view personal tickets, update profile information

### Advanced Ticket Management
- **Complete Lifecycle**: Open → In Progress → Resolved → Closed workflow
- **Priority System**: Low, Medium, High, Critical with visual indicators
- **Department Categories**: Organized by IT, HR, Finance, Operations, etc.
- **Comment System**: Real-time updates and communication on tickets
- **File Attachments**: Support for documentation and screenshots
- **Auto-Detection**: Captures user IP address and system information

### Reporting & Analytics
- **Dashboard Metrics**: Visual charts and statistics
- **Performance Tracking**: User and department analytics
- **Export Options**: Generate reports in Excel format
- **Real-time Monitoring**: Live ticket status updates

### Database Support
- **PostgreSQL**: Primary production database (recommended)
- **MySQL**: Alternative database option
- **SQL Server**: Enterprise integration support
- **Automatic Detection**: Configures based on connection string

## Installation Methods

### Method 1: Windows GUI Application (Recommended for End Users)

**System Requirements:**
- Windows 10 or Windows 11
- Python 3.11+ (automatically guided installation)
- PostgreSQL database access
- 4GB RAM, 500MB disk space

**Installation Steps:**
1. Download `IT_Helpdesk_Complete_Windows.zip` from releases
2. Extract the ZIP file to a folder
3. Right-click `Install_IT_Helpdesk.bat` and select "Run as Administrator"
4. Follow the installation prompts
5. Desktop shortcut "IT Helpdesk" will be created

**Usage:**
1. Double-click the "IT Helpdesk" desktop shortcut
2. Configure PostgreSQL connection in the "Database Config" tab:
   - Host: Your PostgreSQL server (e.g., localhost)
   - Port: Usually 5432
   - Database: Your database name
   - Username: Database username
   - Password: Database password
3. Click "Test Connection" to verify settings
4. Go to "Server Management" tab and click "Start Server"
5. Click "Open in Browser" to access the helpdesk

### Method 2: Development Setup

**Prerequisites:**
```bash
# Install Python 3.11+
python --version

# Install PostgreSQL
# Windows: Download from postgresql.org
# Ubuntu: sudo apt install postgresql postgresql-contrib
# macOS: brew install postgresql
```

**Installation:**
```bash
# Clone/download the project
cd it-helpdesk

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL example)
export DATABASE_URL="postgresql://username:password@localhost:5432/it_helpdesk"

# Initialize database
python -c "from app import app, db; from models import *; app.app_context().push(); db.create_all()"

# Run application
python main.py
```

**Access the application at:** `http://localhost:5000`

### Method 3: Production Deployment

**Environment Variables:**
```bash
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
export SESSION_SECRET="your-secure-random-secret-key"
export FLASK_ENV="production"
```

**Using Gunicorn:**
```bash
# Install gunicorn
pip install gunicorn

# Start production server
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

**Using Docker (optional):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## Database Configuration

### PostgreSQL (Recommended)
```bash
# Create database
createdb it_helpdesk

# Connection string
DATABASE_URL="postgresql://username:password@localhost:5432/it_helpdesk"
```

### MySQL Alternative
```bash
# Connection string
DATABASE_URL="mysql://username:password@localhost:3306/it_helpdesk"
```

### SQL Server Enterprise
```bash
# Connection string
DATABASE_URL="mssql://username:password@server:1433/it_helpdesk"
```

## Default Login Credentials

**Super Admin Access:**
- Username: `superadmin`
- Password: `superadmin123`

> **Important**: Change these credentials immediately after first login for security

## User Guide

### For End Users

**Creating a Ticket:**
1. Login with your user credentials
2. Click "Create New Ticket"
3. Fill in the ticket details:
   - Title: Brief description of the issue
   - Department: Select appropriate department
   - Priority: Choose urgency level
   - Description: Detailed explanation
   - Attachments: Upload files if needed
4. Submit the ticket

**Tracking Your Tickets:**
- View all your tickets on the user dashboard
- Check status updates and comments
- Add additional information via comments
- Receive notifications on status changes

### For Administrators

**Managing Tickets:**
1. Access admin dashboard for ticket overview
2. Assign tickets to appropriate staff
3. Update ticket status and priority
4. Add comments and resolutions
5. Generate reports and analytics

**User Management:**
1. Create new user accounts
2. Assign roles and permissions
3. Manage department assignments
4. Monitor user activity

### For Super Administrators

**System Management:**
1. Complete user and admin management
2. System configuration and settings
3. Database administration access
4. Security and audit controls

## API Endpoints

### Authentication
- `POST /login` - User authentication
- `POST /admin/login` - Admin authentication
- `GET /logout` - Session logout

### Ticket Management
- `GET /tickets` - List user tickets
- `POST /tickets` - Create new ticket
- `GET /ticket/<id>` - View ticket details
- `PUT /ticket/<id>` - Update ticket
- `POST /ticket/<id>/comment` - Add comment

### Administration
- `GET /admin/dashboard` - Admin overview
- `GET /admin/tickets` - All tickets management
- `POST /admin/users` - Create user
- `GET /admin/reports` - Generate reports

## File Structure

```
it-helpdesk/
├── main.py                      # Application entry point
├── app.py                       # Flask configuration
├── routes.py                    # URL routing and views
├── models.py                    # Database models
├── forms.py                     # WTForms definitions
├── gui_launcher.py              # Windows GUI launcher
├── requirements.txt             # Python dependencies
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── index.html              # Homepage
│   ├── user_login.html         # User login
│   ├── admin_login.html        # Admin login
│   ├── user_dashboard.html     # User dashboard
│   ├── admin_dashboard.html    # Admin dashboard
│   ├── create_ticket.html      # Ticket creation
│   └── ...                     # Other templates
├── static/                      # Static assets
│   ├── style.css               # Stylesheet
│   ├── script.js               # JavaScript
│   ├── favicon.ico             # Site icon
│   └── uploads/                # File uploads
└── IT_Helpdesk_Windows_Final/   # Windows deployment package
    ├── IT_Helpdesk.bat         # Windows launcher
    ├── Install_IT_Helpdesk.bat # Installer script
    └── README.txt              # Windows user guide
```

## Security Features

- **Session Management**: Secure cookie-based authentication
- **CSRF Protection**: Form security against cross-site attacks
- **Input Validation**: Comprehensive data sanitization
- **SQL Injection Prevention**: ORM-based database queries
- **Role-Based Access**: Granular permission controls
- **File Upload Security**: Type and size validation

## Troubleshooting

### Common Issues

**Database Connection Errors:**
- Verify PostgreSQL is running
- Check connection credentials
- Ensure database exists
- Confirm network connectivity

**Python Import Errors:**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Find process using port 5000
netstat -tulpn | grep 5000
# Kill the process
kill -9 <process_id>
```

**Windows GUI Issues:**
- Ensure Python is installed and in PATH
- Run `python --version` in Command Prompt
- Reinstall dependencies with `pip install -r requirements.txt`

### Performance Optimization

**Database Indexing:**
```sql
-- Add indexes for better performance
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_created_date ON tickets(created_date);
```

**Caching Configuration:**
```python
# Add to app.py for production
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

## Support

For technical support:
- Check the troubleshooting section above
- Review the database setup guide
- Contact your system administrator
- Submit a ticket through the system itself

## License

This software is provided for internal organizational use. See LICENSE file for details.

## Version History

- **v2.0** - Added Windows GUI launcher, removed GTN branding
- **v1.5** - Enhanced security features and database support
- **v1.0** - Initial release with core helpdesk functionality