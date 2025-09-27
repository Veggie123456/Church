import random
import os
from PIL import Image, ImageDraw, ImageFont
import io
from typing import Optional

class ImageService:
    def __init__(self):
        # Local images from Picturesforchurch folder
        self.local_images = [
            "Picturesforchurch/artworks-000615487375-ao6j42-t500x500.jpg",
            "Picturesforchurch/image.png"
        ]
        
        # Filter to only existing images
        self.available_images = [img for img in self.local_images if os.path.exists(img)]
    
    def get_jfc_image(self) -> Optional[str]:
        """Get a random local image from Picturesforchurch folder"""
        if self.available_images:
            return random.choice(self.available_images)
        return None
    
    def get_prayer_image(self) -> Optional[str]:
        """Get a random prayer-related image URL"""
        if self.prayer_images:
            return random.choice(self.prayer_images)
        return None
    
    def create_prayer_card(self, ticker: str, prayer_count: int, username: str) -> Optional[bytes]:
        """Create a custom prayer card image"""
        try:
            # Create a new image with white background
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Try to use a default font, fallback to basic if not available
            try:
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_medium = ImageFont.truetype("arial.ttf", 32)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title = "🙏 Prayer Card"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 50), title, fill='black', font=font_large)
            
            # Draw ticker
            ticker_text = f"Ticker: {ticker}"
            ticker_bbox = draw.textbbox((0, 0), ticker_text, font=font_medium)
            ticker_width = ticker_bbox[2] - ticker_bbox[0]
            ticker_x = (width - ticker_width) // 2
            draw.text((ticker_x, 150), ticker_text, fill='blue', font=font_medium)
            
            # Draw prayer count
            count_text = f"Total Prayers: {prayer_count}"
            count_bbox = draw.textbbox((0, 0), count_text, font=font_medium)
            count_width = count_bbox[2] - count_bbox[0]
            count_x = (width - count_width) // 2
            draw.text((count_x, 220), count_text, fill='green', font=font_medium)
            
            # Draw username
            user_text = f"Prayed by: {username}"
            user_bbox = draw.textbbox((0, 0), user_text, font=font_small)
            user_width = user_bbox[2] - user_bbox[0]
            user_x = (width - user_width) // 2
            draw.text((user_x, 300), user_text, fill='gray', font=font_small)
            
            # Draw decorative elements
            draw.rectangle([50, 400, width-50, 450], outline='gold', width=3)
            draw.text((width//2-100, 410), "Blessed Be The Lord", fill='gold', font=font_small)
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            print(f"Error creating prayer card: {e}")
            return None
    
    def create_stats_image(self, stats_data: dict) -> Optional[bytes]:
        """Create a statistics image"""
        try:
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            try:
                font_large = ImageFont.truetype("arial.ttf", 36)
                font_medium = ImageFont.truetype("arial.ttf", 24)
                font_small = ImageFont.truetype("arial.ttf", 18)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Title
            title = "📊 Prayer Statistics"
            title_bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 30), title, fill='black', font=font_large)
            
            # Stats
            y_position = 100
            for key, value in stats_data.items():
                if key == "top_tickers":
                    draw.text((50, y_position), "Top Tickers:", fill='blue', font=font_medium)
                    y_position += 40
                    for i, ticker in enumerate(value[:5]):
                        ticker_text = f"{i+1}. {ticker['ticker']}: {ticker['count']} prayers"
                        draw.text((70, y_position), ticker_text, fill='black', font=font_small)
                        y_position += 25
                else:
                    text = f"{key.replace('_', ' ').title()}: {value}"
                    draw.text((50, y_position), text, fill='black', font=font_medium)
                    y_position += 40
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            print(f"Error creating stats image: {e}")
            return None

