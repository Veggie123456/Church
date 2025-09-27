import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ALLOWED_GROUP_ID = int(os.getenv('ALLOWED_GROUP_ID', 0))

# Bible API Configuration - Using bible-api.com (no API key required)

# Database file path
DB_FILE = 'prayer_data.json'

# Bible verses for random selection (King James Version)
BIBLE_VERSES = [
    "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life. - John 3:16",
    "I can do all things through Christ which strengtheneth me. - Philippians 4:13",
    "Trust in the LORD with all thine heart; and lean not unto thine own understanding. - Proverbs 3:5",
    "The LORD is my shepherd; I shall not want. - Psalm 23:1",
    "Be strong and of a good courage, fear not, nor be afraid of them: for the LORD thy God, he it is that doth go with thee; he will not fail thee, nor forsake thee. - Deuteronomy 31:6",
    "But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint. - Isaiah 40:31",
    "Come unto me, all ye that labour and are heavy laden, and I will give you rest. - Matthew 11:28",
    "Let not your heart be troubled, neither let it be afraid. - John 14:27",
    "This is the day which the LORD hath made; we will rejoice and be glad in it. - Psalm 118:24",
    "The LORD is my light and my salvation; whom shall I fear? the LORD is the strength of my life; of whom shall I be afraid? - Psalm 27:1"
]

