import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from config import DB_FILE

class PrayerDatabase:
    def __init__(self):
        self.db_file = DB_FILE
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self.get_default_structure()
        return self.get_default_structure()
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get_default_structure(self) -> Dict:
        """Get default database structure"""
        return {
            "prayers": {},
            "user_stats": {},
            "last_verse_time": None,
            "total_prayers": 0,
            "leaderboard_history": [],
            "ideas": []
        }
    
    def add_prayer(self, ticker: str, user_id: int, username: str) -> Dict:
        """Add a prayer for a specific ticker"""
        ticker = ticker.upper().strip()
        
        if ticker not in self.data["prayers"]:
            self.data["prayers"][ticker] = {
                "count": 0,
                "prayers": [],
                "last_prayer": None
            }
        
        # Check if user already prayed for this ticker today
        today = datetime.now().strftime("%Y-%m-%d")
        existing_prayer = next(
            (p for p in self.data["prayers"][ticker]["prayers"] 
             if p["user_id"] == user_id and p["date"] == today), 
            None
        )
        
        if existing_prayer:
            return {
                "success": False,
                "message": f"You have already prayed for {ticker} today! 🙏"
            }
        
        # Add new prayer
        prayer_record = {
            "user_id": user_id,
            "username": username,
            "date": today,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["prayers"][ticker]["prayers"].append(prayer_record)
        self.data["prayers"][ticker]["count"] += 1
        self.data["prayers"][ticker]["last_prayer"] = datetime.now().isoformat()
        
        # Update user stats
        if str(user_id) not in self.data["user_stats"]:
            self.data["user_stats"][str(user_id)] = {
                "username": username,
                "total_prayers": 0,
                "tickers_prayed_for": []
            }
        
        self.data["user_stats"][str(user_id)]["total_prayers"] += 1
        
        # Ensure tickers_prayed_for is a list and add ticker if not already present
        if ticker not in self.data["user_stats"][str(user_id)]["tickers_prayed_for"]:
            self.data["user_stats"][str(user_id)]["tickers_prayed_for"].append(ticker)
        
        self.data["total_prayers"] += 1
        self.save_data()
        
        return {
            "success": True,
            "message": f"🙏 Prayer recorded for {ticker}! Total prayers: {self.data['prayers'][ticker]['count']}",
            "ticker_count": self.data["prayers"][ticker]["count"]
        }
    
    def get_ticker_stats(self, ticker: str) -> Optional[Dict]:
        """Get statistics for a specific ticker"""
        ticker = ticker.upper().strip()
        if ticker in self.data["prayers"]:
            return self.data["prayers"][ticker]
        return None
    
    def get_top_tickers(self, limit: int = 10) -> List[Dict]:
        """Get top tickers by prayer count"""
        tickers = []
        for ticker, data in self.data["prayers"].items():
            tickers.append({
                "ticker": ticker,
                "count": data["count"],
                "last_prayer": data["last_prayer"]
            })
        
        tickers.sort(key=lambda x: x["count"], reverse=True)
        return tickers[:limit]
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """Get statistics for a specific user"""
        user_id_str = str(user_id)
        if user_id_str in self.data["user_stats"]:
            return self.data["user_stats"][user_id_str]
        return None
    
    def get_total_stats(self) -> Dict:
        """Get overall statistics"""
        return {
            "total_prayers": self.data["total_prayers"],
            "unique_tickers": len(self.data["prayers"]),
            "unique_users": len(self.data["user_stats"])
        }
    
    def set_last_verse_time(self, timestamp: str):
        """Set the last time a random verse was sent"""
        self.data["last_verse_time"] = timestamp
        self.save_data()
    
    def get_last_verse_time(self) -> Optional[str]:
        """Get the last time a random verse was sent"""
        return self.data.get("last_verse_time")
    
    def save_leaderboard_snapshot(self):
        """Save current leaderboard state for persistence"""
        top_tickers = self.get_top_tickers(10)
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "total_prayers": self.data["total_prayers"],
            "leaderboard": top_tickers
        }
        
        # Add to history (keep last 100 snapshots)
        self.data["leaderboard_history"].append(snapshot)
        if len(self.data["leaderboard_history"]) > 100:
            self.data["leaderboard_history"] = self.data["leaderboard_history"][-100:]
        
        self.save_data()
        return snapshot
    
    def get_persistent_leaderboard(self) -> List[Dict]:
        """Get the most recent leaderboard snapshot"""
        if self.data["leaderboard_history"]:
            return self.data["leaderboard_history"][-1]["leaderboard"]
        return self.get_top_tickers(10)
    
    def add_idea(self, idea: str, user_id: int, username: str) -> Dict:
        """Add a new idea submission"""
        if not idea or not idea.strip():
            return {
                "success": False,
                "message": "Please provide an idea! 🙏"
            }
        
        # Ensure ideas list exists
        if "ideas" not in self.data:
            self.data["ideas"] = []
        
        idea_record = {
            "id": len(self.data["ideas"]) + 1,
            "idea": idea.strip(),
            "user_id": user_id,
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.data["ideas"].append(idea_record)
        self.save_data()
        
        return {
            "success": True,
            "message": f"💡 Idea submitted successfully! Thank you for your contribution!",
            "idea_id": idea_record["id"]
        }
    
    def get_all_ideas(self) -> List[Dict]:
        """Get all submitted ideas"""
        if "ideas" not in self.data:
            return []
        return self.data["ideas"]
    
    def get_ideas_by_user(self, user_id: int) -> List[Dict]:
        """Get ideas submitted by a specific user"""
        if "ideas" not in self.data:
            return []
        return [idea for idea in self.data["ideas"] if idea["user_id"] == user_id]

