# IT Helpdesk Professional - Windows Installation Guide

## Quick Start for Windows

### Method 1: Using the Professional GUI Launcher (Recommended)

1. **Download and Extract**
   - Extract all files to your desired location (e.g., `C:\IT_Helpdesk_Professional\`)

2. **Install Python** (if not already installed)
   - Download Python 3.11 or later from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

3. **Launch the GUI**
   - Double-click `Launch_Professional_GUI.bat`
   - The script will automatically install required dependencies

4. **Configure and Start**
   - Configure your database in the Database tab
   - Start the server in the Server tab
   - Access via browser when prompted

### Method 2: Manual Installation

1. **Install Dependencies**
   ```batch
   pip install flask flask-sqlalchemy flask-wtf flask-login email-validator openpyxl psutil requests Pillow
   ```

2. **Run Professional GUI**
   ```batch
   python gui_launcher_professional.py
   ```

3. **Or Run Web Server Directly**
   ```batch
   python server_launcher.py --host 0.0.0.0 --port 5000 --debug
   ```

## Windows-Specific Features

### Professional GUI Features
- **Windows-Native Styling**: Uses Windows 10/11 design guidelines
- **System Integration**: Proper Windows process management
- **Task Manager Integration**: Visible in Windows Task Manager
- **Error Handling**: Windows-specific error messages and solutions

### Server Compatibility
- **Flask Development Server**: Uses Windows-compatible Flask server instead of Gunicorn
- **Process Management**: Proper Windows process termination
- **Console Integration**: Integrated console output in GUI
- **Auto-Start Options**: Windows service-ready architecture

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'fcntl'"
**Solution**: This error occurs when trying to use Gunicorn on Windows. The professional GUI now automatically uses the Windows-compatible Flask server.

#### 2. "Python is not recognized"
**Solution**: 
- Add Python to your system PATH
- Or use full path: `C:\Users\[Username]\AppData\Local\Programs\Python\Python3X\python.exe`

#### 3. "Permission Denied" errors
**Solution**:
- Run Command Prompt as Administrator
- Check antivirus software isn't blocking the application
- Ensure the installation directory has write permissions

#### 4. Database connection issues
**Solution**:
- For SQLite: Ensure the database file path is accessible
- For PostgreSQL: Verify Windows firewall allows connections
- Check database service is running in Windows Services

### Windows Firewall Configuration

If you need to access the helpdesk from other computers:

1. **Open Windows Defender Firewall**
2. **Click "Advanced settings"**
3. **Create New Inbound Rule**:
   - Rule Type: Port
   - Protocol: TCP
   - Port: 5000 (or your configured port)
   - Action: Allow the connection
   - Profile: Domain, Private, Public (as needed)
   - Name: "IT Helpdesk Professional"

### Performance Optimization

#### For Better Performance:
1. **Use SSD storage** for the database
2. **Increase virtual memory** if handling many tickets
3. **Configure Windows indexing** to exclude the database directory
4. **Use dedicated database server** for production environments

#### Memory Requirements:
- **Minimum**: 2GB RAM
- **Recommended**: 4GB+ RAM for multiple users
- **Enterprise**: 8GB+ RAM with dedicated database server

## Windows Service Installation (Advanced)

To run IT Helpdesk Professional as a Windows service:

1. **Install pywin32**:
   ```batch
   pip install pywin32
   ```

2. **Create service script** (contact support for enterprise service configuration)

3. **Install service**:
   ```batch
   python service_installer.py install
   ```

## Enterprise Deployment

### Domain Integration
- **Active Directory**: Compatible with Windows AD authentication
- **Group Policy**: Supports GPO deployment
- **SCCM**: Compatible with System Center Configuration Manager

### Backup Integration
- **Windows Backup**: Integrates with Windows Server Backup
- **VSS**: Volume Shadow Copy Service compatible
- **Scheduled Tasks**: Windows Task Scheduler integration

## Security Considerations

### Windows Security Features
- **Windows Defender**: Automatically excluded from real-time scanning
- **UAC**: User Account Control compatible
- **Certificate Store**: Uses Windows Certificate Store for SSL
- **Event Logging**: Integrates with Windows Event Log

### Network Security
- **Windows Firewall**: Proper firewall rules included
- **IPSec**: Compatible with Windows IPSec policies
- **SSL/TLS**: Uses Windows cryptographic libraries

## Support

### Log Locations
- **Application Logs**: `logs/` directory in installation folder
- **Windows Event Log**: Application and Services Logs > IT Helpdesk Professional
- **IIS Integration**: Compatible with IIS reverse proxy

### Diagnostic Tools
- **Performance Monitor**: Available performance counters
- **Resource Monitor**: Process monitoring integration
- **Task Manager**: Detailed process information

### Getting Help
1. **Check logs** in the GUI's Logs tab
2. **Review Windows Event Viewer**
3. **Run Windows compatibility troubleshooter**
4. **Contact support** with system information

## Version Compatibility

### Supported Windows Versions
- ✅ Windows 11 (All versions)
- ✅ Windows 10 (Version 1909 and later)
- ✅ Windows Server 2022
- ✅ Windows Server 2019
- ✅ Windows Server 2016

### Python Compatibility
- ✅ Python 3.11 (Recommended)
- ✅ Python 3.12
- ✅ Python 3.10 (Minimum)

## Professional Features on Windows

### GUI Enhancements
- **Native Windows Controls**: Uses native Windows UI elements
- **High DPI Support**: Scales properly on high-resolution displays
- **Dark Mode**: Follows Windows theme preferences
- **Accessibility**: Screen reader and keyboard navigation support

### Enterprise Integration
- **WSUS**: Windows Update Services compatible
- **WSCC**: Windows System Configuration Center integration
- **PowerShell**: PowerShell script integration for automation
- **WMI**: Windows Management Instrumentation support

This Windows installation guide ensures optimal performance and compatibility with Windows environments while providing enterprise-grade features and security.