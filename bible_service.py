import random
import requests
from typing import Optional, List
from config import BIBLE_VERSES

class BibleService:
    def __init__(self):
        self.bible_verses = BIBLE_VERSES
        self.api_base = "https://bible-api.com"
    
    def get_random_verse(self) -> str:
        """Get a random Bible verse from bible-api.com"""
        try:
            # Try to get a random verse from bible-api.com
            api_verse = self._get_random_verse_from_api()
            if api_verse:
                return api_verse
        except Exception as e:
            print(f"Error getting random verse from API: {e}")
        
        # Fallback to built-in verses
        return random.choice(self.bible_verses)
    
    def _get_random_verse_from_api(self) -> Optional[str]:
        """Get a random verse from bible-api.com"""
        try:
            # bible-api.com doesn't have a random endpoint, so we'll pick from popular references
            popular_references = [
                "john3:16", "psalm23:1", "philippians4:13", "proverbs3:5",
                "matthew11:28", "isaiah40:31", "romans8:28", "jeremiah29:11",
                "joshua1:9", "psalm27:1", "galatians5:22", "ephesians2:8",
                "1corinthians13:4", "2timothy1:7", "hebrews11:1", "psalm91:1",
                "matthew6:33", "john14:27", "psalm118:24", "deuteronomy31:6"
            ]
            
            # Pick a random reference
            reference = random.choice(popular_references)
            response = requests.get(f"{self.api_base}/{reference}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # bible-api.com returns: {"reference": "...", "verses": [{"text": "..."}]}
                reference_name = data.get("reference", "")
                verses = data.get("verses", [])
                
                if verses and reference_name:
                    text = verses[0].get("text", "").strip()
                    if text:
                        return f"{text}\n\n- {reference_name}"
            
            return None
                
        except Exception as e:
            print(f"Error getting random verse from bible-api.com: {e}")
            return None
    
    def get_verse_by_reference(self, reference: str) -> Optional[str]:
        """Get a specific Bible verse by reference using bible-api.com"""
        try:
            # Use bible-api.com for specific verse references
            # Format: john 3:16 or jn 3:16
            formatted_ref = reference.lower().replace(" ", "")
            response = requests.get(f"{self.api_base}/{formatted_ref}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("text", "").strip()
                reference_name = data.get("reference", reference)
                
                if text:
                    return f"{text}\n\n- {reference_name}"
            
            return None
            
        except Exception as e:
            print(f"Error fetching Bible verse '{reference}': {e}")
            return None
    
    def get_verse_by_chapter(self, book: str, chapter: int) -> Optional[str]:
        """Get an entire chapter from the Bible using bible-api.com"""
        try:
            # Use bible-api.com for chapter requests
            # Format: psalms 23 or psalm 23
            formatted_ref = f"{book.lower()} {chapter}"
            response = requests.get(f"{self.api_base}/{formatted_ref}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                text = data.get("text", "").strip()
                reference_name = data.get("reference", f"{book} {chapter}")
                
                if text:
                    return f"**{reference_name}**\n\n{text}"
            
            return None
            
        except Exception as e:
            print(f"Error fetching Bible chapter '{book} {chapter}': {e}")
            return None
    
    def search_verses(self, query: str, limit: int = 5) -> List[str]:
        """Search for verses containing specific keywords using bible-api.com"""
        try:
            # Use bible-api.com search functionality
            # Note: bible-api.com doesn't have a direct search endpoint
            # We'll use popular references that might match the query
            popular_references = [
                "john 3:16", "psalm 23:1", "philippians 4:13", "proverbs 3:5",
                "matthew 11:28", "isaiah 40:31", "romans 8:28", "jeremiah 29:11",
                "joshua 1:9", "psalm 27:1", "galatians 5:22", "ephesians 2:8",
                "1 corinthians 13:4", "2 timothy 1:7", "hebrews 11:1"
            ]
            
            # Simple keyword matching - look for references that might contain the query
            query_lower = query.lower()
            matching_refs = []
            
            for ref in popular_references:
                if any(word in ref for word in query_lower.split()):
                    matching_refs.append(ref)
            
            # If no matches, return some random popular verses
            if not matching_refs:
                matching_refs = random.sample(popular_references, min(limit, len(popular_references)))
            
            results = []
            for ref in matching_refs[:limit]:
                verse = self.get_verse_by_reference(ref)
                if verse:
                    results.append(verse)
            
            return results
            
        except Exception as e:
            print(f"Error searching Bible verses for '{query}': {e}")
            return []
    
    def get_daily_verse(self) -> str:
        """Get a daily verse (same verse for the day)"""
        import datetime
        today = datetime.date.today()
        day_of_year = today.timetuple().tm_yday
        
        # Try API first, then fallback to built-in
        try:
            api_verse = self._get_daily_verse_from_api(day_of_year)
            if api_verse:
                return api_verse
        except Exception as e:
            print(f"Error getting daily verse from API: {e}")
        
        # Fallback to built-in verses
        verse_index = day_of_year % len(self.bible_verses)
        return self.bible_verses[verse_index]
    
    def _get_daily_verse_from_api(self, day_of_year: int) -> Optional[str]:
        """Get a daily verse from bible-api.com based on day of year"""
        try:
            # Use day of year to select from popular references
            popular_references = [
                "john 3:16", "psalm 23:1", "philippians 4:13", "proverbs 3:5",
                "matthew 11:28", "isaiah 40:31", "romans 8:28", "jeremiah 29:11",
                "joshua 1:9", "psalm 27:1", "galatians 5:22", "ephesians 2:8",
                "1 corinthians 13:4", "2 timothy 1:7", "hebrews 11:1"
            ]
            
            reference_index = day_of_year % len(popular_references)
            reference = popular_references[reference_index]
            
            return self.get_verse_by_reference(reference)
            
        except Exception as e:
            print(f"Error getting daily verse from API: {e}")
            return None
    
    def get_encouraging_verse(self) -> str:
        """Get an encouraging verse for crypto prayers"""
        try:
            # Try to get encouraging verses from bible-api.com
            encouraging_references = [
                "philippians 4:13", "isaiah 40:31", "joshua 1:9", "psalm 27:1",
                "romans 8:28", "jeremiah 29:11", "2 timothy 1:7"
            ]
            
            for reference in encouraging_references:
                verse = self.get_verse_by_reference(reference)
                if verse:
                    return verse
        except Exception as e:
            print(f"Error getting encouraging verse from API: {e}")
        
        # Fallback to built-in encouraging verses
        encouraging_verses = [
            "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life. - John 3:16",
            "I can do all things through Christ which strengtheneth me. - Philippians 4:13",
            "Trust in the LORD with all thine heart; and lean not unto thine own understanding. - Proverbs 3:5",
            "The LORD is my shepherd; I shall not want. - Psalm 23:1",
            "Be strong and of a good courage, fear not, nor be afraid of them: for the LORD thy God, he it is that doth go with thee; he will not fail thee, nor forsake thee. - Deuteronomy 31:6"
        ]
        return random.choice(encouraging_verses)
    
    def is_api_available(self) -> bool:
        """Check if Bible API is available and working"""
        try:
            # Test if bible-api.com is accessible with a simple verse
            response = requests.get(f"{self.api_base}/john3:16", timeout=5)
            return response.status_code == 200
        except:
            return False
