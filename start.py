#!/usr/bin/env python3
"""
Startup script for Crypto Church Bot
This ensures the bot starts properly on deployment platforms
"""

import os
import sys
from main import main

if __name__ == "__main__":
    # Check if required environment variables are set
    if not os.getenv('BOT_TOKEN'):
        print("❌ Error: BOT_TOKEN environment variable not set")
        print("Please set BOT_TOKEN in your deployment platform")
        sys.exit(1)
    
    if not os.getenv('ALLOWED_GROUP_ID'):
        print("❌ Error: ALLOWED_GROUP_ID environment variable not set")
        print("Please set ALLOWED_GROUP_ID in your deployment platform")
        sys.exit(1)
    
    print("🚀 Starting Crypto Church Bot...")
    print("✅ Environment variables loaded")
    print("✅ Bot is ready to serve!")
    
    # Start the bot
    main()
