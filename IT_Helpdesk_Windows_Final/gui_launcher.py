#!/usr/bin/env python3
"""
IT Helpdesk - GUI Launcher
Desktop application for managing the IT Helpdesk system with database configuration
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
        self.root.title("IT Helpdesk - Server Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configuration file
        self.config_file = "helpdesk_config.json"
        self.server_process = None
        self.server_thread = None
        self.is_server_running = False
        
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
                "host": "localhost",
                "port": "5000"
            }
        }
        
        self.load_config()
        self.create_widgets()
        self.update_status()
        
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
        """Create the GUI interface"""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Database Configuration Tab
        self.db_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.db_frame, text="Database Config")
        self.create_database_tab()
        
        # Server Management Tab
        self.server_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.server_frame, text="Server Management")
        self.create_server_tab()
        
        # Dashboard Tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.create_dashboard_tab()
        
        # Logs Tab
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="Logs")
        self.create_logs_tab()
    
    def create_database_tab(self):
        """Create database configuration interface"""
        # Title
        title_label = ttk.Label(self.db_frame, text="Database Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # PostgreSQL Configuration Frame
        pg_frame = ttk.LabelFrame(self.db_frame, text="PostgreSQL Settings", padding=10)
        pg_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Database fields
        fields = [
            ("Host:", "host"),
            ("Port:", "port"),
            ("Database Name:", "database"),
            ("Username:", "username"),
            ("Password:", "password")
        ]
        
        self.db_vars = {}
        for i, (label_text, key) in enumerate(fields):
            ttk.Label(pg_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if key == "password":
                var = tk.StringVar(value=self.config["postgresql"][key])
                entry = ttk.Entry(pg_frame, textvariable=var, show="*", width=30)
            else:
                var = tk.StringVar(value=self.config["postgresql"][key])
                entry = ttk.Entry(pg_frame, textvariable=var, width=30)
            
            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
            self.db_vars[key] = var
        
        # Test Connection Button
        test_btn = ttk.Button(pg_frame, text="Test Connection", 
                             command=self.test_database_connection)
        test_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Connection Status
        self.db_status_var = tk.StringVar(value="Not tested")
        status_label = ttk.Label(pg_frame, textvariable=self.db_status_var)
        status_label.grid(row=len(fields)+1, column=0, columnspan=2, pady=5)
        
        # Save Configuration Button
        save_btn = ttk.Button(self.db_frame, text="Save Configuration", 
                             command=self.save_database_config)
        save_btn.pack(pady=10)
    
    def create_server_tab(self):
        """Create server management interface"""
        # Title
        title_label = ttk.Label(self.server_frame, text="Server Management", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Server Configuration Frame
        server_config_frame = ttk.LabelFrame(self.server_frame, text="Server Settings", padding=10)
        server_config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Host and Port
        ttk.Label(server_config_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.server_host_var = tk.StringVar(value=self.config["server"]["host"])
        ttk.Entry(server_config_frame, textvariable=self.server_host_var, width=20).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(server_config_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.server_port_var = tk.StringVar(value=self.config["server"]["port"])
        ttk.Entry(server_config_frame, textvariable=self.server_port_var, width=10).grid(
            row=0, column=3, sticky=tk.W, padx=10, pady=5)
        
        # Server Controls Frame
        controls_frame = ttk.LabelFrame(self.server_frame, text="Server Controls", padding=10)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Control Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(button_frame, text="Start Server", 
                                   command=self.start_server)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Server", 
                                  command=self.stop_server, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.restart_btn = ttk.Button(button_frame, text="Restart Server", 
                                     command=self.restart_server, state=tk.DISABLED)
        self.restart_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_browser_btn = ttk.Button(button_frame, text="Open in Browser", 
                                          command=self.open_browser, state=tk.DISABLED)
        self.open_browser_btn.pack(side=tk.LEFT, padx=5)
        
        # Server Status
        status_frame = ttk.Frame(controls_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.server_status_var = tk.StringVar(value="Stopped")
        status_label = ttk.Label(status_frame, textvariable=self.server_status_var, 
                                foreground="red")
        status_label.pack(side=tk.LEFT, padx=10)
        
        # URL Display
        ttk.Label(status_frame, text="URL:").pack(side=tk.LEFT, padx=(20, 0))
        self.url_var = tk.StringVar(value="")
        url_label = ttk.Label(status_frame, textvariable=self.url_var, 
                             foreground="blue", cursor="hand2")
        url_label.pack(side=tk.LEFT, padx=5)
        url_label.bind("<Button-1>", lambda e: self.open_browser())
    
    def create_dashboard_tab(self):
        """Create system dashboard"""
        # Title
        title_label = ttk.Label(self.dashboard_frame, text="System Dashboard", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Statistics Frame
        stats_frame = ttk.LabelFrame(self.dashboard_frame, text="System Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create statistics display
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=10, width=70)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh Button
        refresh_btn = ttk.Button(self.dashboard_frame, text="Refresh Statistics", 
                                command=self.refresh_dashboard)
        refresh_btn.pack(pady=10)
        
        # Auto-refresh
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_cb = ttk.Checkbutton(self.dashboard_frame, 
                                         text="Auto-refresh every 30 seconds",
                                         variable=self.auto_refresh_var)
        auto_refresh_cb.pack()
        
        # Start auto-refresh
        self.schedule_refresh()
    
    def create_logs_tab(self):
        """Create logs viewing interface"""
        # Title
        title_label = ttk.Label(self.logs_frame, text="Server Logs", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Logs display
        self.logs_text = scrolledtext.ScrolledText(self.logs_frame, height=20, width=80)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Log controls
        log_controls = ttk.Frame(self.logs_frame)
        log_controls.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(log_controls, text="Clear Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(log_controls, text="Refresh Logs", 
                  command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
    
    def test_database_connection(self):
        """Test database connection"""
        try:
            # Update config with current values
            for key, var in self.db_vars.items():
                self.config["postgresql"][key] = var.get()
            
            # Create test connection string
            db_config = self.config["postgresql"]
            db_url = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            
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
            
            self.db_status_var.set("✓ Connection successful")
            messagebox.showinfo("Success", "Database connection successful!")
            
        except ImportError:
            self.db_status_var.set("✗ psycopg2 not installed")
            messagebox.showerror("Error", "psycopg2 package not found. Install with: pip install psycopg2-binary")
        except Exception as e:
            self.db_status_var.set(f"✗ Connection failed: {str(e)}")
            messagebox.showerror("Connection Error", f"Database connection failed:\n{str(e)}")
    
    def save_database_config(self):
        """Save database configuration"""
        for key, var in self.db_vars.items():
            self.config["postgresql"][key] = var.get()
        
        self.config["server"]["host"] = self.server_host_var.get()
        self.config["server"]["port"] = self.server_port_var.get()
        
        self.save_config()
        messagebox.showinfo("Success", "Configuration saved successfully!")
    
    def start_server(self):
        """Start the Flask server"""
        try:
            # Save current configuration
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
            
            # Update URL
            url = f"http://{self.config['server']['host']}:{self.config['server']['port']}"
            self.url_var.set(url)
            
            self.log_message("Server starting...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            self.log_message(f"Error starting server: {str(e)}")
    
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
            self.root.after(2000, lambda: self.log_message("Server started successfully"))
            
            # Read server output
            for line in iter(self.server_process.stdout.readline, ''):
                if line:
                    self.root.after(0, lambda msg=line.strip(): self.log_message(msg))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Server error: {str(e)}"))
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
            self.url_var.set("")
            
            self.log_message("Server stopped")
            
        except subprocess.TimeoutExpired:
            self.server_process.kill()
            self.log_message("Server force stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop server: {str(e)}")
            self.log_message(f"Error stopping server: {str(e)}")
    
    def restart_server(self):
        """Restart the Flask server"""
        self.log_message("Restarting server...")
        self.stop_server()
        time.sleep(2)
        self.start_server()
    
    def open_browser(self):
        """Open the application in web browser"""
        if self.is_server_running:
            url = f"http://{self.config['server']['host']}:{self.config['server']['port']}"
            webbrowser.open(url)
            self.log_message(f"Opened browser: {url}")
        else:
            messagebox.showwarning("Warning", "Server is not running")
    
    def refresh_dashboard(self):
        """Refresh dashboard statistics"""
        try:
            stats = []
            stats.append(f"System Statistics - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            stats.append("=" * 50)
            
            # System information
            stats.append(f"Python Version: {sys.version}")
            stats.append(f"Platform: {sys.platform}")
            
            # Server status
            if self.is_server_running:
                stats.append(f"Server Status: Running")
                stats.append(f"Server URL: http://{self.config['server']['host']}:{self.config['server']['port']}")
                
                # Try to get server stats
                try:
                    url = f"http://{self.config['server']['host']}:{self.config['server']['port']}"
                    response = requests.get(url, timeout=5)
                    stats.append(f"Server Response: {response.status_code}")
                except:
                    stats.append("Server Response: Unable to connect")
            else:
                stats.append("Server Status: Stopped")
            
            # Database status
            db_config = self.config["postgresql"]
            stats.append(f"Database Host: {db_config['host']}:{db_config['port']}")
            stats.append(f"Database Name: {db_config['database']}")
            
            # System resources
            stats.append("\nSystem Resources:")
            stats.append(f"CPU Usage: {psutil.cpu_percent()}%")
            stats.append(f"Memory Usage: {psutil.virtual_memory().percent}%")
            stats.append(f"Disk Usage: {psutil.disk_usage('/').percent}%")
            
            # Process information
            if self.server_process:
                try:
                    process = psutil.Process(self.server_process.pid)
                    stats.append(f"\nServer Process:")
                    stats.append(f"PID: {self.server_process.pid}")
                    stats.append(f"CPU: {process.cpu_percent()}%")
                    stats.append(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
                except:
                    stats.append("\nServer Process: Information unavailable")
            
            # Update display
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, "\n".join(stats))
            
        except Exception as e:
            self.log_message(f"Error refreshing dashboard: {str(e)}")
    
    def schedule_refresh(self):
        """Schedule automatic dashboard refresh"""
        if self.auto_refresh_var.get():
            self.refresh_dashboard()
        
        # Schedule next refresh
        self.root.after(30000, self.schedule_refresh)  # 30 seconds
    
    def log_message(self, message):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
    
    def clear_logs(self):
        """Clear the logs display"""
        self.logs_text.delete(1.0, tk.END)
    
    def refresh_logs(self):
        """Refresh logs display"""
        # This could be enhanced to read from actual log files
        self.log_message("Logs refreshed")
    
    def update_status(self):
        """Update status indicators"""
        # Check if server is actually running
        if self.server_process and self.server_process.poll() is None:
            if not self.is_server_running:
                self.is_server_running = True
                self.server_status_var.set("Running")
        else:
            if self.is_server_running:
                self.is_server_running = False
                self.server_status_var.set("Stopped")
                
                # Reset UI if server stopped unexpectedly
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.restart_btn.config(state=tk.DISABLED)
                self.open_browser_btn.config(state=tk.DISABLED)
        
        # Schedule next update
        self.root.after(1000, self.update_status)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_server_running:
            if messagebox.askokcancel("Quit", "Server is running. Stop server and quit?"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = HelpDeskLauncher()
    app.run()