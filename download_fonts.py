#!/usr/bin/env python3
"""
Download free serif fonts for The Holy Ledger project
"""

import os
import requests
from pathlib import Path

def download_font(url, filename):
    """Download a font file"""
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(f"fonts/{filename}", 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def main():
    """Download free serif fonts"""
    print("🎨 Downloading free serif fonts for The Holy Ledger...")
    
    # Create fonts directory if it doesn't exist
    os.makedirs("fonts", exist_ok=True)
    
    # Free serif fonts that would work well for the project
    fonts_to_download = [
        {
            "name": "Cinzel-Regular.ttf",
            "url": "https://github.com/google/fonts/raw/main/ofl/cinzel/Cinzel-Regular.ttf"
        },
        {
            "name": "PlayfairDisplay-Regular.ttf", 
            "url": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Regular.ttf"
        },
        {
            "name": "CrimsonText-Regular.ttf",
            "url": "https://github.com/google/fonts/raw/main/ofl/crimsontext/CrimsonText-Regular.ttf"
        },
        {
            "name": "LibreBaskerville-Regular.ttf",
            "url": "https://github.com/google/fonts/raw/main/ofl/librebaskerville/LibreBaskerville-Regular.ttf"
        }
    ]
    
    success_count = 0
    for font in fonts_to_download:
        if download_font(font["url"], font["name"]):
            success_count += 1
    
    print(f"\n🎉 Successfully downloaded {success_count}/{len(fonts_to_download)} fonts!")
    
    if success_count > 0:
        print("\n📁 Fonts are now available in the 'fonts/' directory")
        print("🔄 The bot will automatically detect and use these fonts")
        print("🚀 You can now use /holyledger command with beautiful typography!")
    else:
        print("\n⚠️ No fonts were downloaded. The bot will use default fonts.")

if __name__ == "__main__":
    main()
