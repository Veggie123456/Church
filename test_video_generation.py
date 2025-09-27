#!/usr/bin/env python3
"""
Test script for video generation functionality
Run this to test The Holy Ledger video generation
"""

import os
import sys
from database import PrayerDatabase
from video_service import VideoService

def test_video_generation():
    """Test the video generation functionality"""
    print("🎬 Testing The Holy Ledger Video Generation...")
    
    # Initialize services
    db = PrayerDatabase()
    video_service = VideoService()
    
    # Check if base video exists
    if not os.path.exists(video_service.video_path):
        print(f"❌ Base video not found: {video_service.video_path}")
        print("Please ensure the MP4 file is in the Picturesforchurch folder")
        return False
    
    # Get current leaderboard data
    top_tickers = db.get_top_tickers(10)
    print(f"📊 Found {len(top_tickers)} tickers in database")
    
    if not top_tickers:
        print("❌ No ticker data available. Please add some prayers first!")
        return False
    
    # Display current leaderboard
    print("\n📜 Current Leaderboard:")
    for i, ticker in enumerate(top_tickers, 1):
        print(f"{i}. {ticker['ticker']} - {ticker['count']} prayers")
    
    # Test static image generation first
    print("\n🖼️ Testing static image generation...")
    static_image = video_service.create_static_leaderboard_image(top_tickers)
    if static_image and os.path.exists(static_image):
        print(f"✅ Static image created: {static_image}")
    else:
        print("❌ Failed to create static image")
        return False
    
    # Test video generation
    print("\n🎬 Testing video generation...")
    video_path = video_service.get_leaderboard_video()
    if video_path and os.path.exists(video_path):
        print(f"✅ Video created: {video_path}")
        print(f"📁 File size: {os.path.getsize(video_path)} bytes")
        return True
    else:
        print("❌ Failed to create video")
        return False

if __name__ == "__main__":
    success = test_video_generation()
    if success:
        print("\n🎉 Video generation test completed successfully!")
        print("You can now use /holyledger command in the bot")
    else:
        print("\n❌ Video generation test failed!")
        print("Check the error messages above and ensure all dependencies are installed")
        sys.exit(1)
