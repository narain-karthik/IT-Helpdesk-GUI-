# PostgreSQL Setup Guide for Windows
**GTN Engineering IT Helpdesk System**

This guide will help you set up PostgreSQL on your Windows PC and configure it for the GTN Engineering IT Helpdesk System.

## Table of Contents
1. [Download and Install PostgreSQL](#1-download-and-install-postgresql)
2. [Configure PostgreSQL](#2-configure-postgresql)
3. [Create Database and User](#3-create-database-and-user)
4. [Set Up Database Tables](#4-set-up-database-tables)
5. [Configure Application Connection](#5-configure-application-connection)
6. [Test the Connection](#6-test-the-connection)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Download and Install PostgreSQL

### Step 1.1: Download PostgreSQL
1. Visit the official PostgreSQL website: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Click on "Download the installer"
3. Download PostgreSQL 15 or later (recommended: PostgreSQL 16)
4. Choose the Windows x86-64 version for 64-bit systems

### Step 1.2: Install PostgreSQL
1. Run the downloaded installer (`postgresql-16.x-windows-x64.exe`)
2. Follow the installation wizard:
   - **Installation Directory**: Keep default (`C:\Program Files\PostgreSQL\16`)
   - **Data Directory**: Keep default (`C:\Program Files\PostgreSQL\16\data`)
   - **Password**: Choose a strong password for the `postgres` user (remember this!)
   - **Port**: Keep default (5432)
   - **Locale**: Keep default
3. **Important**: Uncheck "Stack Builder" at the end (not needed)
4. Complete the installation

---

## 2. Configure PostgreSQL

### Step 2.1: Add PostgreSQL to PATH
1. Open **System Properties** → **Advanced** → **Environment Variables**
2. In **System Variables**, find and edit `PATH`
3. Add: `C:\Program Files\PostgreSQL\16\bin`
4. Click **OK** to save

### Step 2.2: Test PostgreSQL Installation
1. Open **Command Prompt** as Administrator
2. Type: `psql --version`
3. You should see: `psql (PostgreSQL) 16.x`

---

## 3. Create Database and User

### Step 3.1: Connect to PostgreSQL
1. Open **Command Prompt**
2. Connect as the postgres superuser:
   ```cmd
   psql -U postgres -h localhost
   ```
3. Enter the password you set during installation

### Step 3.2: Create Database
Run these SQL commands in the PostgreSQL prompt:

```sql
-- Create database for the helpdesk system
CREATE DATABASE gtn_helpdesk
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Create application user
CREATE USER gtn_user WITH
    LOGIN
    SUPERUSER
    INHERIT
    CREATEDB
    CREATEROLE
    REPLICATION
    PASSWORD 'gtn_password_2024';

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk TO gtn_user;
```

### Step 3.3: Verify Database Creation
```sql
-- List all databases
\l

-- Connect to the new database
\c gtn_helpdesk

-- Exit PostgreSQL
\q
```

---

## 4. Set Up Database Tables

### Step 4.1: Database Schema
The application will automatically create these tables when first run:

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    is_admin BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    system_name VARCHAR(100),
    profile_image VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tickets Table
```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,  -- Hardware, Software (Network and Other removed)
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Open',
    user_name VARCHAR(100) NOT NULL,
    user_ip_address VARCHAR(45),
    user_system_name VARCHAR(100),
    image_filename VARCHAR(255),  -- NEW: For uploaded image attachments
    user_id INTEGER NOT NULL REFERENCES users(id),
    assigned_to INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);
```

#### Ticket Comments Table
```sql
CREATE TABLE ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 4.2: New Features (Updated Schema)
The latest version includes image upload functionality:

- **Image Upload**: Users can attach screenshots and images to tickets
- **Secure Storage**: Images are stored in `static/uploads/` directory
- **Admin Access**: Only admins and super admins can view uploaded images
- **File Types**: Supports JPG, JPEG, PNG, and GIF formats
- **Category Changes**: Removed "Network" and "Other" categories, now only "Hardware" and "Software"

---

## 5. Configure Application Connection

### Step 5.1: Environment Variables
Set these environment variables on your Windows system:

1. Open **System Properties** → **Advanced** → **Environment Variables**
2. In **System Variables**, add these new variables:

```
Variable Name: DATABASE_URL
Variable Value: postgresql://gtn_user:gtn_password_2024@localhost:5432/gtn_helpdesk

Variable Name: SESSION_SECRET
Variable Value: your-secret-key-here-change-this-in-production
```

### Step 5.2: Alternative Configuration
If environment variables don't work, you can also set these in your application:

```python
# In app.py, replace the database URI with:
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://gtn_user:gtn_password_2024@localhost:5432/gtn_helpdesk"
```

---

## 6. Test the Connection

### Step 6.1: Test Database Connection
1. Open **Command Prompt**
2. Test connection with the application user:
   ```cmd
   psql -U gtn_user -d gtn_helpdesk -h localhost
   ```
3. If successful, you'll see:
   ```
   gtn_helpdesk=#
   ```

### Step 6.2: Test Application
1. Start your Flask application
2. Check that it connects without errors
3. Visit the application in your browser
4. Try creating a test ticket to verify database functionality

---

## 7. Troubleshooting

### Problem: "psql: command not found"
**Solution**: PostgreSQL bin directory not in PATH
1. Add `C:\Program Files\PostgreSQL\16\bin` to your PATH environment variable
2. Restart Command Prompt

### Problem: "Connection refused"
**Solutions**:
1. **Check if PostgreSQL is running**:
   - Open **Services** (services.msc)
   - Find "postgresql-x64-16"
   - Ensure it's "Running"
   - If not, right-click → Start

2. **Check port availability**:
   ```cmd
   netstat -an | findstr :5432
   ```

### Problem: "Authentication failed"
**Solutions**:
1. **Reset postgres password**:
   - Stop PostgreSQL service
   - Edit `pg_hba.conf` file (in `C:\Program Files\PostgreSQL\16\data\`)
   - Change `md5` to `trust` temporarily
   - Restart PostgreSQL
   - Reset password, then change back to `md5`

2. **Check pg_hba.conf settings**:
   ```
   # Add this line for local connections:
   host    all             all             127.0.0.1/32           md5
   ```

### Problem: "Database does not exist"
**Solution**: Create the database manually:
```sql
psql -U postgres
CREATE DATABASE gtn_helpdesk;
```

### Problem: Application can't connect
**Solutions**:
1. **Verify connection string format**:
   ```
   postgresql://username:password@host:port/database
   ```

2. **Check firewall settings**:
   - Ensure PostgreSQL port 5432 is not blocked
   - Add exception for PostgreSQL in Windows Firewall

3. **Verify user permissions**:
   ```sql
   -- Connect as postgres user
   GRANT ALL PRIVILEGES ON DATABASE gtn_helpdesk TO gtn_user;
   GRANT ALL ON ALL TABLES IN SCHEMA public TO gtn_user;
   GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO gtn_user;
   ```

---

## Additional Configuration

### Enable Remote Connections (Optional)
If you need to access the database from other computers:

1. **Edit postgresql.conf**:
   ```
   listen_addresses = '*'
   ```

2. **Edit pg_hba.conf**:
   ```
   host    all             all             0.0.0.0/0               md5
   ```

3. **Restart PostgreSQL service**

### Performance Tuning (Optional)
For better performance, edit `postgresql.conf`:

```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.7
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
```

---

## Default Login Credentials

After first setup, use these default accounts:

### Super Admin
- **Username**: `superadmin`
- **Password**: `super123`
- **Role**: Super Administrator (full access)

### Test Admin Users
- **Username**: `yuvaraj` / Password: `admin123`
- **Username**: `jayachandran` / Password: `admin123`
- **Username**: `narainkarthik` / Password: `admin123`

### Test Regular User
- **Username**: `testuser` / Password: `user123`

**Important**: Change these default passwords immediately after first login!

---

## Security Recommendations

1. **Change default passwords** immediately
2. **Use strong passwords** (minimum 12 characters)
3. **Enable SSL/TLS** for production
4. **Regular backups**:
   ```cmd
   pg_dump -U gtn_user gtn_helpdesk > backup.sql
   ```
5. **Keep PostgreSQL updated**
6. **Monitor database logs** regularly

---

## Support

If you encounter issues not covered in this guide:
1. Check PostgreSQL logs in: `C:\Program Files\PostgreSQL\16\data\log\`
2. Consult PostgreSQL official documentation
3. Contact your system administrator

---

**Last Updated**: June 22, 2025  
**Compatible with**: PostgreSQL 15, 16+ on Windows 10/11