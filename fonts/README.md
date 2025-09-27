# Fonts Directory

## Obra Letra Font Setup

To use the Obra Letra font for "The Holy Ledger" video generation, please follow these steps:

### Option 1: Download and Install (Recommended)
1. Download the Obra Letra font from a reputable font website
2. Install it on your system (usually by double-clicking the font file)
3. The bot will automatically detect it in the Windows Fonts directory

### Option 2: Place Font File Here
1. Download the Obra Letra font file (TTF or OTF format)
2. Rename it to one of these names:
   - `ObraLetra.ttf`
   - `obra-letra.ttf`
   - `ObraLetra.otf`
   - `obra-letra.otf`
3. Place the font file in this `fonts/` directory

### Supported Font Formats
- `.ttf` (TrueType Font)
- `.otf` (OpenType Font)

### Fallback
If the Obra Letra font is not found, the bot will automatically use the system default font as a fallback.

### Font Detection Order
The bot will look for the font in this order:
1. `fonts/ObraLetra.ttf`
2. `fonts/obra-letra.ttf`
3. `fonts/ObraLetra.otf`
4. `fonts/obra-letra.otf`
5. `C:/Windows/Fonts/obra-letra.ttf`
6. `C:/Windows/Fonts/ObraLetra.ttf`
7. System default font (fallback)
