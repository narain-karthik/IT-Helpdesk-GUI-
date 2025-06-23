
#!/usr/bin/env python3
"""
IT Helpdesk Professional - Enhanced GUI Launcher
Enterprise-grade desktop application for managing the IT Helpdesk system
For the latest professional version, use gui_launcher_professional.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import psutil
import requests
import os
import sys
import json
import time
from pathlib import Path
import webbrowser
from datetime import datetime

class HelpDeskLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IT Helpdesk Professional - Server Manager")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        # Set icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'static', 'app_icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Configuration file
        self.config_file = "helpdesk_config.json"
        self.server_process = None
        self.server_thread = None
        self.is_server_running = False
        
        # Professional color scheme
        self.colors = {
            'primary': '#2563eb',
            'primary_dark': '#1d4ed8',
            'secondary': '#64748b',
            'success': '#059669',
            'warning': '#d97706',
            'danger': '#dc2626',
            'light': '#f8fafc',
            'white': '#ffffff',
            'gray_100': '#f3f4f6',
            'gray_200': '#e5e7eb',
            'gray_300': '#d1d5db',
            'gray_600': '#4b5563',
            'gray_800': '#1f2937'
        }
        
        # Default configuration
        self.config = {
            "postgresql": {
                "host": "localhost",
                "port": "5432",
                "database": "it_helpdesk",
                "username": "postgres",
                "password": ""
            },
            "server": {
                "host": "0.0.0.0",
                "port": "5000"
            }
        }
        
        self.load_config()
        self.setup_styles()
        self.create_widgets()
        self.update_status()
        
    def setup_styles(self):
        """Setup professional ttk styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure notebook style
        self.style.configure('Professional.TNotebook', 
                            background=self.colors['white'],
                            borderwidth=0)
        self.style.configure('Professional.TNotebook.Tab',
                            padding=[20, 10],
                            background=self.colors['gray_100'],
                            foreground=self.colors['gray_800'],
                            font=('Segoe UI', 10, 'bold'))
        self.style.map('Professional.TNotebook.Tab',
                      background=[('selected', self.colors['primary']),
                                ('active', self.colors['gray_200'])],
                      foreground=[('selected', self.colors['white'])])
        
        # Configure button styles
        self.style.configure('Primary.TButton',
                            background=self.colors['primary'],
                            foreground=self.colors['white'],
                            font=('Segoe UI', 9, 'bold'),
                            padding=[15, 8])
        self.style.map('Primary.TButton',
                      background=[('active', self.colors['primary_dark'])])
        
        self.style.configure('Success.TButton',
                            background=self.colors['success'],
                            foreground=self.colors['white'],
                            font=('Segoe UI', 9, 'bold'),
                            padding=[15, 8])
        
        self.style.configure('Warning.TButton',
                            background=self.colors['warning'],
                            foreground=self.colors['white'],
                            font=('Segoe UI', 9, 'bold'),
                            padding=[15, 8])
        
        self.style.configure('Danger.TButton',
                            background=self.colors['danger'],
                            foreground=self.colors['white'],
                            font=('Segoe UI', 9, 'bold'),
                            padding=[15, 8])
        
        # Configure frame styles
        self.style.configure('Card.TFrame',
                            background=self.colors['white'],
                            relief='solid',
                            borderwidth=1)
        
        self.style.configure('Header.TFrame',
                            background=self.colors['primary'])
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except Exception as e:
                messagebox.showwarning("Config Warning", f"Could not load config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Config Error", f"Could not save config: {e}")
    
    def create_widgets(self):
        """Create the professional GUI interface"""
        # Create header
        self.create_header()
        
        # Main container
        main_container = ttk.Frame(self.root, style='Card.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(main_container, style='Professional.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_database_tab()
        self.create_server_tab()
        self.create_dashboard_tab()
        self.create_logs_tab()
        
        # Create status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create professional header"""
        header_frame = ttk.Frame(self.root, style='Header.TFrame', padding=20)
        header_frame.pack(fill=tk.X)
        
        # Logo and title section
        logo_frame = ttk.Frame(header_frame, style='Header.TFrame')
        logo_frame.pack(side=tk.LEFT)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="IT Helpdesk Professional", 
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['white'],
                              bg=self.colors['primary'])
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Server Management Console", 
                                 font=('Segoe UI', 10),
                                 fg=self.colors['gray_200'],
                                 bg=self.colors['primary'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Version info
        version_label = tk.Label(header_frame, 
                                text="v2.0", 
                                font=('Segoe UI', 9),
                                fg=self.colors['gray_200'],
                                bg=self.colors['primary'])
        version_label.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_database_tab(self):
        """Create enhanced database configuration interface"""
        self.db_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.db_frame, text="🗄️ Database Configuration")
        
        # Main container with padding
        container = ttk.Frame(self.db_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title section
        title_frame = ttk.Frame(container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="Database Configuration", 
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['gray_800'],
                              bg=self.colors['light'])
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame, 
                                 text="Configure your PostgreSQL database connection", 
                                 font=('Segoe UI', 10),
                                 fg=self.colors['gray_600'],
                                 bg=self.colors['light'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # PostgreSQL Configuration Card
        pg_card = ttk.LabelFrame(container, text=" PostgreSQL Settings ", 
                                style='Card.TFrame', padding=25)
        pg_card.pack(fill=tk.X, pady=(0, 20))
        
        # Database fields in a grid
        fields = [
            ("Host:", "host", "Database server hostname or IP address"),
            ("Port:", "port", "Database server port (default: 5432)"),
            ("Database Name:", "database", "Name of the database"),
            ("Username:", "username", "Database username"),
            ("Password:", "password", "Database password")
        ]
        
        self.db_vars = {}
        for i, (label_text, key, tooltip) in enumerate(fields):
            # Label
            label = ttk.Label(pg_card, text=label_text, font=('Segoe UI', 10, 'bold'))
            label.grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            # Entry
            if key == "password":
                var = tk.StringVar(value=self.config["postgresql"][key])
                entry = ttk.Entry(pg_card, textvariable=var, show="*", width=35, font=('Segoe UI', 10))
            else:
                var = tk.StringVar(value=self.config["postgresql"][key])
                entry = ttk.Entry(pg_card, textvariable=var, width=35, font=('Segoe UI', 10))
            
            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=8)
            self.db_vars[key] = var
            
            # Tooltip
            tooltip_label = ttk.Label(pg_card, text=tooltip, 
                                     font=('Segoe UI', 8), 
                                     foreground=self.colors['gray_600'])
            tooltip_label.grid(row=i, column=2, sticky=tk.W, padx=(10, 0), pady=8)
        
        # Buttons frame
        buttons_frame = ttk.Frame(pg_card)
        buttons_frame.grid(row=len(fields), column=0, columnspan=3, pady=(20, 0))
        
        # Test Connection Button
        test_btn = ttk.Button(buttons_frame, text="🔗 Test Connection", 
                             command=self.test_database_connection,
                             style='Primary.TButton')
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save Configuration Button
        save_btn = ttk.Button(buttons_frame, text="💾 Save Configuration", 
                             command=self.save_database_config,
                             style='Success.TButton')
        save_btn.pack(side=tk.LEFT)
        
        # Connection Status
        status_frame = ttk.Frame(container)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(status_frame, text="Connection Status:", 
                                font=('Segoe UI', 10, 'bold'))
        status_label.pack(side=tk.LEFT)
        
        self.db_status_var = tk.StringVar(value="Not tested")
        self.db_status_label = tk.Label(status_frame, textvariable=self.db_status_var,
                                       font=('Segoe UI', 10),
                                       fg=self.colors['gray_600'])
        self.db_status_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def create_server_tab(self):
        """Create enhanced server management interface"""
        self.server_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.server_frame, text="🖥️ Server Management")
        
        container = ttk.Frame(self.server_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(container, 
                              text="Server Management", 
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['gray_800'])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Server Configuration Card
        config_card = ttk.LabelFrame(container, text=" Server Configuration ", 
                                    style='Card.TFrame', padding=25)
        config_card.pack(fill=tk.X, pady=(0, 20))
        
        # Host and Port configuration
        config_grid = ttk.Frame(config_card)
        config_grid.pack(fill=tk.X)
        
        ttk.Label(config_grid, text="Host:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.server_host_var = tk.StringVar(value=self.config["server"]["host"])
        host_entry = ttk.Entry(config_grid, textvariable=self.server_host_var, 
                              width=20, font=('Segoe UI', 10))
        host_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(config_grid, text="Port:", font=('Segoe UI', 10, 'bold')).grid(
            row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.server_port_var = tk.StringVar(value=self.config["server"]["port"])
        port_entry = ttk.Entry(config_grid, textvariable=self.server_port_var, 
                              width=10, font=('Segoe UI', 10))
        port_entry.grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        
        # Server Controls Card
        controls_card = ttk.LabelFrame(container, text=" Server Controls ", 
                                      style='Card.TFrame', padding=25)
        controls_card.pack(fill=tk.X, pady=(0, 20))
        
        # Control Buttons
        button_frame = ttk.Frame(controls_card)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.start_btn = ttk.Button(button_frame, text="▶️ Start Server", 
                                   command=self.start_server,
                                   style='Success.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Stop Server", 
                                  command=self.stop_server, 
                                  state=tk.DISABLED,
                                  style='Danger.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.restart_btn = ttk.Button(button_frame, text="🔄 Restart Server", 
                                     command=self.restart_server, 
                                     state=tk.DISABLED,
                                     style='Warning.TButton')
        self.restart_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_browser_btn = ttk.Button(button_frame, text="🌐 Open in Browser", 
                                          command=self.open_browser, 
                                          state=tk.DISABLED,
                                          style='Primary.TButton')
        self.open_browser_btn.pack(side=tk.LEFT)
        
        # Server Status Display
        status_display = ttk.Frame(controls_card)
        status_display.pack(fill=tk.X)
        
        # Status indicator
        status_row1 = ttk.Frame(status_display)
        status_row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(status_row1, text="Status:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.server_status_var = tk.StringVar(value="Stopped")
        self.server_status_label = tk.Label(status_row1, textvariable=self.server_status_var, 
                                           font=('Segoe UI', 10, 'bold'),
                                           fg=self.colors['danger'])
        self.server_status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # URL display
        status_row2 = ttk.Frame(status_display)
        status_row2.pack(fill=tk.X)
        
        ttk.Label(status_row2, text="URL:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.url_var = tk.StringVar(value="Server not running")
        url_label = tk.Label(status_row2, textvariable=self.url_var, 
                            font=('Segoe UI', 10),
                            fg=self.colors['primary'], 
                            cursor="hand2")
        url_label.pack(side=tk.LEFT, padx=(10, 0))
        url_label.bind("<Button-1>", lambda e: self.open_browser())
    
    def create_dashboard_tab(self):
        """Create enhanced system dashboard"""
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="📊 Dashboard")
        
        container = ttk.Frame(self.dashboard_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(container, 
                              text="System Dashboard", 
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['gray_800'])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Statistics Card
        stats_card = ttk.LabelFrame(container, text=" System Statistics ", 
                                   style='Card.TFrame', padding=25)
        stats_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Stats display with better formatting
        self.stats_text = scrolledtext.ScrolledText(stats_card, 
                                                   height=15, 
                                                   font=('Consolas', 10),
                                                   bg=self.colors['gray_100'],
                                                   fg=self.colors['gray_800'],
                                                   relief='flat',
                                                   borderwidth=1)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        controls = ttk.Frame(container)
        controls.pack(fill=tk.X)
        
        refresh_btn = ttk.Button(controls, text="🔄 Refresh Statistics", 
                                command=self.refresh_dashboard,
                                style='Primary.TButton')
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_cb = ttk.Checkbutton(controls, 
                                         text="Auto-refresh every 30 seconds",
                                         variable=self.auto_refresh_var)
        auto_refresh_cb.pack(side=tk.LEFT)
        
        # Start auto-refresh
        self.schedule_refresh()
    
    def create_logs_tab(self):
        """Create enhanced logs viewing interface"""
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="📋 Server Logs")
        
        container = ttk.Frame(self.logs_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(container, 
                              text="Server Logs", 
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['gray_800'])
        title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Logs display
        logs_card = ttk.LabelFrame(container, text=" Real-time Server Logs ", 
                                  style='Card.TFrame', padding=25)
        logs_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.logs_text = scrolledtext.ScrolledText(logs_card, 
                                                  height=20, 
                                                  font=('Consolas', 9),
                                                  bg='#1e1e1e',
                                                  fg='#d4d4d4',
                                                  insertbackground='white',
                                                  relief='flat')
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = ttk.Frame(container)
        log_controls.pack(fill=tk.X)
        
        clear_btn = ttk.Button(log_controls, text="🗑️ Clear Logs", 
                              command=self.clear_logs,
                              style='Warning.TButton')
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = ttk.Button(log_controls, text="🔄 Refresh Logs", 
                                command=self.refresh_logs,
                                style='Primary.TButton')
        refresh_btn.pack(side=tk.LEFT)
    
    def create_status_bar(self):
        """Create professional status bar"""
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN, padding=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Current time
        self.time_var = tk.StringVar()
        time_label = ttk.Label(self.status_bar, textvariable=self.time_var, 
                              font=('Segoe UI', 9))
        time_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.status_bar, textvariable=self.status_var, 
                                font=('Segoe UI', 9))
        status_label.pack(side=tk.LEFT)
        
        # Update time
        self.update_time()
    
    def update_time(self):
        """Update status bar time"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(current_time)
        self.root.after(1000, self.update_time)
    
    def test_database_connection(self):
        """Test database connection with enhanced feedback"""
        self.status_var.set("Testing database connection...")
        try:
            # Update config with current values
            for key, var in self.db_vars.items():
                self.config["postgresql"][key] = var.get()
            
            # Create test connection string
            db_config = self.config["postgresql"]
            
            # Test with psycopg2
            import psycopg2
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['username'],
                password=db_config['password']
            )
            conn.close()
            
            self.db_status_var.set("✅ Connection successful")
            self.db_status_label.config(fg=self.colors['success'])
            self.status_var.set("Database connection successful")
            messagebox.showinfo("Success", "Database connection successful!")
            
        except ImportError:
            self.db_status_var.set("❌ psycopg2 not installed")
            self.db_status_label.config(fg=self.colors['danger'])
            self.status_var.set("Ready")
            messagebox.showerror("Error", "psycopg2 package not found. Install with: pip install psycopg2-binary")
        except Exception as e:
            self.db_status_var.set(f"❌ Connection failed")
            self.db_status_label.config(fg=self.colors['danger'])
            self.status_var.set("Ready")
            messagebox.showerror("Connection Error", f"Database connection failed:\n{str(e)}")
    
    def save_database_config(self):
        """Save database configuration with validation"""
        try:
            for key, var in self.db_vars.items():
                self.config["postgresql"][key] = var.get()
            
            self.config["server"]["host"] = self.server_host_var.get()
            self.config["server"]["port"] = self.server_port_var.get()
            
            self.save_config()
            self.status_var.set("Configuration saved successfully")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def start_server(self):
        """Start the Flask server with enhanced feedback"""
        try:
            self.save_database_config()
            
            # Set environment variables
            db_config = self.config["postgresql"]
            db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            
            env = os.environ.copy()
            env['DATABASE_URL'] = db_url
            env['FLASK_SECRET_KEY'] = 'it-helpdesk-secret-key-2025'
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self._run_server, args=(env,))
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Update UI
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.restart_btn.config(state=tk.NORMAL)
            self.open_browser_btn.config(state=tk.NORMAL)
            
            self.is_server_running = True
            self.server_status_var.set("Starting...")
            self.server_status_label.config(fg=self.colors['warning'])
            
            # Update URL
            url = f"http://{self.config['server']['host']}:{self.config['server']['port']}"
            self.url_var.set(url)
            
            self.status_var.set("Server starting...")
            self.log_message("🚀 Server starting...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            self.log_message(f"❌ Error starting server: {str(e)}")
    
    def _run_server(self, env):
        """Run the Flask server (internal method)"""
        try:
            host = self.config["server"]["host"]
            port = self.config["server"]["port"]
            
            # Start gunicorn server
            cmd = [
                sys.executable, "-m", "gunicorn",
                "--bind", f"{host}:{port}",
                "--reuse-port",
                "--reload",
                "main:app"
            ]
            
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1,
                universal_newlines=True
            )
            
            # Update status when server starts
            self.root.after(2000, lambda: self.server_status_var.set("Running"))
            self.root.after(2000, lambda: self.server_status_label.config(fg=self.colors['success']))
            self.root.after(2000, lambda: self.status_var.set("Server running successfully"))
            self.root.after(2000, lambda: self.log_message("✅ Server started successfully"))
            
            # Read server output
            for line in iter(self.server_process.stdout.readline, ''):
                if line:
                    self.root.after(0, lambda msg=line.strip(): self.log_message(msg))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Server error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Server Error", str(e)))
    
    def stop_server(self):
        """Stop the Flask server"""
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                self.server_process = None
            
            self.is_server_running = False
            
            # Update UI
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.restart_btn.config(state=tk.DISABLED)
            self.open_browser_btn.config(state=tk.DISABLED)
            
            self.server_status_var.set("Stopped")
            self.server_status_label.config(fg=self.colors['danger'])
            self.url_var.set("Server not running")
            
            self.status_var.set("Server stopped")
            self.log_message("⏹️ Server stopped")
            
        except subprocess.TimeoutExpired:
            self.server_process.kill()
            self.log_message("🔥 Server force stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop server: {str(e)}")
            self.log_message(f"❌ Error stopping server: {str(e)}")
    
    def restart_server(self):
        """Restart the Flask server"""
        self.log_message("🔄 Restarting server...")
        self.status_var.set("Restarting server...")
        self.stop_server()
        time.sleep(2)
        self.start_server()
    
    def open_browser(self):
        """Open the application in web browser"""
        if self.is_server_running:
            url = f"http://localhost:{self.config['server']['port']}"
            webbrowser.open(url)
            self.log_message(f"🌐 Opened browser: {url}")
            self.status_var.set(f"Opened browser: {url}")
        else:
            messagebox.showwarning("Warning", "Server is not running")
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics with enhanced display"""
        try:
            stats = []
            stats.append("=" * 60)
            stats.append(f"  IT HELPDESK SYSTEM DASHBOARD")
            stats.append(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            stats.append("=" * 60)
            stats.append("")
            
            # System information
            stats.append("🖥️  SYSTEM INFORMATION")
            stats.append("-" * 30)
            stats.append(f"   Python Version: {sys.version.split()[0]}")
            stats.append(f"   Platform: {sys.platform}")
            stats.append(f"   Working Directory: {os.getcwd()}")
            stats.append("")
            
            # Server status
            stats.append("🌐 SERVER STATUS")
            stats.append("-" * 30)
            if self.is_server_running:
                stats.append(f"   Status: ✅ RUNNING")
                stats.append(f"   Host: {self.config['server']['host']}")
                stats.append(f"   Port: {self.config['server']['port']}")
                stats.append(f"   URL: http://localhost:{self.config['server']['port']}")
                
                # Try to get server response
                try:
                    url = f"http://localhost:{self.config['server']['port']}"
                    response = requests.get(url, timeout=5)
                    stats.append(f"   Response Code: {response.status_code}")
                    stats.append(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
                except:
                    stats.append(f"   Response: ❌ Unable to connect")
            else:
                stats.append(f"   Status: ⏹️ STOPPED")
            stats.append("")
            
            # Database status
            stats.append("🗄️  DATABASE CONFIGURATION")
            stats.append("-" * 30)
            db_config = self.config["postgresql"]
            stats.append(f"   Host: {db_config['host']}")
            stats.append(f"   Port: {db_config['port']}")
            stats.append(f"   Database: {db_config['database']}")
            stats.append(f"   Username: {db_config['username']}")
            stats.append("")
            
            # System resources
            stats.append("📊 SYSTEM RESOURCES")
            stats.append("-" * 30)
            stats.append(f"   CPU Usage: {psutil.cpu_percent(interval=0.1):.1f}%")
            
            memory = psutil.virtual_memory()
            stats.append(f"   Memory Usage: {memory.percent:.1f}%")
            stats.append(f"   Memory Available: {memory.available / 1024 / 1024 / 1024:.1f} GB")
            
            disk = psutil.disk_usage('/')
            stats.append(f"   Disk Usage: {disk.percent:.1f}%")
            stats.append(f"   Disk Free: {disk.free / 1024 / 1024 / 1024:.1f} GB")
            stats.append("")
            
            # Process information
            if self.server_process:
                try:
                    process = psutil.Process(self.server_process.pid)
                    stats.append("⚙️  SERVER PROCESS")
                    stats.append("-" * 30)
                    stats.append(f"   PID: {self.server_process.pid}")
                    stats.append(f"   CPU: {process.cpu_percent():.1f}%")
                    stats.append(f"   Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
                    stats.append(f"   Status: {process.status()}")
                    stats.append(f"   Threads: {process.num_threads()}")
                except:
                    stats.append("⚙️  SERVER PROCESS: Information unavailable")
            else:
                stats.append("⚙️  SERVER PROCESS: Not running")
            
            stats.append("")
            stats.append("=" * 60)
            
            # Update display
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, "\n".join(stats))
            
            self.status_var.set("Dashboard refreshed")
            
        except Exception as e:
            self.log_message(f"❌ Error refreshing dashboard: {str(e)}")
    
    def schedule_refresh(self):
        """Schedule automatic dashboard refresh"""
        if self.auto_refresh_var.get():
            self.refresh_dashboard()
        
        # Schedule next refresh
        self.root.after(30000, self.schedule_refresh)  # 30 seconds
    
    def log_message(self, message):
        """Add message to logs with timestamp and emoji"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        
        # Limit log size
        lines = self.logs_text.get("1.0", tk.END).count('\n')
        if lines > 1000:
            self.logs_text.delete("1.0", "100.0")
    
    def clear_logs(self):
        """Clear the logs display"""
        self.logs_text.delete(1.0, tk.END)
        self.log_message("🗑️ Logs cleared")
    
    def refresh_logs(self):
        """Refresh logs display"""
        self.log_message("🔄 Logs refreshed")
    
    def update_status(self):
        """Update status indicators"""
        # Check if server is actually running
        if self.server_process and self.server_process.poll() is None:
            if not self.is_server_running:
                self.is_server_running = True
                self.server_status_var.set("Running")
                self.server_status_label.config(fg=self.colors['success'])
        else:
            if self.is_server_running:
                self.is_server_running = False
                self.server_status_var.set("Stopped")
                self.server_status_label.config(fg=self.colors['danger'])
                
                # Reset UI if server stopped unexpectedly
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.restart_btn.config(state=tk.DISABLED)
                self.open_browser_btn.config(state=tk.DISABLED)
                self.url_var.set("Server not running")
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_server_running:
            if messagebox.askokcancel("Quit Application", 
                                     "Server is currently running.\n\nDo you want to stop the server and quit?"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = HelpDeskLauncher()
    app.run()
