# GTN Engineering IT Helpdesk System

## Overview

The GTN Engineering IT Helpdesk System is a comprehensive Flask-based web application designed to manage IT support tickets within an organization. The system features role-based access control with three distinct user levels (Super Admin, Admin, and User), automatic system information capture, and a complete ticket lifecycle management system.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: Multi-database support with automatic detection
  - PostgreSQL: Primary production database (default)
  - SQL Server: Enterprise production database with pyodbc connector
  - MySQL: Alternative production database with PyMySQL connector
- **Authentication**: Session-based authentication with role-based access control
- **Server**: Gunicorn WSGI server for production deployment

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5.3.0 for responsive design
- **Icons**: Remix Icons for consistent iconography
- **JavaScript**: Vanilla JavaScript for client-side interactions

### Application Structure
```
├── main.py              # Application entry point
├── app.py               # Flask app configuration and initialization
├── routes.py            # URL routing and view functions
├── models.py            # Database models (User, Ticket, TicketComment)
├── forms.py             # WTForms form definitions
├── gui_launcher.py      # Windows GUI launcher application
├── templates/           # Jinja2 HTML templates
├── static/              # CSS, JavaScript, and static assets
└── GTN_Helpdesk_Windows/ # Windows deployment package
```

## Windows Desktop Application

### GUI Launcher Features
- **Database Configuration**: PostgreSQL connection setup with test functionality
- **Server Management**: Start/stop/restart web server with real-time status
- **System Dashboard**: Monitor server performance and system statistics
- **Log Viewer**: Real-time server log monitoring and management
- **Browser Integration**: Direct launch to web interface

### Windows Deployment Package
- Complete standalone package in `GTN_Helpdesk_Windows/`
- Automated installer with system requirement checks
- Desktop shortcut creation and Start Menu integration
- Requirements management and dependency installation
- Multiple launch options (batch file, Python direct)

### Installation Requirements
- Windows 10 or Windows 11
- Python 3.11+ (automatically checked and guided installation)
- PostgreSQL database access (local or remote)
- 4GB RAM minimum, 500MB disk space

## Key Components

### Database Models
1. **User Model**: Handles user authentication, profile information, and role management
2. **Ticket Model**: Manages support tickets with full lifecycle tracking
3. **TicketComment Model**: Enables comment system for ticket updates

### Role-Based Access Control
- **Super Admin**: Full system access, user management, ticket oversight
- **Admin**: Ticket management, assignment capabilities
- **User**: Ticket creation and personal ticket management

### Automatic System Detection
- IP address capture for user tracking
- System name detection for better support context
- Integration with ticket creation process

### Forms and Validation
- WTForms integration for secure form handling
- Comprehensive validation for all user inputs
- CSRF protection enabled

## Data Flow

1. **User Authentication**: Session-based login with role verification
2. **Ticket Creation**: Users submit tickets with automatic system info capture
3. **Ticket Assignment**: Admins can assign tickets based on category specialization
4. **Ticket Management**: Status updates, comments, and resolution tracking
5. **Reporting**: Excel export functionality for administrative oversight

## External Dependencies

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-WTF (form handling)
- Flask-Login (authentication)
- Werkzeug (WSGI utilities)
- Gunicorn (production server)
- email-validator (email validation)
- openpyxl (Excel export functionality)

### Frontend Dependencies
- Bootstrap 5.3.0 (CSS framework)
- Remix Icons (icon library)

### Development Dependencies
- SQLite (development database)
- PostgreSQL packages (production ready)

## Deployment Strategy

### Development Environment
- SQLite database for local development
- Flask development server with debug mode
- Hot reload enabled for rapid development

### Production Environment
- Gunicorn WSGI server with autoscale deployment
- PostgreSQL database support configured
- ProxyFix middleware for proper header handling
- Environment-based configuration management

### Container Configuration
- Replit configuration with multiple modules (web, python-3.11, nodejs-20)
- Nixpkgs for system dependencies (openssl, postgresql)
- Port configuration for external access

## Recent Changes

- **Login Pages Completely Redesigned**: Replaced complex split-screen layouts with clean, centered card designs featuring professional styling, better form layouts, and improved user experience
- **Updated README.md**: Added missing IT Helpdesk logo to documentation header for professional presentation
- **Project Cleanup**: Removed unwanted files including Python cache files, temporary files, and unused template variations
- **Windows Compatibility Fixed**: Resolved Windows server startup issues by replacing Gunicorn with Windows-compatible Flask server, created dedicated server_launcher.py for cross-platform compatibility
- **Professional Windows GUI Developed**: Created enterprise-grade Windows GUI launcher (gui_launcher_professional.py) with advanced features including system monitoring, security settings, backup management, and multi-database support
- **Enhanced User Interface**: Modernized all web templates with professional styling, improved header/footer design, and enterprise-grade visual elements  
- **Migration Completed**: Successfully migrated project from Replit Agent to Replit environment
- **Database Setup**: Created PostgreSQL database with proper environment variables
- **Complete Rebranding**: Removed all GTN references, renamed to "IT Helpdesk" throughout
- **Windows Package**: Created IT_Helpdesk_Complete_Windows.zip with GUI launcher and installer
- **Documentation Updated**: Comprehensive README.md with full A-Z usage instructions
- **File Cleanup**: Removed all temporary build files and unwanted development artifacts
- **Final Distribution**: Ready-to-deploy Windows package with user-friendly documentation
- **Logo Updated**: Replaced GTN logo with custom IT Helpdesk logo and branding
- **Final Cleanup**: Removed all cache files, logs, and development artifacts
- **Professional Documentation**: Enhanced README.md with enterprise-grade documentation standards

## User Preferences

- Requires Windows executable for distribution to end users
- Prefers GUI-based database configuration over command line
- Needs standalone application that can run on Windows without technical setup
- Prefers clean, simple login page designs over complex split-screen layouts
- Values professional presentation with proper logo placement in documentation

## Changelog

- June 23, 2025: Migration to Replit completed with PostgreSQL database integration  
- June 23, 2025: Windows GUI launcher and deployment package created
- June 23, 2025: Updated README.md with professional formatting, removed test user credentials, kept only Super Admin default login
- June 23, 2025: Created comprehensive database schema documentation (README_Database_Schema.md)
- June 23, 2025: Cleaned up project by removing unwanted files (__pycache__, attached_assets) and added .gitignore
- June 23, 2025: Removed Network and Other categories from all pages (admin dashboard, super admin dashboard, reports dashboard)
- June 23, 2025: Fixed ticket creation 500 errors by creating uploads directory and improving file handling
- June 23, 2025: Fixed dashboard 500 errors by adding image_filename column to database
- June 23, 2025: Successfully migrated from Replit Agent to Replit environment with enhanced image upload functionality
- June 23, 2025: Added secure image upload system for tickets with admin-only viewing capabilities
- June 23, 2025: Updated ticket categories to Hardware and Software only (removed Network and Other)
- June 23, 2025: Enhanced database schema with image_filename field for ticket attachments
- June 23, 2025: Updated documentation in README.md and README_PostgreSQL_Setup.md
- June 22, 2025: Completed migration to Replit environment with PostgreSQL as primary database
- June 22, 2025: Enhanced system name detection to capture accurate client information per ticket
- June 22, 2025: Implemented modern UI/UX design with CSS custom properties and professional styling
- June 22, 2025: Created comprehensive PostgreSQL setup guide for Windows systems
- June 22, 2025: Added Microsoft SQL Server integration with comprehensive setup guide and connection testing
- June 22, 2025: Updated comprehensive README.md with complete setup instructions, user guides, and troubleshooting
- June 22, 2025: Added Reports Dashboard with visual analytics, assignment editing functionality, and MySQL support
- June 21, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.