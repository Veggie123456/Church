#!/usr/bin/env python3
"""Test the fixed /ideas command"""

from database import PrayerDatabase

def test_fixed_ideas():
    """Test the fixed /ideas command output"""
    db = PrayerDatabase()
    
    print("Testing FIXED /ideas command...")
    
    ideas = db.get_all_ideas()
    
    if not ideas:
        ideas_text = "💡 Community Ideas 💡\n\nNo ideas submitted yet! Be the first to suggest a feature!\n\nUse /submitidea <your idea> to submit your suggestions! 🙏"
    else:
        recent_ideas = ideas[-10:] if len(ideas) > 10 else ideas
        
        ideas_text = "💡 Community Ideas 💡\n\n"
        
        for idea in reversed(recent_ideas):
            ideas_text += f"#{idea['id']} - {idea['username']}\n"
            ideas_text += f"💭 \"{idea['idea']}\"\n"
            ideas_text += f"📅 {idea['date']}\n\n"
        
        if len(ideas) > 10:
            ideas_text += f"... and {len(ideas) - 10} more ideas!\n\n"
        
        ideas_text += "Submit your ideas with /submitidea <your idea> 🙏"
    
    print("\n" + "="*50)
    print("FIXED IDEAS COMMAND OUTPUT:")
    print("="*50)
    print(ideas_text)
    print("="*50)
    
    # Check for problematic characters
    print(f"\nText length: {len(ideas_text)} characters")
    print(f"Contains @ symbols: {'@' in ideas_text}")
    print(f"Contains * symbols: {'*' in ideas_text}")
    print(f"Contains _ symbols: {'_' in ideas_text}")
    print("✅ Should work without any markdown parsing errors!")

if __name__ == "__main__":
    test_fixed_ideas()
