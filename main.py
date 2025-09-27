

import asyncio
import logging
import os
import schedule
import time
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from config import BOT_TOKEN, ALLOWED_GROUP_ID, BIBLE_VERSES
from database import PrayerDatabase
from bible_service import BibleService
from image_service import ImageService
# Removed image overlay service - using text-only leaderboard

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize services
db = PrayerDatabase()
bible_service = BibleService()
image_service = ImageService()
# Removed overlay service - using text-only leaderboard

# Global variable to track the scheduled task
scheduled_task = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    if not is_allowed_group(update):
        return
    
    welcome_message = f"""
🙏 Welcome to the Crypto Church Bot! 🙏

This bot helps you pray for your favorite cryptocurrencies and receive spiritual guidance.

Available commands:
/pray <ticker> - Pray for a specific cryptocurrency ticker
/verse - Get a random Bible verse
/verse <reference> - Get a specific Bible verse (e.g., /verse John 3:16)
/chapter <book> <chapter> - Get entire chapter (e.g., /chapter Psalm 23)
/search <keywords> - Search for verses containing keywords
/jfc - Get a random image from the church collection
/stats - View prayer statistics
/leaderboard - View top 10 most prayed cryptocurrencies
/submitidea <idea> - Submit an idea for new features
/ideas - View all submitted ideas
/help - Show this help message

May your investments be blessed! ✝️
    """
    
    await update.message.reply_text(welcome_message.strip())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    if not is_allowed_group(update):
        return
    
    help_text = f"""
🙏 **Crypto Church Bot Commands** 🙏

**Prayer Commands:**
• `/pray <ticker>` - Pray for a cryptocurrency (e.g., `/pray BTC`)
• `/stats` - View your prayer statistics
• `/leaderboard` - View top 10 most prayed cryptocurrencies
# Removed leaderboardimage command

**Spiritual Commands:**
• `/verse` - Get a random Bible verse
• `/verse <reference>` - Get a specific Bible verse (e.g., `/verse John 3:16`)
• `/chapter <book> <chapter>` - Get entire chapter (e.g., `/chapter Psalm 23`)
• `/search <keywords>` - Search for verses containing keywords

**Fun Commands:**
• `/jfc` - Get a random image from the church collection

**Community Commands:**
• `/submitidea <idea>` - Submit an idea for new features
• `/ideas` - View all submitted ideas from the community

**Information:**
• `/help` - Show this help message
• `/start` - Welcome message

**Examples:**
• `/pray ETH` - Pray for Ethereum
• `/pray DOGE` - Pray for Dogecoin
• `/verse` - Get spiritual guidance
• `/verse Romans 8:28` - Get specific verse
• `/chapter Genesis 1` - Get first chapter of Genesis
• `/search love` - Search for verses about love
• `/submitidea Add crypto price alerts` - Submit a feature idea
• `/ideas` - View community suggestions

Remember: You can only pray for each ticker once per day! 🙏
    """
    
    await update.message.reply_text(help_text.strip(), parse_mode=ParseMode.MARKDOWN)

async def pray_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /pray command."""
    if not is_allowed_group(update):
        return
    
    if not context.args:
        await update.message.reply_text(
            "🙏 Please specify a ticker to pray for!\n\n"
            "Usage: `/pray <ticker>`\n"
            "Example: `/pray BTC`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    ticker = context.args[0].upper().strip()
    user = update.effective_user
    username = user.username or user.first_name or "Anonymous"
    
    # Add prayer to database
    result = db.add_prayer(ticker, user.id, username)
    
    if result["success"]:
        # Save leaderboard snapshot for persistence
        db.save_leaderboard_snapshot()
        
        await update.message.reply_text(
            f"🙏 {result['message']}\n\nBlessed be the Lord! ✝️"
        )
    else:
        await update.message.reply_text(result["message"])

async def verse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /verse command."""
    if not is_allowed_group(update):
        return
    
    if context.args:
        # Try to get specific verse by reference
        reference = " ".join(context.args)
        verse = bible_service.get_verse_by_reference(reference)
        if verse:
            await update.message.reply_text(
                f"📖 **{reference}**\n\n{verse}",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Fallback to random verse
            random_verse = bible_service.get_random_verse()
            await update.message.reply_text(
                f"📖 **Random Bible Verse**\n\n{random_verse}",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        # Get random verse
        random_verse = bible_service.get_random_verse()
        await update.message.reply_text(
            f"📖 **Random Bible Verse**\n\n{random_verse}",
            parse_mode=ParseMode.MARKDOWN
        )

async def chapter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /chapter command."""
    if not is_allowed_group(update):
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "📖 Please specify book and chapter!\n\n"
            "Usage: `/chapter <book> <chapter>`\n"
            "Examples:\n"
            "• `/chapter Psalm 23`\n"
            "• `/chapter Genesis 1`\n"
            "• `/chapter John 3`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        chapter_num = int(context.args[-1])
        book = " ".join(context.args[:-1])
        
        verse = bible_service.get_verse_by_chapter(book, chapter_num)
        if verse:
            await update.message.reply_text(
                f"📖 **{book} Chapter {chapter_num}**\n\n{verse}",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                f"📖 Could not find {book} Chapter {chapter_num}.\n\n"
                "Make sure the book name and chapter number are correct.",
                parse_mode=ParseMode.MARKDOWN
            )
    except ValueError:
        await update.message.reply_text(
            "📖 Invalid chapter number!\n\n"
            "Usage: `/chapter <book> <chapter>`\n"
            "Example: `/chapter Psalm 23`",
            parse_mode=ParseMode.MARKDOWN
        )

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /search command."""
    if not is_allowed_group(update):
        return
    
    if not context.args:
        await update.message.reply_text(
            "🔍 Please specify keywords to search for!\n\n"
            "Usage: `/search <keywords>`\n"
            "Examples:\n"
            "• `/search love`\n"
            "• `/search faith`\n"
            "• `/search hope`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    query = " ".join(context.args)
    results = bible_service.search_verses(query, limit=3)
    
    if results:
        search_text = f"🔍 **Search Results for: {query}**\n\n"
        for i, result in enumerate(results, 1):
            search_text += f"**{i}.** {result}\n\n"
        
        # Split long messages if needed
        if len(search_text) > 4000:
            parts = [search_text[i:i+4000] for i in range(0, len(search_text), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(search_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(
            f"🔍 No verses found containing '{query}'.\n\n"
            "Try different keywords or check your spelling.",
            parse_mode=ParseMode.MARKDOWN
        )

async def jfc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /jfc command."""
    if not is_allowed_group(update):
        return
    
    jfc_image_path = image_service.get_jfc_image()
    
    if jfc_image_path:
        try:
            # Send local image file using update.message.reply_photo
            with open(jfc_image_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
        except Exception as e:
            logger.error(f"Error sending JFC image: {e}")
            await update.message.reply_text(
                f"🎭 Random image requested! 🙏\n\n*Error: {str(e)}*",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        await update.message.reply_text(
            "🎭 Random image requested! 🙏\n\n*No images available at the moment*"
        )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /stats command."""
    if not is_allowed_group(update):
        return
    
    user = update.effective_user
    user_stats = db.get_user_stats(user.id)
    
    if user_stats:
        stats_text = f"""
📊 **Your Prayer Statistics** 📊

👤 **User:** {user_stats['username']}
🙏 **Total Prayers:** {user_stats['total_prayers']}
🪙 **Unique Tickers:** {len(user_stats['tickers_prayed_for'])}

**Tickers you've prayed for:**
{', '.join(user_stats['tickers_prayed_for'][:10])}{'...' if len(user_stats['tickers_prayed_for']) > 10 else ''}

Keep spreading the faith! 🙏✝️
        """
    else:
        stats_text = """
📊 **Your Prayer Statistics** 📊

🙏 You haven't prayed for any tickers yet!

Start your spiritual journey with `/pray <ticker>` ✝️
        """
    
    await update.message.reply_text(stats_text.strip(), parse_mode=ParseMode.MARKDOWN)

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /leaderboard command - shows persistent top 10 most prayed tickers."""
    if not is_allowed_group(update):
        return
    
    # Get persistent leaderboard data (survives bot restarts)
    top_tickers = db.get_persistent_leaderboard()
    
    if not top_tickers:
        await update.message.reply_text("🙏 No prayers recorded yet! Be the first to pray!")
        return
    
    # Create a nice formatted leaderboard matching your example
    leaderboard_text = "📜 **THE HOLY LEDGER** 📜\n\n"
    
    for i, ticker_data in enumerate(top_tickers, 1):
        leaderboard_text += f"{i}.  **${ticker_data['ticker']}**\n"
    
    leaderboard_text += "\n🙏 Keep praying for your favorite coins! ✝️"
    
    await update.message.reply_text(leaderboard_text, parse_mode=ParseMode.MARKDOWN)

# Removed leaderboard_image_command - using text-only leaderboard

async def global_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /globalstats command."""
    if not is_allowed_group(update):
        return
    
    total_stats = db.get_total_stats()
    
    stats_text = f"""
🌍 **Global Prayer Statistics** 🌍

🙏 **Total Prayers:** {total_stats['total_prayers']}
🪙 **Unique Tickers:** {total_stats['unique_tickers']}
👥 **Unique Users:** {total_stats['unique_users']}

The power of prayer is strong in this community! 🙏✝️
    """
    
    await update.message.reply_text(stats_text.strip(), parse_mode=ParseMode.MARKDOWN)

async def bible_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /biblestatus command to show Bible API status."""
    if not is_allowed_group(update):
        return
    
    api_available = bible_service.is_api_available()
    
    if api_available:
        status_text = """
📖 **Bible API Status** ✅

The Bible API is working and providing verses from the Scripture API.
You can use advanced commands like:
• `/verse <reference>` - Get specific verses
• `/chapter <book> <chapter>` - Get entire chapters
• `/search <keywords>` - Search for verses
        """
    else:
        status_text = """
📖 **Bible API Status** ❌

The Bible API is not available. This could be because:
• No API key provided in .env file
• API key is invalid
• Network connectivity issues

The bot will use built-in Bible verses instead.
        """
    
    await update.message.reply_text(status_text.strip(), parse_mode=ParseMode.MARKDOWN)

async def submit_idea_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /submitidea command."""
    if not is_allowed_group(update):
        return
    
    if not context.args:
        await update.message.reply_text(
            "💡 Please provide your idea!\n\n"
            "Usage: `/submitidea <your idea>`\n"
            "Example: `/submitidea Add a command to show crypto prices`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    idea = " ".join(context.args)
    user = update.effective_user
    username = user.username or user.first_name or "Anonymous"
    
    # Add idea to database
    result = db.add_idea(idea, user.id, username)
    
    if result["success"]:
        await update.message.reply_text(
            f"💡 **{result['message']}**\n\n"
            f"Idea ID: #{result['idea_id']}\n"
            f"Your idea: \"{idea}\"\n\n"
            f"Thank you for helping improve the bot! 🙏✝️",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(result["message"])

async def ideas_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /ideas command to show all submitted ideas."""
    if not is_allowed_group(update):
        return
    
    ideas = db.get_all_ideas()
    
    if not ideas:
        await update.message.reply_text(
            "💡 **Community Ideas** 💡\n\n"
            "No ideas submitted yet! Be the first to suggest a feature!\n\n"
            "Use `/submitidea <your idea>` to submit your suggestions! 🙏",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show latest 10 ideas
    recent_ideas = ideas[-10:] if len(ideas) > 10 else ideas
    
    ideas_text = "💡 **Community Ideas** 💡\n\n"
    
    for idea in reversed(recent_ideas):  # Show newest first
        ideas_text += f"**#{idea['id']}** - @{idea['username']}\n"
        ideas_text += f"💭 \"{idea['idea']}\"\n"
        ideas_text += f"📅 {idea['date']}\n\n"
    
    if len(ideas) > 10:
        ideas_text += f"... and {len(ideas) - 10} more ideas!\n\n"
    
    ideas_text += "Submit your ideas with `/submitidea <your idea>` 🙏"
    
    # Split long messages if needed
    if len(ideas_text) > 4000:
        parts = [ideas_text[i:i+4000] for i in range(0, len(ideas_text), 4000)]
        for part in parts:
            await update.message.reply_text(part, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(ideas_text, parse_mode=ParseMode.MARKDOWN)

async def clear_leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hidden admin command to clear leaderboard - only for @DarthMagician"""
    if not is_allowed_group(update):
        return
    
    # Check if user is @DarthMagician
    user = update.effective_user
    if user.username != "DarthMagician":
        await update.message.reply_text("❌ Access denied. This command is restricted.")
        return
    
    try:
        # Clear all prayer data
        db.data = {
            "prayers": {},
            "user_stats": {},
            "last_verse_time": None,
            "total_prayers": 0,
            "leaderboard_history": [],
            "ideas": []
        }
        db.save_data()
        
        await update.message.reply_text(
            "🗑️ **Leaderboard Cleared!**\n\n"
            "All prayer data has been reset.\n"
            "The leaderboard is now empty and ready for new prayers.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Leaderboard cleared by admin user: {user.username}")
        
    except Exception as e:
        logger.error(f"Error clearing leaderboard: {e}")
        await update.message.reply_text("❌ Error clearing leaderboard")


def is_allowed_group(update: Update) -> bool:
    """Check if the message is from the allowed group."""
    if not update.effective_chat:
        return False
    
    # Allow private messages for testing (remove in production)
    if update.effective_chat.type == "private":
        return True
    
    # Check if it's the allowed group
    return update.effective_chat.id == ALLOWED_GROUP_ID

async def send_scheduled_verse(context: ContextTypes.DEFAULT_TYPE):
    """Send a scheduled Bible verse every 2.5 hours."""
    try:
        if ALLOWED_GROUP_ID:
            verse = bible_service.get_random_verse()
            message = f"""
⏰ **Random Blessing** ⏰

{verse}

🙏✝️
            """
            
            await context.bot.send_message(
                chat_id=ALLOWED_GROUP_ID,
                text=message.strip(),
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Update last verse time
            db.set_last_verse_time(datetime.now().isoformat())
            logger.info("Scheduled verse sent successfully")
            
    except Exception as e:
        logger.error(f"Error sending scheduled verse: {e}")

def setup_scheduler(application: Application):
    """Set up the scheduler for periodic tasks."""
    global scheduled_task
    
    # Schedule verse every 2.5 hours
    schedule.every(2.5).hours.do(lambda: asyncio.create_task(send_scheduled_verse(application)))
    
    # Start scheduler in background
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("Scheduler started successfully")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Check if bot token is provided
    if not BOT_TOKEN:
        logger.error("No bot token provided! Please set BOT_TOKEN in your environment variables.")
        return
    
    if not ALLOWED_GROUP_ID:
        logger.warning("No group ID provided! Bot will work in all groups. Set ALLOWED_GROUP_ID to restrict access.")
    
    # Log Bible API status
    if bible_service.is_api_available():
        logger.info("Bible API is available and initialized successfully!")
    else:
        logger.warning("Bible API is not available. Bot will use built-in verses.")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pray", pray_command))
    application.add_handler(CommandHandler("verse", verse_command))
    application.add_handler(CommandHandler("chapter", chapter_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("jfc", jfc_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    # Removed leaderboardimage command handler
    application.add_handler(CommandHandler("globalstats", global_stats_command))
    application.add_handler(CommandHandler("biblestatus", bible_status_command))
    application.add_handler(CommandHandler("submitidea", submit_idea_command))
    application.add_handler(CommandHandler("ideas", ideas_command))
    application.add_handler(CommandHandler("clearleaderboard", clear_leaderboard_command))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Set up scheduler
    setup_scheduler(application)
    
    # Start the bot
    logger.info("Starting Crypto Church Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
