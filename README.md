# GTN Engineering IT Helpdesk System

A comprehensive Flask-based IT helpdesk management system designed for professional IT support operations. Features role-based access control, automatic system detection, ticket lifecycle management, and advanced reporting capabilities.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-v15+-blue.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-v5.3+-purple.svg)

## Features

### 🎯 Core Functionality
- **Role-Based Access Control**: Three user levels (Super Admin, Admin, User)
- **Ticket Management**: Complete lifecycle from creation to resolution
- **Image Upload Support**: Secure file attachment system for tickets
- **System Detection**: Automatic IP address and system name capture
- **Real-time Updates**: Live ticket status tracking and notifications
- **Comment System**: Collaborative ticket discussion and updates

### 📊 Advanced Features
- **Visual Reports Dashboard**: Charts and analytics with Chart.js
- **Excel Export**: Comprehensive ticket data export functionality
- **User Management**: Complete user administration system
- **Assignment System**: Intelligent ticket routing based on categories
- **Search & Filtering**: Advanced ticket filtering and search capabilities

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first Bootstrap 5 interface
- **Professional Styling**: Modern CSS with custom properties
- **Intuitive Navigation**: Role-based menu system
- **Interactive Elements**: Hover effects and smooth transitions
- **Accessibility**: WCAG compliant design patterns

### 🔧 Technical Features
- **Multi-Database Support**: PostgreSQL (primary), SQL Server, MySQL
- **Security**: CSRF protection, secure password hashing
- **Performance**: Connection pooling and optimized queries
- **Scalability**: Gunicorn WSGI server for production deployment

## System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **Database**: PostgreSQL 15+ (recommended), SQL Server, or MySQL
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Storage**: 100MB for application, additional space for database
- **Network**: Port 5000 for development, 80/443 for production

### Supported Platforms
- **Development**: Windows, macOS, Linux
- **Production**: Linux (Ubuntu 20.04+, CentOS 8+), Windows Server
- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd gtn-helpdesk-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
Set your database connection:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/gtn_helpdesk"
export SESSION_SECRET="your-secret-key-here"
```

### 4. Run Application
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Installation Guide

### Development Setup

1. **Install Python 3.11+**
   ```bash
   python --version  # Verify installation
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-wtf flask-login
   pip install werkzeug email-validator openpyxl psycopg2-binary
   pip install gunicorn pymysql pyodbc
   ```

4. **Configure Database**
   - PostgreSQL: See [PostgreSQL Setup Guide](README_PostgreSQL_Setup.md)
   - SQL Server: Configure connection string with pyodbc
   - MySQL: Configure connection string with PyMySQL

### Production Deployment

1. **Configure Environment Variables**
   ```bash
   export DATABASE_URL="your-production-database-url"
   export SESSION_SECRET="secure-production-secret"
   export FLASK_ENV="production"
   ```

2. **Start with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   ```

3. **Setup Reverse Proxy** (Nginx recommended)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

## Configuration

### Database Configuration

The system supports multiple database backends with automatic detection:

```python
# Priority order: PostgreSQL > SQL Server > MySQL
DATABASE_URL = "postgresql://user:pass@host:port/db"  # Primary
SQL_SERVER_URL = "mssql+pyodbc://user:pass@host:port/db?driver=..."
MYSQL_URL = "mysql+pymysql://user:pass@host:port/db"
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Primary database connection | None | Yes |
| `SESSION_SECRET` | Flask session secret key | None | Yes |
| `SQL_SERVER_HOST` | SQL Server hostname | None | No |
| `SQL_SERVER_DATABASE` | SQL Server database name | gtn_helpdesk | No |
| `MYSQL_URL` | MySQL connection URL | None | No |

### Application Settings

```python
# In app.py - customize as needed
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    },
    'WTF_CSRF_ENABLED': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024  # 16MB max file upload
})
```

## User Guide

### Default Login Credentials

#### Super Administrator
- **Username**: `superadmin`
- **Password**: `super123`
- **Capabilities**: Full system access, user management, reports

**⚠️ Important**: Change the default password immediately after installation and create your own admin and user accounts through the user management interface.

### User Roles & Permissions

| Feature | User | Admin | Super Admin |
|---------|------|-------|-------------|
| Create Tickets | ✅ | ✅ | ✅ |
| View Own Tickets | ✅ | ✅ | ✅ |
| View All Tickets | ❌ | ✅ | ✅ |
| Assign Tickets | ❌ | ✅ | ✅ |
| Upload Images | ✅ | ✅ | ✅ |
| View Uploaded Images | ❌ | ✅ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |
| Reports Dashboard | ❌ | ❌ | ✅ |
| Excel Export | ❌ | ❌ | ✅ |
| System Settings | ❌ | ❌ | ✅ |

### Creating Your First Ticket

1. **Login** as a regular user
2. **Navigate** to "New Ticket" 
3. **Fill out the form**:
   - Title: Descriptive summary
   - Description: Detailed problem description
   - Category: Hardware/Software
   - Priority: Low/Medium/High/Critical
   - System Name: Auto-detected or manual entry
   - Image Upload: Optional screenshot or photo attachment
4. **Submit** - Ticket number will be generated automatically

### Administrative Workflow

1. **Dashboard Overview**: View all tickets and statistics
2. **Ticket Management**: Assign tickets to appropriate administrators
3. **Status Updates**: Update ticket status as work progresses
4. **Comment System**: Add internal notes and user communication
5. **Resolution**: Mark tickets as resolved with solution details
6. **User Management**: Create and manage user accounts (Super Admin only)
7. **Reports & Analytics**: Generate reports and export data (Super Admin only)

## API Documentation

### Database Models

#### User Model
```python
class User(db.Model):
    id = Integer (Primary Key)
    username = String(80) (Unique)
    email = String(120) (Unique)
    password_hash = String(256)
    first_name = String(50)
    last_name = String(50)
    department = String(100)
    role = String(20)  # user, admin, super_admin
    is_admin = Boolean
    ip_address = String(45)
    system_name = String(100)
    created_at = DateTime
```

#### Ticket Model
```python
class Ticket(db.Model):
    id = Integer (Primary Key)
    title = String(200)
    description = Text
    category = String(50)  # Hardware, Software
    priority = String(20)  # Low, Medium, High, Critical
    status = String(20)    # Open, In Progress, Resolved, Closed
    user_id = Integer (Foreign Key)
    assigned_to = Integer (Foreign Key)
    user_name = String(100)  # Full name of ticket creator
    user_ip_address = String(45)  # IP address at ticket creation
    user_system_name = String(100)  # System name at ticket creation
    image_filename = String(255)  # Uploaded image filename (NEW)
    created_at = DateTime
    updated_at = DateTime
    resolved_at = DateTime
```

#### Comment Model
```python
class TicketComment(db.Model):
    id = Integer (Primary Key)
    ticket_id = Integer (Foreign Key)
    user_id = Integer (Foreign Key)
    comment = Text
    created_at = DateTime
```

### Key Routes

| Route | Method | Description | Access Level |
|-------|--------|-------------|--------------|
| `/` | GET | Homepage | Public |
| `/user-login` | GET/POST | User authentication | Public |
| `/admin-login` | GET/POST | Admin authentication | Public |
| `/user-dashboard` | GET | User ticket overview | User+ |
| `/admin-dashboard` | GET | Admin ticket management | Admin+ |
| `/super-admin-dashboard` | GET | System overview | Super Admin |
| `/create-ticket` | GET/POST | New ticket creation | User+ |
| `/ticket/<id>` | GET | Ticket details | Owner/Admin+ |
| `/reports-dashboard` | GET | Analytics dashboard | Super Admin |
| `/download-excel-report` | GET | Excel export | Super Admin |

## Advanced Features

### System Information Capture

The application automatically captures:
- **IP Address**: Real client IP (handles proxy forwarding)
- **System Name**: Operating system and browser detection
- **User Agent**: Browser and device information
- **Session Data**: Login time and activity tracking

### Intelligent Assignment System

- **Category-Based**: Routes tickets to specialized teams
- **Workload Balancing**: Distributes tickets evenly among admins
- **Priority Handling**: Escalates critical issues automatically
- **Department Matching**: Assigns based on user department

### Reporting & Analytics

- **Visual Charts**: Category, priority, and status breakdowns
- **Export Capabilities**: Excel files with complete ticket data
- **Performance Metrics**: Resolution times and response rates
- **Historical Data**: Trend analysis and reporting

### Security Features

- **Password Hashing**: Werkzeug secure password storage
- **CSRF Protection**: Form submission security
- **Session Management**: Secure user session handling
- **Input Validation**: WTForms data validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check database status
systemctl status postgresql  # Linux
net start postgresql-x64-16  # Windows

# Verify connection string
psql -U username -d database_name -h localhost
```

#### Application Won't Start
```bash
# Check Python version
python --version

# Verify dependencies
pip list | grep -E "(flask|sqlalchemy|wtf)"

# Check environment variables
echo $DATABASE_URL
echo $SESSION_SECRET
```

#### Permission Denied Errors
```bash
# Check file permissions
chmod 755 main.py
chmod 644 *.html *.css *.js

# Database permissions
GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk TO username;
```

### Performance Optimization

#### Database Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
```

#### Application Tuning
```python
# Configure connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'pool_recycle': 300,
    'pool_pre_ping': True,
    'max_overflow': 30
}
```

## Development

### Project Structure
```
gtn-helpdesk-system/
├── main.py                 # Application entry point
├── app.py                  # Flask app configuration
├── routes.py               # URL routing and views
├── models.py               # Database models
├── forms.py                # WTForms definitions
├── static/                 # CSS, JS, images
│   ├── style.css          # Custom styling
│   ├── script.js          # Client-side functionality
│   └── gtn_logo.jpg       # Company logo
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── user_dashboard.html # User interface
│   ├── admin_dashboard.html # Admin interface
│   └── ...
├── README.md              # This file
├── README_PostgreSQL_Setup.md # Database setup guide
└── requirements.txt       # Python dependencies
```

### Adding New Features

1. **Database Changes**: Update models.py and run migrations
2. **Forms**: Add new form classes in forms.py
3. **Routes**: Create new endpoints in routes.py
4. **Templates**: Design HTML interfaces in templates/
5. **Styling**: Update static/style.css for new components

### Code Style Guidelines

- **Python**: Follow PEP 8 standards
- **HTML**: Use semantic markup and proper indentation
- **CSS**: Use CSS custom properties and BEM methodology
- **JavaScript**: ES6+ features with proper error handling

## Deployment Options

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Systemd Service (Linux)
```ini
[Unit]
Description=GTN Helpdesk System
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/opt/gtn-helpdesk
Environment=DATABASE_URL=postgresql://...
Environment=SESSION_SECRET=...
ExecStart=/opt/gtn-helpdesk/venv/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Windows Service
Use NSSM (Non-Sucking Service Manager) or similar tools to run as Windows service.

## Support & Maintenance

### Backup Strategy
```bash
# Daily database backup
pg_dump -U username gtn_helpdesk > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/app
```

### Monitoring
- **Application Logs**: Check Flask application logs
- **Database Performance**: Monitor query execution times
- **System Resources**: CPU, memory, and disk usage
- **User Activity**: Login patterns and ticket creation rates

### Updates & Patches
1. **Test Environment**: Always test updates in staging
2. **Database Migration**: Use proper migration scripts
3. **Backup First**: Create full backup before updates
4. **Gradual Rollout**: Deploy to small user groups first

## License

This project is proprietary software developed for GTN Engineering (India) Ltd.

## Contact

For technical support or questions:
- **Internal Helpdesk**: Use this system to create tickets
- **IT Department**: Contact your organization's IT administrator
- **System Administrator**: Contact the Super Administrator for system-level issues

---

**GTN Engineering IT Helpdesk System**  
*Professional IT Support Management Solution*

Last Updated: June 23, 2025  
Version: 2.1.0