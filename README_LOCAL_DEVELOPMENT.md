# Local Development Guide

## CORS Issue with Local Files

When opening `index.html` directly in a browser (`file://`), you'll get CORS errors because browsers block `fetch()` requests to local files for security reasons.

## Solution: Run a Local Web Server

Choose one of these methods:

### Option 1: Python Simple Server (Recommended - No Installation)

```bash
# Python 3
python3 -m http.server 8000

# Then open: http://localhost:8000
```

### Option 2: Node.js http-server

```bash
# Install once
npm install -g http-server

# Run server
http-server -p 8000

# Then open: http://localhost:8000
```

### Option 3: PHP Built-in Server

```bash
php -S localhost:8000

# Then open: http://localhost:8000
```

### Option 4: VS Code Live Server Extension

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"

## For Production/Distribution

If you want to distribute a single HTML file that works without a server, run:

```bash
python3 embed_translations.py
```

This will create `index-standalone.html` with embedded translations that works when opened directly.

## File Structure

```
learn-html-css/
├── index.html              → Main app (requires server)
├── styles.css              → All styles
├── translations.json       → Single source of truth for content
├── embed_translations.py   → Script to create standalone version
└── server.py              → Simple server script
```

## Quick Start

```bash
# Navigate to project directory
cd /Users/david/learn-html-css

# Start server
python3 -m http.server 8000

# Open browser
open http://localhost:8000
```

