# 🎨 Obra Letra Font Setup for The Holy Ledger

## Quick Setup

To get the exact font styling from your example image, follow these steps:

### Option 1: Download and Install (Recommended)
1. **Download Obra Letra font** from a reputable font website
2. **Install the font** by double-clicking the downloaded file
3. **Restart the bot** - it will automatically detect the font

### Option 2: Manual Font Placement
1. **Download Obra Letra font** (TTF or OTF format)
2. **Rename the font file** to one of these names:
   - `ObraLetra.ttf`
   - `obra-letra.ttf`
   - `ObraLetra.otf`
   - `obra-letra.otf`
3. **Place the font file** in the `fonts/` directory
4. **Restart the bot**

## Font Detection Order

The bot will automatically look for the font in this order:
1. `fonts/ObraLetra.ttf`
2. `fonts/obra-letra.ttf`
3. `fonts/ObraLetra.otf`
4. `fonts/obra-letra.otf`
5. `C:/Windows/Fonts/obra-letra.ttf`
6. `C:/Windows/Fonts/ObraLetra.ttf`
7. **System default font** (fallback)

## Testing

After setting up the font:
1. Run `python test_video_generation.py` to test locally
2. Use `/holyledger` command in your Telegram bot
3. Check the generated video for proper font styling

## Expected Result

With Obra Letra font properly installed, your video will show:
- **"THE HOLY LEDGER"** title in elegant serif font
- **Numbered list** with tickers like `1.  $BTC`, `2.  $ETH`, etc.
- **Capital letters** for all ticker symbols
- **Proper spacing** between list items
- **Centered alignment** on the video overlay

## Troubleshooting

- **Font not loading?** Check the file name matches exactly
- **Still using default font?** Restart the bot after installing
- **Video not generating?** Check that OpenCV is installed: `pip install opencv-python`
