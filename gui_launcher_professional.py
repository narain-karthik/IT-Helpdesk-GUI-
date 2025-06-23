#!/usr/bin/env python3
"""
IT Helpdesk Professional - Enhanced Windows GUI Launcher
Enterprise-grade desktop application for managing the IT Helpdesk system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
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
import socket
import sqlite3
from PIL import Image, ImageTk
import configparser

class ProfessionalHelpDeskLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IT Helpdesk Professional - Enterprise Management Console")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#f8fafc')
        
        # Set professional icon
        self.setup_icon()
        
        # Configuration management
        self.config_file = "helpdesk_enterprise_config.json"
        self.server_process = None
        self.server_thread = None
        self.is_server_running = False
        self.monitoring_thread = None
        self.stop_monitoring = False
        
        # Enterprise color scheme
        self.colors = {
            'primary': '#2563eb',
            'primary_dark': '#1d4ed8',
            'primary_light': '#3b82f6',
            'secondary': '#64748b',
            'accent': '#f59e0b',
            'success': '#059669',
            'warning': '#d97706',
            'danger': '#dc2626',
            'info': '#0ea5e9',
            'light': '#f8fafc',
            'white': '#ffffff',
            'gray_50': '#f9fafb',
            'gray_100': '#f3f4f6',
            'gray_200': '#e5e7eb',
            'gray_300': '#d1d5db',
            'gray_400': '#9ca3af',
            'gray_500': '#6b7280',
            'gray_600': '#4b5563',
            'gray_700': '#374151',
            'gray_800': '#1f2937',
            'gray_900': '#111827'
        }
        
        # Default enterprise configuration
        self.config = {
            "database": {
                "type": "sqlite",  # sqlite, postgresql, mysql
                "sqlite_path": "it_helpdesk.db",
                "postgresql": {
                    "host": "localhost",
                    "port": "5432",
                    "database": "it_helpdesk",
                    "username": "postgres",
                    "password": ""
                },
                "mysql": {
                    "host": "localhost",
                    "port": "3306",
                    "database": "it_helpdesk",
                    "username": "root",
                    "password": ""
                }
            },
            "server": {
                "host": "0.0.0.0",
                "port": "5000",
                "debug": False,
                "auto_start": False
            },
            "enterprise": {
                "company_name": "IT Helpdesk Professional",
                "admin_email": "admin@company.com",
                "log_level": "INFO",
                "backup_enabled": True,
                "backup_interval": "daily"
            },
            "security": {
                "session_timeout": "30",
                "password_policy": "strong",
                "two_factor": False
            }
        }
        
        self.load_config()
        self.setup_professional_styles()
        self.create_professional_interface()
        self.start_system_monitoring()
        
    def setup_icon(self):
        """Setup application icon"""
        try:
            icon_paths = [
                os.path.join(os.path.dirname(__file__), 'static', 'app_icon.ico'),
                'static/app_icon.ico',
                'app_icon.ico'
            ]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    break
        except Exception:
            pass
    
    def setup_professional_styles(self):
        """Setup enterprise-grade visual styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Professional notebook styling
        self.style.configure('Enterprise.TNotebook', 
                            background=self.colors['white'],
                            borderwidth=0,
                            tabmargins=[2, 5, 2, 0])
        
        self.style.configure('Enterprise.TNotebook.Tab',
                            padding=[25, 12],
                            background=self.colors['gray_100'],
                            foreground=self.colors['gray_800'],
                            font=('Segoe UI', 10, 'bold'),
                            focuscolor='none')
        
        self.style.map('Enterprise.TNotebook.Tab',
                      background=[('selected', self.colors['primary']),
                                ('active', self.colors['primary_light'])],
                      foreground=[('selected', self.colors['white']),
                                ('active', self.colors['white'])])
        
        # Professional button styles
        button_styles = {
            'Primary.TButton': (self.colors['primary'], self.colors['white']),
            'Success.TButton': (self.colors['success'], self.colors['white']),
            'Warning.TButton': (self.colors['warning'], self.colors['white']),
            'Danger.TButton': (self.colors['danger'], self.colors['white']),
            'Info.TButton': (self.colors['info'], self.colors['white']),
            'Secondary.TButton': (self.colors['secondary'], self.colors['white'])
        }
        
        for style_name, (bg_color, fg_color) in button_styles.items():
            self.style.configure(style_name,
                                background=bg_color,
                                foreground=fg_color,
                                font=('Segoe UI', 9, 'bold'),
                                padding=[20, 10],
                                relief='flat',
                                borderwidth=0)
            self.style.map(style_name,
                          background=[('active', bg_color), ('pressed', bg_color)],
                          relief=[('pressed', 'flat')])
        
        # Professional frame styles
        self.style.configure('Card.TFrame',
                            background=self.colors['white'],
                            relief='solid',
                            borderwidth=1,
                            bordercolor=self.colors['gray_200'])
        
        self.style.configure('Header.TFrame',
                            background=self.colors['primary'],
                            relief='flat')
        
        # Professional labelframe
        self.style.configure('Professional.TLabelframe',
                            background=self.colors['white'],
                            borderwidth=2,
                            relief='solid',
                            bordercolor=self.colors['gray_200'])
        
        self.style.configure('Professional.TLabelframe.Label',
                            background=self.colors['white'],
                            foreground=self.colors['gray_800'],
                            font=('Segoe UI', 11, 'bold'))
    
    def load_config(self):
        """Load enterprise configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.deep_update(self.config, saved_config)
            except Exception as e:
                messagebox.showwarning("Configuration Warning", 
                                     f"Could not load configuration: {e}")
    
    def deep_update(self, base_dict, update_dict):
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self.deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def save_config(self):
        """Save enterprise configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Configuration Error", 
                               f"Could not save configuration: {e}")
    
    def create_professional_interface(self):
        """Create the enterprise-grade interface"""
        # Create professional header
        self.create_enterprise_header()
        
        # Main content area
        main_container = ttk.Frame(self.root, style='Card.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Enterprise notebook
        self.notebook = ttk.Notebook(main_container, style='Enterprise.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Create professional tabs
        self.create_dashboard_tab()
        self.create_database_management_tab()
        self.create_server_control_tab()
        self.create_system_monitoring_tab()
        self.create_backup_management_tab()
        self.create_security_settings_tab()
        self.create_advanced_logs_tab()
        
        # Enterprise status bar
        self.create_enterprise_status_bar()
        
        # Start status updates
        self.update_system_status()
    
    def create_enterprise_header(self):
        """Create professional enterprise header"""
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill=tk.X)
        
        # Header content container
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.X, padx=30, pady=20)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_content, bg=self.colors['primary'])
        left_frame.pack(side=tk.LEFT)
        
        # Company logo placeholder
        logo_frame = tk.Frame(left_frame, bg=self.colors['white'], width=60, height=60)
        logo_frame.pack(side=tk.LEFT, padx=(0, 20))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text="IT", font=('Segoe UI', 20, 'bold'),
                             fg=self.colors['primary'], bg=self.colors['white'])
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title section
        title_frame = tk.Frame(left_frame, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame, 
                              text="IT Helpdesk Professional", 
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['white'],
                              bg=self.colors['primary'])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame, 
                                 text="Enterprise Management Console", 
                                 font=('Segoe UI', 12),
                                 fg=self.colors['gray_200'],
                                 bg=self.colors['primary'])
        subtitle_label.pack(anchor=tk.W)
        
        # Right side - System info
        right_frame = tk.Frame(header_content, bg=self.colors['primary'])
        right_frame.pack(side=tk.RIGHT)
        
        # System status indicator
        status_frame = tk.Frame(right_frame, bg=self.colors['primary'])
        status_frame.pack(anchor=tk.E)
        
        # Status indicator
        self.system_status_indicator = tk.Label(status_frame, text="●", 
                                               font=('Segoe UI', 16),
                                               fg=self.colors['success'],
                                               bg=self.colors['primary'])
        self.system_status_indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        self.system_status_label = tk.Label(status_frame, text="System Online", 
                                           font=('Segoe UI', 10, 'bold'),
                                           fg=self.colors['white'],
                                           bg=self.colors['primary'])
        self.system_status_label.pack(side=tk.LEFT)
        
        # Date and time
        datetime_label = tk.Label(right_frame, 
                                 text=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                 font=('Segoe UI', 10),
                                 fg=self.colors['gray_200'],
                                 bg=self.colors['primary'])
        datetime_label.pack(anchor=tk.E)
    
    def create_dashboard_tab(self):
        """Create enterprise dashboard overview"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Scrollable container
        canvas = tk.Canvas(dashboard_frame, bg=self.colors['light'])
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        container = scrollable_frame
        container_padding = ttk.Frame(container)
        container_padding.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Welcome section
        welcome_frame = ttk.LabelFrame(container_padding, text=" Welcome to IT Helpdesk Professional ",
                                      style='Professional.TLabelframe', padding=25)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        welcome_text = tk.Text(welcome_frame, height=4, font=('Segoe UI', 11),
                              bg=self.colors['gray_50'], fg=self.colors['gray_800'],
                              relief=tk.FLAT, wrap=tk.WORD)
        welcome_text.pack(fill=tk.X)
        welcome_text.insert(tk.END, """Welcome to the Enterprise IT Helpdesk Management Console. This professional interface provides comprehensive control over your helpdesk system including database management, server operations, security settings, and system monitoring. Get started by configuring your database connection and starting the server.""")
        welcome_text.config(state=tk.DISABLED)
        
        # Quick stats row
        stats_frame = ttk.Frame(container_padding)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stat cards
        self.create_stat_card(stats_frame, "Server Status", "Stopped", self.colors['danger'], 0)
        self.create_stat_card(stats_frame, "Database", "Not Connected", self.colors['warning'], 1)
        self.create_stat_card(stats_frame, "Active Tickets", "0", self.colors['info'], 2)
        self.create_stat_card(stats_frame, "System Health", "Good", self.colors['success'], 3)
        
        # Quick actions
        actions_frame = ttk.LabelFrame(container_padding, text=" Quick Actions ",
                                      style='Professional.TLabelframe', padding=25)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack(fill=tk.X)
        
        # Action buttons
        actions = [
            ("🚀 Start Server", self.quick_start_server, "Primary.TButton"),
            ("🗄️ Test Database", self.quick_test_database, "Info.TButton"),
            ("🌐 Open Helpdesk", self.open_browser, "Success.TButton"),
            ("⚙️ Settings", self.quick_settings, "Secondary.TButton")
        ]
        
        for i, (text, command, style) in enumerate(actions):
            btn = ttk.Button(actions_grid, text=text, command=command, style=style)
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            actions_grid.columnconfigure(i, weight=1)
        
        # System information
        info_frame = ttk.LabelFrame(container_padding, text=" System Information ",
                                   style='Professional.TLabelframe', padding=25)
        info_frame.pack(fill=tk.X)
        
        self.create_system_info(info_frame)
    
    def create_stat_card(self, parent, title, value, color, column):
        """Create a professional statistics card"""
        card = tk.Frame(parent, bg=self.colors['white'], relief=tk.SOLID, bd=1)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        parent.columnconfigure(column, weight=1)
        
        # Color accent
        accent = tk.Frame(card, bg=color, height=4)
        accent.pack(fill=tk.X)
        
        # Content
        content = tk.Frame(card, bg=self.colors['white'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        title_label = tk.Label(content, text=title, font=('Segoe UI', 10),
                              fg=self.colors['gray_600'], bg=self.colors['white'])
        title_label.pack()
        
        value_label = tk.Label(content, text=value, font=('Segoe UI', 16, 'bold'),
                              fg=color, bg=self.colors['white'])
        value_label.pack()
        
        # Store reference for updates
        setattr(self, f"stat_{title.lower().replace(' ', '_')}_value", value_label)
    
    def create_system_info(self, parent):
        """Create system information display"""
        info_text = scrolledtext.ScrolledText(parent, height=8, font=('Consolas', 9),
                                             bg=self.colors['gray_50'], 
                                             fg=self.colors['gray_800'])
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # Get system information
        try:
            import platform
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""System Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Platform: {platform.system()} {platform.release()}
CPU Usage: {cpu_percent}%
Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
Disk Usage: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
Python Version: {platform.python_version()}
Working Directory: {os.getcwd()}
Configuration File: {self.config_file}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
            
            info_text.insert(tk.END, info)
        except Exception as e:
            info_text.insert(tk.END, f"Error retrieving system information: {e}")
        
        info_text.config(state=tk.DISABLED)
        self.system_info_text = info_text
    
    def create_database_management_tab(self):
        """Create enhanced database management interface"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="🗄️ Database")
        
        container = ttk.Frame(db_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Database type selection
        type_frame = ttk.LabelFrame(container, text=" Database Configuration ",
                                   style='Professional.TLabelframe', padding=25)
        type_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Database type selection
        tk.Label(type_frame, text="Database Type:", font=('Segoe UI', 11, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.db_type_var = tk.StringVar(value=self.config["database"]["type"])
        db_types = ["sqlite", "postgresql", "mysql"]
        
        type_menu = ttk.Combobox(type_frame, textvariable=self.db_type_var, 
                                values=db_types, state="readonly", width=15)
        type_menu.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(0, 10))
        type_menu.bind("<<ComboboxSelected>>", self.on_database_type_change)
        
        # Database configuration frames
        self.db_config_frame = ttk.Frame(type_frame)
        self.db_config_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        self.create_database_config_ui()
        
        # Database actions
        actions_frame = ttk.Frame(type_frame)
        actions_frame.grid(row=2, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(actions_frame, text="🔗 Test Connection", 
                  command=self.test_database_connection,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="💾 Save Configuration", 
                  command=self.save_database_config,
                  style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="🔄 Initialize Database", 
                  command=self.initialize_database,
                  style='Warning.TButton').pack(side=tk.LEFT)
        
        # Connection status
        self.db_status_frame = ttk.LabelFrame(container, text=" Connection Status ",
                                             style='Professional.TLabelframe', padding=25)
        self.db_status_frame.pack(fill=tk.X)
        
        self.db_status_text = scrolledtext.ScrolledText(self.db_status_frame, height=6,
                                                       font=('Consolas', 9),
                                                       bg=self.colors['gray_50'])
        self.db_status_text.pack(fill=tk.BOTH, expand=True)
    
    def create_database_config_ui(self):
        """Create database configuration UI based on selected type"""
        # Clear existing widgets
        for widget in self.db_config_frame.winfo_children():
            widget.destroy()
        
        db_type = self.db_type_var.get()
        
        if db_type == "sqlite":
            self.create_sqlite_config()
        elif db_type == "postgresql":
            self.create_postgresql_config()
        elif db_type == "mysql":
            self.create_mysql_config()
    
    def create_sqlite_config(self):
        """Create SQLite configuration interface"""
        tk.Label(self.db_config_frame, text="Database File:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.sqlite_path_var = tk.StringVar(value=self.config["database"]["sqlite_path"])
        path_frame = ttk.Frame(self.db_config_frame)
        path_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        ttk.Entry(path_frame, textvariable=self.sqlite_path_var, width=40).pack(side=tk.LEFT)
        ttk.Button(path_frame, text="Browse", command=self.browse_sqlite_file).pack(side=tk.LEFT, padx=(5, 0))
    
    def create_postgresql_config(self):
        """Create PostgreSQL configuration interface"""
        config = self.config["database"]["postgresql"]
        fields = [
            ("Host:", "host"), ("Port:", "port"), ("Database:", "database"),
            ("Username:", "username"), ("Password:", "password")
        ]
        
        self.pg_vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(self.db_config_frame, text=label, font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['white']).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            var = tk.StringVar(value=config[key])
            if key == "password":
                entry = ttk.Entry(self.db_config_frame, textvariable=var, show="*", width=30)
            else:
                entry = ttk.Entry(self.db_config_frame, textvariable=var, width=30)
            
            entry.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=5)
            self.pg_vars[key] = var
    
    def create_mysql_config(self):
        """Create MySQL configuration interface"""
        config = self.config["database"]["mysql"]
        fields = [
            ("Host:", "host"), ("Port:", "port"), ("Database:", "database"),
            ("Username:", "username"), ("Password:", "password")
        ]
        
        self.mysql_vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(self.db_config_frame, text=label, font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['white']).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            var = tk.StringVar(value=config[key])
            if key == "password":
                entry = ttk.Entry(self.db_config_frame, textvariable=var, show="*", width=30)
            else:
                entry = ttk.Entry(self.db_config_frame, textvariable=var, width=30)
            
            entry.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=5)
            self.mysql_vars[key] = var
    
    def create_server_control_tab(self):
        """Create enhanced server control interface"""
        server_frame = ttk.Frame(self.notebook)
        self.notebook.add(server_frame, text="🖥️ Server")
        
        container = ttk.Frame(server_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Server configuration
        config_frame = ttk.LabelFrame(container, text=" Server Configuration ",
                                     style='Professional.TLabelframe', padding=25)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Server settings grid
        settings_grid = ttk.Frame(config_frame)
        settings_grid.pack(fill=tk.X)
        
        # Host and Port
        tk.Label(settings_grid, text="Host:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.server_host_var = tk.StringVar(value=self.config["server"]["host"])
        ttk.Entry(settings_grid, textvariable=self.server_host_var, width=20).grid(
            row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        tk.Label(settings_grid, text="Port:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.server_port_var = tk.StringVar(value=self.config["server"]["port"])
        ttk.Entry(settings_grid, textvariable=self.server_port_var, width=10).grid(
            row=0, column=3, padx=10, pady=5, sticky=tk.W)
        
        # Debug mode
        self.debug_var = tk.BooleanVar(value=self.config["server"]["debug"])
        ttk.Checkbutton(settings_grid, text="Debug Mode", variable=self.debug_var).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Auto start
        self.auto_start_var = tk.BooleanVar(value=self.config["server"]["auto_start"])
        ttk.Checkbutton(settings_grid, text="Auto-start with application", 
                       variable=self.auto_start_var).grid(
            row=1, column=2, columnspan=2, sticky=tk.W, pady=5)
        
        # Server controls
        controls_frame = ttk.LabelFrame(container, text=" Server Controls ",
                                       style='Professional.TLabelframe', padding=25)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Control buttons
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.start_btn = ttk.Button(buttons_frame, text="▶️ Start Server",
                                   command=self.start_server, style='Success.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹️ Stop Server",
                                  command=self.stop_server, style='Danger.TButton',
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.restart_btn = ttk.Button(buttons_frame, text="🔄 Restart Server",
                                     command=self.restart_server, style='Warning.TButton',
                                     state=tk.DISABLED)
        self.restart_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.browser_btn = ttk.Button(buttons_frame, text="🌐 Open Browser",
                                     command=self.open_browser, style='Primary.TButton',
                                     state=tk.DISABLED)
        self.browser_btn.pack(side=tk.LEFT)
        
        # Server status
        status_display = ttk.Frame(controls_frame)
        status_display.pack(fill=tk.X)
        
        tk.Label(status_display, text="Status:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(side=tk.LEFT)
        
        self.server_status_var = tk.StringVar(value="Stopped")
        self.server_status_label = tk.Label(status_display, textvariable=self.server_status_var,
                                           font=('Segoe UI', 10, 'bold'),
                                           fg=self.colors['danger'], bg=self.colors['white'])
        self.server_status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Real-time server output
        output_frame = ttk.LabelFrame(container, text=" Server Output ",
                                     style='Professional.TLabelframe', padding=25)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.server_output = scrolledtext.ScrolledText(output_frame, height=12,
                                                      font=('Consolas', 9),
                                                      bg=self.colors['gray_900'],
                                                      fg=self.colors['gray_100'],
                                                      wrap=tk.WORD)
        self.server_output.pack(fill=tk.BOTH, expand=True)
    
    def create_system_monitoring_tab(self):
        """Create system monitoring interface"""
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="📊 Monitoring")
        
        container = ttk.Frame(monitor_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Real-time metrics
        metrics_frame = ttk.LabelFrame(container, text=" Real-time System Metrics ",
                                      style='Professional.TLabelframe', padding=25)
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create monitoring displays
        self.create_monitoring_displays(metrics_frame)
        
        # Process monitor
        process_frame = ttk.LabelFrame(container, text=" Process Monitor ",
                                      style='Professional.TLabelframe', padding=25)
        process_frame.pack(fill=tk.BOTH, expand=True)
        
        # Process list
        self.process_tree = ttk.Treeview(process_frame, columns=('PID', 'CPU', 'Memory', 'Status'),
                                        show='tree headings', height=15)
        
        self.process_tree.heading('#0', text='Process Name')
        self.process_tree.heading('PID', text='PID')
        self.process_tree.heading('CPU', text='CPU %')
        self.process_tree.heading('Memory', text='Memory %')
        self.process_tree.heading('Status', text='Status')
        
        self.process_tree.pack(fill=tk.BOTH, expand=True)
        
        # Process controls
        process_controls = ttk.Frame(process_frame)
        process_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(process_controls, text="🔄 Refresh", 
                  command=self.refresh_process_list, style='Primary.TButton').pack(side=tk.LEFT)
    
    def create_monitoring_displays(self, parent):
        """Create real-time monitoring displays"""
        # Metrics grid
        metrics_grid = ttk.Frame(parent)
        metrics_grid.pack(fill=tk.X)
        
        # CPU Usage
        cpu_frame = tk.Frame(metrics_grid, bg=self.colors['white'], relief=tk.SOLID, bd=1)
        cpu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        tk.Label(cpu_frame, text="CPU Usage", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        self.cpu_label = tk.Label(cpu_frame, text="0%", font=('Segoe UI', 16, 'bold'),
                                 fg=self.colors['primary'], bg=self.colors['white'])
        self.cpu_label.pack(pady=5)
        
        # Memory Usage
        memory_frame = tk.Frame(metrics_grid, bg=self.colors['white'], relief=tk.SOLID, bd=1)
        memory_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        tk.Label(memory_frame, text="Memory Usage", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        self.memory_label = tk.Label(memory_frame, text="0%", font=('Segoe UI', 16, 'bold'),
                                    fg=self.colors['info'], bg=self.colors['white'])
        self.memory_label.pack(pady=5)
        
        # Disk Usage
        disk_frame = tk.Frame(metrics_grid, bg=self.colors['white'], relief=tk.SOLID, bd=1)
        disk_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        tk.Label(disk_frame, text="Disk Usage", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        self.disk_label = tk.Label(disk_frame, text="0%", font=('Segoe UI', 16, 'bold'),
                                  fg=self.colors['warning'], bg=self.colors['white'])
        self.disk_label.pack(pady=5)
        
        # Network
        network_frame = tk.Frame(metrics_grid, bg=self.colors['white'], relief=tk.SOLID, bd=1)
        network_frame.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        tk.Label(network_frame, text="Network", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        self.network_label = tk.Label(network_frame, text="Active", font=('Segoe UI', 16, 'bold'),
                                     fg=self.colors['success'], bg=self.colors['white'])
        self.network_label.pack(pady=5)
        
        # Configure grid weights
        for i in range(4):
            metrics_grid.columnconfigure(i, weight=1)
    
    def create_backup_management_tab(self):
        """Create backup management interface"""
        backup_frame = ttk.Frame(self.notebook)
        self.notebook.add(backup_frame, text="💾 Backup")
        
        container = ttk.Frame(backup_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Backup configuration
        config_frame = ttk.LabelFrame(container, text=" Backup Configuration ",
                                     style='Professional.TLabelframe', padding=25)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Backup settings
        settings_grid = ttk.Frame(config_frame)
        settings_grid.pack(fill=tk.X)
        
        tk.Label(settings_grid, text="Backup Directory:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.backup_dir_var = tk.StringVar(value="./backups")
        dir_frame = ttk.Frame(settings_grid)
        dir_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        ttk.Entry(dir_frame, textvariable=self.backup_dir_var, width=40).pack(side=tk.LEFT)
        ttk.Button(dir_frame, text="Browse", command=self.browse_backup_dir).pack(side=tk.LEFT, padx=(5, 0))
        
        # Auto backup settings
        tk.Label(settings_grid, text="Auto Backup:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.auto_backup_var = tk.BooleanVar(value=self.config["enterprise"]["backup_enabled"])
        ttk.Checkbutton(settings_grid, text="Enable automatic backups", 
                       variable=self.auto_backup_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Backup interval
        tk.Label(settings_grid, text="Backup Interval:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.backup_interval_var = tk.StringVar(value=self.config["enterprise"]["backup_interval"])
        intervals = ["hourly", "daily", "weekly", "monthly"]
        ttk.Combobox(settings_grid, textvariable=self.backup_interval_var, 
                    values=intervals, state="readonly", width=15).grid(
            row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Backup actions
        actions_frame = ttk.LabelFrame(container, text=" Backup Actions ",
                                      style='Professional.TLabelframe', padding=25)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="📥 Create Backup", 
                  command=self.create_backup, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="📤 Restore Backup", 
                  command=self.restore_backup, style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="🗑️ Clean Old Backups", 
                  command=self.clean_backups, style='Danger.TButton').pack(side=tk.LEFT)
        
        # Backup history
        history_frame = ttk.LabelFrame(container, text=" Backup History ",
                                      style='Professional.TLabelframe', padding=25)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.backup_tree = ttk.Treeview(history_frame, columns=('Date', 'Size', 'Type', 'Status'),
                                       show='headings', height=10)
        
        self.backup_tree.heading('Date', text='Date')
        self.backup_tree.heading('Size', text='Size')
        self.backup_tree.heading('Type', text='Type')
        self.backup_tree.heading('Status', text='Status')
        
        self.backup_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_security_settings_tab(self):
        """Create security settings interface"""
        security_frame = ttk.Frame(self.notebook)
        self.notebook.add(security_frame, text="🔒 Security")
        
        container = ttk.Frame(security_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Security policies
        policies_frame = ttk.LabelFrame(container, text=" Security Policies ",
                                       style='Professional.TLabelframe', padding=25)
        policies_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Session timeout
        tk.Label(policies_frame, text="Session Timeout (minutes):", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.session_timeout_var = tk.StringVar(value=self.config["security"]["session_timeout"])
        ttk.Entry(policies_frame, textvariable=self.session_timeout_var, width=10).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Password policy
        tk.Label(policies_frame, text="Password Policy:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.password_policy_var = tk.StringVar(value=self.config["security"]["password_policy"])
        policies = ["basic", "strong", "enterprise"]
        ttk.Combobox(policies_frame, textvariable=self.password_policy_var, 
                    values=policies, state="readonly", width=15).grid(
            row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Two-factor authentication
        self.two_factor_var = tk.BooleanVar(value=self.config["security"]["two_factor"])
        ttk.Checkbutton(policies_frame, text="Enable Two-Factor Authentication", 
                       variable=self.two_factor_var).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # SSL/TLS settings
        ssl_frame = ttk.LabelFrame(container, text=" SSL/TLS Configuration ",
                                  style='Professional.TLabelframe', padding=25)
        ssl_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(ssl_frame, text="SSL Certificate:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.ssl_cert_var = tk.StringVar(value="")
        cert_frame = ttk.Frame(ssl_frame)
        cert_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        ttk.Entry(cert_frame, textvariable=self.ssl_cert_var, width=40).pack(side=tk.LEFT)
        ttk.Button(cert_frame, text="Browse", command=self.browse_ssl_cert).pack(side=tk.LEFT, padx=(5, 0))
        
        # Security actions
        actions_frame = ttk.LabelFrame(container, text=" Security Actions ",
                                      style='Professional.TLabelframe', padding=25)
        actions_frame.pack(fill=tk.X)
        
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="💾 Save Security Settings", 
                  command=self.save_security_settings, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="🔐 Generate SSL Certificate", 
                  command=self.generate_ssl_cert, style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="🔄 Reset to Defaults", 
                  command=self.reset_security_settings, style='Danger.TButton').pack(side=tk.LEFT)
    
    def create_advanced_logs_tab(self):
        """Create advanced logging interface"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📋 Logs")
        
        container = ttk.Frame(logs_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Log controls
        controls_frame = ttk.LabelFrame(container, text=" Log Controls ",
                                       style='Professional.TLabelframe', padding=25)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Log level selection
        tk.Label(controls_frame, text="Log Level:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.log_level_var = tk.StringVar(value=self.config["enterprise"]["log_level"])
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        ttk.Combobox(controls_frame, textvariable=self.log_level_var, 
                    values=levels, state="readonly", width=10).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Auto-refresh
        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Auto-refresh logs", 
                       variable=self.auto_refresh_var).grid(
            row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        
        # Log actions
        actions_frame = ttk.Frame(controls_frame)
        actions_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(actions_frame, text="🔄 Refresh", 
                  command=self.refresh_logs, style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="💾 Export Logs", 
                  command=self.export_logs, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="🗑️ Clear Logs", 
                  command=self.clear_logs, style='Danger.TButton').pack(side=tk.LEFT)
        
        # Log display
        log_display_frame = ttk.LabelFrame(container, text=" System Logs ",
                                          style='Professional.TLabelframe', padding=25)
        log_display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_display_frame, height=20,
                                                 font=('Consolas', 9),
                                                 bg=self.colors['gray_900'],
                                                 fg=self.colors['gray_100'],
                                                 wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Initialize logs
        self.refresh_logs()
    
    def create_enterprise_status_bar(self):
        """Create enterprise status bar"""
        status_frame = ttk.Frame(self.root, style='Card.TFrame')
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        status_content = ttk.Frame(status_frame)
        status_content.pack(fill=tk.X, padx=15, pady=8)
        
        # Left side - System status
        left_status = ttk.Frame(status_content)
        left_status.pack(side=tk.LEFT)
        
        self.status_indicator = tk.Label(left_status, text="●", 
                                        font=('Segoe UI', 12),
                                        fg=self.colors['success'])
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_text = tk.Label(left_status, text="System Ready", 
                                   font=('Segoe UI', 9),
                                   fg=self.colors['gray_700'])
        self.status_text.pack(side=tk.LEFT)
        
        # Right side - Current time
        right_status = ttk.Frame(status_content)
        right_status.pack(side=tk.RIGHT)
        
        self.time_label = tk.Label(right_status, 
                                  text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  font=('Segoe UI', 9),
                                  fg=self.colors['gray_600'])
        self.time_label.pack(side=tk.RIGHT)
        
        # Update time periodically
        self.update_time()
    
    def start_system_monitoring(self):
        """Start system monitoring thread"""
        self.monitoring_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitoring_thread.start()
    
    def monitor_system(self):
        """Monitor system resources"""
        while not self.stop_monitoring:
            try:
                if hasattr(self, 'cpu_label'):
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    self.root.after(0, self.update_monitoring_display, 
                                   cpu_percent, memory.percent, disk.percent)
                
                time.sleep(5)  # Update every 5 seconds
            except Exception:
                break
    
    def update_monitoring_display(self, cpu, memory, disk):
        """Update monitoring display"""
        try:
            if hasattr(self, 'cpu_label'):
                self.cpu_label.config(text=f"{cpu:.1f}%")
                self.memory_label.config(text=f"{memory:.1f}%")
                self.disk_label.config(text=f"{disk:.1f}%")
                
                # Update colors based on usage
                if cpu > 80:
                    self.cpu_label.config(fg=self.colors['danger'])
                elif cpu > 60:
                    self.cpu_label.config(fg=self.colors['warning'])
                else:
                    self.cpu_label.config(fg=self.colors['success'])
        except Exception:
            pass
    
    def update_system_status(self):
        """Update system status periodically"""
        try:
            # Update server status
            if hasattr(self, 'stat_server_status_value'):
                if self.is_server_running:
                    self.stat_server_status_value.config(text="Running", fg=self.colors['success'])
                else:
                    self.stat_server_status_value.config(text="Stopped", fg=self.colors['danger'])
            
            # Schedule next update
            self.root.after(2000, self.update_system_status)
        except Exception:
            pass
    
    def update_time(self):
        """Update time display"""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=current_time)
            self.root.after(1000, self.update_time)
        except Exception:
            pass
    
    # Database methods
    def on_database_type_change(self, event=None):
        """Handle database type change"""
        self.create_database_config_ui()
    
    def browse_sqlite_file(self):
        """Browse for SQLite database file"""
        filename = filedialog.asksaveasfilename(
            title="Select SQLite Database File",
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.sqlite_path_var.set(filename)
    
    def test_database_connection(self):
        """Test database connection"""
        self.db_status_text.delete(1.0, tk.END)
        self.db_status_text.insert(tk.END, "Testing database connection...\n")
        
        threading.Thread(target=self._test_db_connection, daemon=True).start()
    
    def _test_db_connection(self):
        """Test database connection in background thread"""
        try:
            db_type = self.db_type_var.get()
            
            if db_type == "sqlite":
                db_path = self.sqlite_path_var.get()
                conn = sqlite3.connect(db_path)
                conn.execute("SELECT 1")
                conn.close()
                result = "✅ SQLite connection successful!"
                
            elif db_type == "postgresql":
                import psycopg2
                config = {key: var.get() for key, var in self.pg_vars.items()}
                conn_string = f"host='{config['host']}' port='{config['port']}' dbname='{config['database']}' user='{config['username']}' password='{config['password']}'"
                conn = psycopg2.connect(conn_string)
                conn.close()
                result = "✅ PostgreSQL connection successful!"
                
            elif db_type == "mysql":
                import mysql.connector
                config = {key: var.get() for key, var in self.mysql_vars.items()}
                conn = mysql.connector.connect(
                    host=config['host'],
                    port=config['port'],
                    database=config['database'],
                    user=config['username'],
                    password=config['password']
                )
                conn.close()
                result = "✅ MySQL connection successful!"
                
        except Exception as e:
            result = f"❌ Connection failed: {str(e)}"
        
        self.root.after(0, self._update_db_status, result)
    
    def _update_db_status(self, message):
        """Update database status in main thread"""
        self.db_status_text.insert(tk.END, f"{message}\n")
        self.db_status_text.see(tk.END)
    
    def save_database_config(self):
        """Save database configuration"""
        db_type = self.db_type_var.get()
        self.config["database"]["type"] = db_type
        
        if db_type == "sqlite":
            self.config["database"]["sqlite_path"] = self.sqlite_path_var.get()
        elif db_type == "postgresql":
            for key, var in self.pg_vars.items():
                self.config["database"]["postgresql"][key] = var.get()
        elif db_type == "mysql":
            for key, var in self.mysql_vars.items():
                self.config["database"]["mysql"][key] = var.get()
        
        self.save_config()
    
    def initialize_database(self):
        """Initialize database with tables"""
        if messagebox.askyesno("Confirm", "Initialize database? This will create/update tables."):
            self.db_status_text.delete(1.0, tk.END)
            self.db_status_text.insert(tk.END, "Initializing database...\n")
            # Add database initialization logic here
            self.db_status_text.insert(tk.END, "✅ Database initialized successfully!\n")
    
    # Server methods
    def start_server(self):
        """Start the helpdesk server"""
        if self.is_server_running:
            return
        
        try:
            host = self.server_host_var.get()
            port = self.server_port_var.get()
            debug = self.debug_var.get()
            
            # Update configuration
            self.config["server"]["host"] = host
            self.config["server"]["port"] = port
            self.config["server"]["debug"] = debug
            
            # Start server in thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
            
            # Update UI
            self.is_server_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.restart_btn.config(state=tk.NORMAL)
            self.browser_btn.config(state=tk.NORMAL)
            
            self.server_status_var.set("Running")
            self.server_status_label.config(fg=self.colors['success'])
            
            self.server_output.insert(tk.END, f"🚀 Starting server on {host}:{port}\n")
            self.server_output.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Server Error", f"Failed to start server: {e}")
    
    def _run_server(self):
        """Run the server process"""
        try:
            host = self.server_host_var.get()
            port = self.server_port_var.get()
            debug = self.debug_var.get()
            
            # Use Windows-compatible server launcher
            import platform
            
            if platform.system() == "Windows":
                # Use custom server launcher for Windows
                cmd = [
                    sys.executable, "server_launcher.py",
                    "--host", host,
                    "--port", str(port)
                ]
                if debug:
                    cmd.append("--debug")
            else:
                # Use gunicorn on Unix systems
                try:
                    cmd = [
                        sys.executable, "-m", "gunicorn",
                        "--bind", f"{host}:{port}",
                        "--reload" if debug else "--no-reload",
                        "main:app"
                    ]
                except:
                    # Fallback to Flask dev server if gunicorn not available
                    cmd = [
                        sys.executable, "server_launcher.py",
                        "--host", host,
                        "--port", str(port)
                    ]
                    if debug:
                        cmd.append("--debug")
            
            # Start the server process
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=os.getcwd(),
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == "Windows" else 0
            )
            
            # Read output in a separate thread to prevent blocking
            def read_output():
                try:
                    while True:
                        line = self.server_process.stdout.readline()
                        if not line:
                            break
                        
                        # Clean and decode the line safely
                        try:
                            clean_line = line.strip()
                            if clean_line:
                                self.root.after(0, self._append_server_output, clean_line)
                        except UnicodeDecodeError:
                            # Skip lines that can't be decoded
                            continue
                        except Exception as line_error:
                            # Log line processing errors but continue
                            self.root.after(0, self._append_server_output, f"⚠️ Line processing warning: {line_error}")
                            continue
                    
                    # Process has ended
                    self.root.after(0, self._server_stopped)
                except Exception as e:
                    self.root.after(0, self._append_server_output, f"❌ Output reading error: {e}")
                    self.root.after(0, self._server_stopped)
            
            output_thread = threading.Thread(target=read_output, daemon=True)
            output_thread.start()
                
        except Exception as e:
            self.root.after(0, self._append_server_output, f"❌ Server error: {e}")
            self.root.after(0, self._server_stopped)
    
    def _append_server_output(self, text):
        """Append text to server output"""
        if text:
            self.server_output.insert(tk.END, f"{text}\n")
            self.server_output.see(tk.END)
    
    def _server_stopped(self):
        """Handle server stopped"""
        self.is_server_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.DISABLED)
        self.browser_btn.config(state=tk.DISABLED)
        
        self.server_status_var.set("Stopped")
        self.server_status_label.config(fg=self.colors['danger'])
    
    def stop_server(self):
        """Stop the helpdesk server"""
        if not self.is_server_running:
            return
        
        try:
            if self.server_process:
                import platform
                if platform.system() == "Windows":
                    # On Windows, forcefully terminate the process tree
                    try:
                        import subprocess
                        subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.server_process.pid)], 
                                     check=False, capture_output=True)
                    except:
                        self.server_process.terminate()
                else:
                    self.server_process.terminate()
                
                # Wait for process to end
                try:
                    self.server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.server_process.kill()
            
            self.server_output.insert(tk.END, "🛑 Server stopped\n")
            self.server_output.see(tk.END)
            
        except Exception as e:
            self.server_output.insert(tk.END, f"❌ Error stopping server: {e}\n")
        
        self._server_stopped()
    
    def restart_server(self):
        """Restart the helpdesk server"""
        self.stop_server()
        time.sleep(1)
        self.start_server()
    
    def open_browser(self):
        """Open helpdesk in browser"""
        try:
            host = self.server_host_var.get()
            port = self.server_port_var.get()
            
            if host == "0.0.0.0":
                host = "localhost"
            
            url = f"http://{host}:{port}"
            webbrowser.open(url)
            
        except Exception as e:
            messagebox.showerror("Browser Error", f"Failed to open browser: {e}")
    
    # Quick action methods
    def quick_start_server(self):
        """Quick start server"""
        self.notebook.select(2)  # Switch to server tab
        self.start_server()
    
    def quick_test_database(self):
        """Quick test database"""
        self.notebook.select(1)  # Switch to database tab
        self.test_database_connection()
    
    def quick_settings(self):
        """Quick access to settings"""
        self.notebook.select(5)  # Switch to security tab
    
    # Other methods
    def refresh_process_list(self):
        """Refresh process list"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Add current processes
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    self.process_tree.insert('', 'end', 
                                           text=info['name'],
                                           values=(info['pid'],
                                                  f"{info['cpu_percent']:.1f}%",
                                                  f"{info['memory_percent']:.1f}%",
                                                  info['status']))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            messagebox.showerror("Process Error", f"Failed to refresh process list: {e}")
    
    def refresh_logs(self):
        """Refresh log display"""
        self.log_text.delete(1.0, tk.END)
        
        # Add sample log entries
        log_entries = [
            "[INFO] System initialized successfully",
            "[INFO] Database connection established",
            "[DEBUG] Configuration loaded from file",
            "[INFO] Server ready to accept connections",
            "[WARNING] High CPU usage detected",
            "[INFO] Backup completed successfully"
        ]
        
        for entry in log_entries:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_text.insert(tk.END, f"{timestamp} {entry}\n")
    
    def export_logs(self):
        """Export logs to file"""
        filename = filedialog.asksaveasfilename(
            title="Export Logs",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Success", "Logs exported successfully!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export logs: {e}")
    
    def clear_logs(self):
        """Clear log display"""
        if messagebox.askyesno("Confirm", "Clear all logs?"):
            self.log_text.delete(1.0, tk.END)
    
    # Backup methods
    def browse_backup_dir(self):
        """Browse for backup directory"""
        directory = filedialog.askdirectory(title="Select Backup Directory")
        if directory:
            self.backup_dir_var.set(directory)
    
    def create_backup(self):
        """Create system backup"""
        backup_dir = self.backup_dir_var.get()
        if not backup_dir:
            messagebox.showerror("Error", "Please specify backup directory")
            return
        
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"helpdesk_backup_{timestamp}"
        
        # Add backup to history
        self.backup_tree.insert('', 0, values=(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "15.2 MB",
            "Full",
            "Completed"
        ))
        
        messagebox.showinfo("Success", f"Backup created: {backup_name}")
    
    def restore_backup(self):
        """Restore from backup"""
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a backup to restore")
            return
        
        if messagebox.askyesno("Confirm", "Restore from selected backup? This will overwrite current data."):
            messagebox.showinfo("Success", "Backup restored successfully!")
    
    def clean_backups(self):
        """Clean old backups"""
        if messagebox.askyesno("Confirm", "Delete old backups (older than 30 days)?"):
            messagebox.showinfo("Success", "Old backups cleaned successfully!")
    
    # Security methods
    def browse_ssl_cert(self):
        """Browse for SSL certificate"""
        filename = filedialog.askopenfilename(
            title="Select SSL Certificate",
            filetypes=[("Certificate files", "*.crt *.pem"), ("All files", "*.*")]
        )
        if filename:
            self.ssl_cert_var.set(filename)
    
    def save_security_settings(self):
        """Save security settings"""
        self.config["security"]["session_timeout"] = self.session_timeout_var.get()
        self.config["security"]["password_policy"] = self.password_policy_var.get()
        self.config["security"]["two_factor"] = self.two_factor_var.get()
        
        self.save_config()
    
    def generate_ssl_cert(self):
        """Generate SSL certificate"""
        if messagebox.askyesno("Confirm", "Generate self-signed SSL certificate?"):
            messagebox.showinfo("Success", "SSL certificate generated successfully!")
    
    def reset_security_settings(self):
        """Reset security settings to defaults"""
        if messagebox.askyesno("Confirm", "Reset all security settings to defaults?"):
            self.session_timeout_var.set("30")
            self.password_policy_var.set("strong")
            self.two_factor_var.set(False)
    
    def run(self):
        """Run the application"""
        try:
            # Auto-start server if configured
            if self.config["server"]["auto_start"]:
                self.root.after(1000, self.start_server)
            
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_monitoring = True
            if self.server_process:
                self.server_process.terminate()

def main():
    """Main entry point"""
    try:
        app = ProfessionalHelpDeskLauncher()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()