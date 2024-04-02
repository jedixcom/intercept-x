import ctypes
import sys
import os
import winreg as reg

def set_wallpaper_style(tile=False):
    # Open the registry key for desktop background settings
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, reg.KEY_WRITE)
    
    # Set the wallpaper style to centered (0) or tiled (1)
    # 0: Center
    # 1: Tile
    # 2: Stretch
    # 3: Fit
    # 4: Fill
    # 5: Span (for multi-monitor setups)
    # Wallpaper style: 0 (Centered), 1 (Tiled), 2 (Stretched), 3 (Fit), 4 (Fill), 5 (Span)
    # For centering without tiling, set WallpaperStyle to 0 and TileWallpaper to 0
    reg.SetValueEx(key, "WallpaperStyle", 0, reg.REG_SZ, "0")
    reg.SetValueEx(key, "TileWallpaper", 0, reg.REG_SZ, "1" if tile else "0")
    
    # Close the registry key
    reg.CloseKey(key)

# Function to set the wallpaper
def set_wallpaper(path):
    # First, set the wallpaper style to centered
    set_wallpaper_style(tile=False)
    
    # Then, set the wallpaper
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# Function to display the banner from banner.txt
def display_banner():
    try:
        with open('banner.txt', 'r') as file:
            banner = file.read()
            print(banner)
    except FileNotFoundError:
        print("The file 'banner.txt' was not found.")
        sys.exit(1)

# Display the banner
display_banner()

# Path to the wallpaper image
# Make sure to replace 'path_to_your_wallpaper.jpg' with the actual path to your new wallpaper image
wallpaper_path = r'C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\wallpaper888.jpg'  # Use a raw string or appropriate escape

# Set the new wallpaper
set_wallpaper(wallpaper_path)

print("Wallpaper has been changed and centered successfully!")
