import os
import tempfile
from typing import List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from database import PrayerDatabase

class VideoService:
    def __init__(self):
        self.db = PrayerDatabase()
        self.video_path = "Picturesforchurch/Your paragrThe Holy Ledgeraph text.mp4"
        
    def create_leaderboard_video(self, top_tickers: List[Dict], output_path: Optional[str] = None) -> Optional[str]:
        """Create a video with leaderboard data overlaid on the base video"""
        try:
            if not os.path.exists(self.video_path):
                print(f"Base video not found: {self.video_path}")
                return None
            
            # Set up video capture
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                print("Error opening video file")
                return None
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Set up video writer
            if output_path is None:
                output_path = "Picturesforchurch/holy_ledger_leaderboard.mp4"
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Add leaderboard overlay to frame
                frame_with_overlay = self._add_leaderboard_overlay(frame, top_tickers, frame_count, total_frames)
                out.write(frame_with_overlay)
                frame_count += 1
            
            # Release everything
            cap.release()
            out.release()
            
            print(f"Leaderboard video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating leaderboard video: {e}")
            return None
    
    def _add_leaderboard_overlay(self, frame: np.ndarray, top_tickers: List[Dict], frame_count: int, total_frames: int) -> np.ndarray:
        """Add leaderboard overlay to a single frame"""
        try:
            # Convert BGR to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            draw = ImageDraw.Draw(pil_image)
            
            # Calculate overlay position and size - center the overlay
            overlay_width = 500
            overlay_height = 600
            overlay_x = (frame.shape[1] - overlay_width) // 2  # Center horizontally
            overlay_y = (frame.shape[0] - overlay_height) // 2  # Center vertically
            
            # Try to load Obra Letra font, fallback to default if not available
            try:
                # Try different possible paths for fonts (Obra Letra first, then free alternatives)
                font_paths = [
                    "fonts/ObraLetra.ttf",
                    "fonts/obra-letra.ttf", 
                    "fonts/ObraLetra.otf",
                    "fonts/obra-letra.otf",
                    "fonts/CrimsonText-Regular.ttf",  # Free elegant serif
                    "fonts/LibreBaskerville-Regular.ttf",  # Free classic serif
                    "C:/Windows/Fonts/obra-letra.ttf",
                    "C:/Windows/Fonts/ObraLetra.ttf",
                    "C:/Windows/Fonts/CrimsonText-Regular.ttf",
                    "C:/Windows/Fonts/LibreBaskerville-Regular.ttf"
                ]
                
                title_font = None
                list_font = None
                
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        title_font = ImageFont.truetype(font_path, 48)  # Larger title font
                        list_font = ImageFont.truetype(font_path, 32)   # Larger list font
                        if frame_count == 0:
                            print(f"✅ Using font: {font_path}")
                        break
                
                if title_font is None:
                    # Fallback to default font
                    title_font = ImageFont.load_default()
                    list_font = ImageFont.load_default()
                    # Only print once per video generation
                    if frame_count == 0:
                        print("Obra Letra font not found, using default font")
                    
            except Exception as e:
                print(f"Font loading error: {e}")
                title_font = ImageFont.load_default()
                list_font = ImageFont.load_default()
            
            # Draw title - centered at the top
            title_text = "THE HOLY LEDGER"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = overlay_x + (overlay_width - title_width) // 2
            draw.text((title_x, overlay_y + 30), title_text, fill='white', font=title_font)
            
            # Draw leaderboard - centered and properly spaced
            y_offset = overlay_y + 120  # Start below title
            for i, ticker_data in enumerate(top_tickers[:10], 1):
                # Format ticker in capital letters with $ symbol like the example
                ticker_symbol = f"${ticker_data['ticker'].upper()}"
                
                # Draw rank number and ticker symbol
                rank_text = f"{i}.  {ticker_symbol}"
                
                # Center the text horizontally
                text_bbox = draw.textbbox((0, 0), rank_text, font=list_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = overlay_x + (overlay_width - text_width) // 2
                
                draw.text((text_x, y_offset), rank_text, fill='white', font=list_font)
                
                # Increase spacing between items for better readability
                y_offset += 50
            
            # Convert back to BGR for OpenCV
            frame_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return frame_bgr
            
        except Exception as e:
            print(f"Error adding overlay to frame: {e}")
            return frame
    
    def get_leaderboard_video(self) -> Optional[str]:
        """Get or create the latest leaderboard video with live, updated data"""
        try:
            # Get the most current top tickers from database (always fresh data)
            top_tickers = self.db.get_top_tickers(10)
            
            if not top_tickers:
                print("No ticker data available for leaderboard")
                return None
            
            print(f"📊 Generating video with live data: {len(top_tickers)} tickers")
            for i, ticker in enumerate(top_tickers[:5], 1):
                print(f"  {i}. {ticker['ticker']} - {ticker['count']} prayers")
            
            # Create the video with current data
            output_path = self.create_leaderboard_video(top_tickers)
            return output_path
            
        except Exception as e:
            print(f"Error getting leaderboard video: {e}")
            return None
    
    def create_static_leaderboard_image(self, top_tickers: List[Dict]) -> Optional[str]:
        """Create a static leaderboard image for preview"""
        try:
            # Create a new image with the same style as the video overlay
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color=(20, 30, 60))  # Dark blue background
            draw = ImageDraw.Draw(image)
            
            # Try to load Obra Letra font
            try:
                font_paths = [
                    "fonts/ObraLetra.ttf",
                    "fonts/obra-letra.ttf", 
                    "fonts/ObraLetra.otf",
                    "fonts/obra-letra.otf",
                    "fonts/CrimsonText-Regular.ttf",  # Free elegant serif
                    "fonts/LibreBaskerville-Regular.ttf",  # Free classic serif
                    "C:/Windows/Fonts/obra-letra.ttf",
                    "C:/Windows/Fonts/ObraLetra.ttf",
                    "C:/Windows/Fonts/CrimsonText-Regular.ttf",
                    "C:/Windows/Fonts/LibreBaskerville-Regular.ttf"
                ]
                
                title_font = None
                list_font = None
                
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        title_font = ImageFont.truetype(font_path, 48)
                        list_font = ImageFont.truetype(font_path, 32)
                        print(f"✅ Using font for static image: {font_path}")
                        break
                
                if title_font is None:
                    title_font = ImageFont.load_default()
                    list_font = ImageFont.load_default()
                    
            except Exception as e:
                print(f"Font loading error: {e}")
                title_font = ImageFont.load_default()
                list_font = ImageFont.load_default()
            
            # Draw title - centered
            title_text = "THE HOLY LEDGER"
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 50), title_text, fill='white', font=title_font)
            
            # Draw leaderboard - centered and properly spaced like the example
            y_offset = 150
            for i, ticker_data in enumerate(top_tickers[:10], 1):
                # Format ticker in capital letters with $ symbol like the example
                ticker_symbol = f"${ticker_data['ticker'].upper()}"
                
                # Draw rank number and ticker symbol
                rank_text = f"{i}.  {ticker_symbol}"
                
                # Center the text horizontally
                text_bbox = draw.textbbox((0, 0), rank_text, font=list_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (width - text_width) // 2
                
                draw.text((text_x, y_offset), rank_text, fill='white', font=list_font)
                
                # Increase spacing between items for better readability
                y_offset += 50
            
            # Save image
            output_path = "Picturesforchurch/holy_ledger_preview.png"
            image.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error creating static leaderboard image: {e}")
            return None
