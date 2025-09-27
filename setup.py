#!/usr/bin/env python3
"""
Crypto Church Bot Setup Script
This script helps you set up the environment variables needed for the bot.
"""

import os
import sys

def create_env_file():
    """Create a .env file with user input"""
    print("🙏 Welcome to Crypto Church Bot Setup! 🙏")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("A .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled. Existing .env file preserved.")
            return
    
    print("\n📝 Let's set up your bot configuration:")
    print("(Press Enter to skip optional values)")
    
    # Required values
    bot_token = input("\n🤖 Enter your Telegram Bot Token (required): ").strip()
    if not bot_token:
        print("❌ Bot token is required! Setup cancelled.")
        return
    
    group_id = input("👥 Enter your Telegram Group ID (required): ").strip()
    if not group_id:
        print("❌ Group ID is required! Setup cancelled.")
        return
    
    # Optional values
    bible_api_key = input("📖 Enter your Bible API Key (optional but recommended): ").strip()
    
    # Create .env content
    env_content = f"""# Telegram Bot Configuration
BOT_TOKEN={bot_token}
ALLOWED_GROUP_ID={group_id}

# Bible API Configuration (Optional but recommended)
BIBLE_API_KEY={bible_api_key or ''}
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")
        
        if bible_api_key:
            print("📖 Bible API configured - you'll have access to advanced features!")
        else:
            print("📖 No Bible API key - bot will use built-in verses")
        
        print("\n🚀 You're ready to run the bot!")
        print("Run: python main.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

def show_help():
    """Show setup help information"""
    print("""
🙏 Crypto Church Bot Setup Help 🙏

This script helps you create a .env file with your bot configuration.

Required Information:
1. Telegram Bot Token - Get from @BotFather
2. Telegram Group ID - The group where your bot will operate

Optional Information:
3. Bible API Key - Get from https://scripture.api.bible/

How to get your Bot Token:
1. Message @BotFather on Telegram
2. Send /newbot
3. Follow the instructions
4. Copy the token provided

How to get your Group ID:
1. Add your bot to a Telegram group
2. Send a message in the group
3. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
4. Look for the "chat.id" field

How to get Bible API Key:
1. Visit https://scripture.api.bible/
2. Sign up for a free account
3. Get your API key
4. Free tier: 1000 requests/month

Run this script again to start setup: python setup.py
""")

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return
    
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("Run 'python setup.py --help' for assistance.")

if __name__ == '__main__':
    main()












