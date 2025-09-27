#!/usr/bin/env python3
"""
Install fonts system-wide for The Holy Ledger project
"""

import os
import shutil
from pathlib import Path

def install_fonts():
    """Install fonts to Windows Fonts directory"""
    print("🎨 Installing fonts system-wide...")
    
    fonts_dir = Path("fonts")
    windows_fonts_dir = Path("C:/Windows/Fonts")
    
    if not fonts_dir.exists():
        print("❌ Fonts directory not found!")
        return False
    
    if not windows_fonts_dir.exists():
        print("❌ Windows Fonts directory not found!")
        return False
    
    installed_count = 0
    font_files = list(fonts_dir.glob("*.ttf")) + list(fonts_dir.glob("*.otf"))
    
    for font_file in font_files:
        try:
            destination = windows_fonts_dir / font_file.name
            if not destination.exists():
                shutil.copy2(font_file, destination)
                print(f"✅ Installed: {font_file.name}")
                installed_count += 1
            else:
                print(f"⚠️ Already installed: {font_file.name}")
        except Exception as e:
            print(f"❌ Failed to install {font_file.name}: {e}")
    
    print(f"\n🎉 Successfully installed {installed_count} fonts!")
    print("🔄 Fonts are now available system-wide")
    print("🚀 The bot will automatically detect and use these fonts")
    
    return installed_count > 0

if __name__ == "__main__":
    install_fonts()
