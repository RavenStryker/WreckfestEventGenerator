import os
import shutil
import sys
import ctypes

def is_font_installed(font_name):
    FR_PRIVATE = 0x10
    hdc = ctypes.windll.user32.GetDC(None)
    result = ctypes.windll.gdi32.AddFontResourceExW(font_name, FR_PRIVATE, None)
    ctypes.windll.user32.ReleaseDC(None, hdc)

    return bool(result)

font_folder = os.getcwd()
destination = 'C:\\Windows\\Fonts\\'

for root, _, files in os.walk(font_folder):
    for file in files:
        if file.endswith('.ttf') or file.endswith('.otf'):
            font_path = os.path.join(root, file)
            font_name = os.path.splitext(file)[0]
            dest_path = os.path.join(destination, file)

            if not is_font_installed(font_name):
                try:
                    shutil.copy(font_path, dest_path)
                    print(f"Installed {font_name}")
                except PermissionError:
                    print(f"Permission denied. Run the script as an administrator to install {font_name}")
            else:
                print(f"{font_name} is already installed")
