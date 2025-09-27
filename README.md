# 🙏 Crypto Church Bot

A Telegram bot that helps users pray for their favorite cryptocurrencies and receive spiritual guidance.

## Features

- **Prayer System**: Track prayers for different cryptocurrency tickers
- **Leaderboard**: "THE HOLY LEDGER" showing most prayed cryptocurrencies
- **Bible Integration**: Random verses, specific references, chapter reading, and search
- **Random Images**: JFC command shows random images from church collection
- **Scheduled Blessings**: Automatic random Bible verses every 2.5 hours
- **Admin Commands**: Hidden clear leaderboard function for administrators

## Commands

### Prayer Commands
- `/pray <ticker>` - Pray for a cryptocurrency (e.g., `/pray BTC`)
- `/stats` - View your personal prayer statistics
- `/leaderboard` - View "THE HOLY LEDGER" - top 10 most prayed cryptocurrencies

### Spiritual Commands
- `/verse` - Get a random Bible verse
- `/verse <reference>` - Get a specific Bible verse (e.g., `/verse John 3:16`)
- `/chapter <book> <chapter>` - Get entire chapter (e.g., `/chapter Psalm 23`)
- `/search <keywords>` - Search for verses containing keywords

### Fun Commands
- `/jfc` - Get a random image from the church collection

### Information Commands
- `/help` - Show complete command list
- `/start` - Welcome message and bot introduction
- `/globalstats` - View global prayer statistics
- `/biblestatus` - Check if Bible API is working

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```
   BOT_TOKEN=your_telegram_bot_token
   ALLOWED_GROUP_ID=your_telegram_group_id
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

## Deployment

This bot is ready for deployment on Railway, Heroku, or any Python hosting platform.

## Files

- `main.py` - Main bot application
- `database.py` - Prayer data persistence
- `bible_service.py` - Bible API integration
- `image_service.py` - Image handling
- `config.py` - Configuration management
- `prayer_data.json` - Prayer data storage
- `Picturesforchurch/` - Image collection folder

## License

This project is for educational and spiritual purposes.