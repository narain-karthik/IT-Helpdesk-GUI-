#!/usr/bin/env python3
"""
Create application icon for the GTN Helpdesk Launcher
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_application_icon():
    """Create a professional application icon"""
    try:
        # Create a 256x256 icon with GTN branding
        size = 256
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Background gradient
        for i in range(size):
            alpha = int(255 * (1 - i / size))
            color = (41, 128, 185, alpha)  # Professional blue
            draw.rectangle([0, i, size, i+1], fill=color)
        
        # Draw main circle
        margin = 20
        circle_size = size - 2 * margin
        draw.ellipse([margin, margin, margin + circle_size, margin + circle_size], 
                    fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=3)
        
        # Draw inner elements
        center = size // 2
        
        # Computer/monitor icon
        monitor_width = 80
        monitor_height = 60
        monitor_x = center - monitor_width // 2
        monitor_y = center - monitor_height // 2 - 10
        
        # Monitor screen
        draw.rectangle([monitor_x, monitor_y, monitor_x + monitor_width, monitor_y + monitor_height],
                      fill=(236, 240, 241, 255), outline=(127, 140, 141, 255), width=2)
        
        # Monitor base
        base_width = 20
        base_height = 8
        base_x = center - base_width // 2
        base_y = monitor_y + monitor_height
        draw.rectangle([base_x, base_y, base_x + base_width, base_y + base_height],
                      fill=(127, 140, 141, 255))
        
        # Screen elements (simulating helpdesk interface)
        screen_margin = 8
        line_height = 6
        
        for i in range(4):
            y_pos = monitor_y + screen_margin + i * (line_height + 2)
            draw.rectangle([monitor_x + screen_margin, y_pos, 
                          monitor_x + monitor_width - screen_margin, y_pos + line_height],
                         fill=(52, 152, 219, 255))
        
        # Add gear/settings icon in corner
        gear_size = 24
        gear_x = size - margin - gear_size - 10
        gear_y = margin + 10
        
        # Simple gear representation
        draw.ellipse([gear_x, gear_y, gear_x + gear_size, gear_y + gear_size],
                    fill=(231, 76, 60, 255), outline=(192, 57, 43, 255), width=2)
        
        # Gear center
        gear_center = gear_size // 2
        center_size = 8
        draw.ellipse([gear_x + gear_center - center_size//2, gear_y + gear_center - center_size//2,
                     gear_x + gear_center + center_size//2, gear_y + gear_center + center_size//2],
                    fill=(255, 255, 255, 255))
        
        # Save in different sizes for Windows icon
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        
        os.makedirs('static', exist_ok=True)
        
        # Save as ICO
        img.save('static/app_icon.ico', format='ICO', sizes=sizes)
        
        # Save as PNG for other uses
        img.save('static/app_icon.png', format='PNG')
        
        print("Application icon created successfully")
        return True
        
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

if __name__ == "__main__":
    create_application_icon()