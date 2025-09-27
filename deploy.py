#!/usr/bin/env python3
"""
Deployment helper script for Crypto Church Bot
This script helps verify the bot is ready for deployment
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'database.py', 
        'bible_service.py',
        'image_service.py',
        'config.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'prayer_data.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_environment():
    """Check environment variables"""
    bot_token = os.getenv('BOT_TOKEN')
    group_id = os.getenv('ALLOWED_GROUP_ID')
    
    if not bot_token:
        print("⚠️  BOT_TOKEN not set (will need to set in deployment platform)")
    else:
        print("✅ BOT_TOKEN is set")
    
    if not group_id:
        print("⚠️  ALLOWED_GROUP_ID not set (will need to set in deployment platform)")
    else:
        print("✅ ALLOWED_GROUP_ID is set")
    
    return True

def check_images():
    """Check if images folder exists"""
    if os.path.exists('Picturesforchurch') and os.listdir('Picturesforchurch'):
        print("✅ Images folder found with content")
        return True
    else:
        print("⚠️  Picturesforchurch folder missing or empty")
        return False

def main():
    """Main deployment check"""
    print("🚀 Crypto Church Bot - Deployment Check")
    print("=" * 40)
    
    files_ok = check_files()
    env_ok = check_environment()
    images_ok = check_images()
    
    print("\n" + "=" * 40)
    if files_ok and env_ok and images_ok:
        print("✅ Bot is ready for deployment!")
        print("\nNext steps:")
        print("1. Upload all files to GitHub repository")
        print("2. Deploy on Railway/Heroku")
        print("3. Set environment variables in deployment platform")
    else:
        print("❌ Bot needs attention before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()
