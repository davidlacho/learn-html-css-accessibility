#!/usr/bin/env python3
"""
Create a standalone version of index.html with embedded translations.
This version can be opened directly in a browser without a server.

Usage:
    python3 embed_translations.py

Output:
    index-standalone.html (single file that works without a server)
"""

import json
import re

print("=" * 80)
print("Creating standalone version with embedded translations...")
print("=" * 80)

# Read files
with open('index.html', 'r') as f:
    html_content = f.read()

with open('translations.json', 'r') as f:
    translations_data = json.load(f)

# Find the fetch code block and replace it with embedded translations
pattern = r"// Load translations from external JSON file\s+let translations = \{\};\s+let translationsLoaded = false;\s+// Load translations\.json\s+fetch\('translations\.json'\)[\s\S]*?\}\);"

embedded_code = f"""// Embedded translations (standalone version)
        const translations = {json.dumps(translations_data, indent=10, ensure_ascii=False)};
        const translationsLoaded = true;"""

# Replace fetch code with embedded translations
new_content = re.sub(pattern, embedded_code, html_content)

# Write standalone version
with open('index-standalone.html', 'w') as f:
    f.write(new_content)

# Get file sizes
import os
original_size = os.path.getsize('index.html')
standalone_size = os.path.getsize('index-standalone.html')
trans_size = os.path.getsize('translations.json')

print(f"\n✅ Created: index-standalone.html")
print(f"\n📊 File Sizes:")
print(f"   index.html (requires server):  {original_size:>8,} bytes ({original_size/1024:>6.1f} KB)")
print(f"   index-standalone.html:         {standalone_size:>8,} bytes ({standalone_size/1024:>6.1f} KB)")
print(f"   translations.json:             {trans_size:>8,} bytes ({trans_size/1024:>6.1f} KB)")

print(f"\n💡 Usage:")
print(f"   • index.html: Use with a local server (python3 -m http.server)")
print(f"   • index-standalone.html: Can be opened directly (double-click)")

print(f"\n✅ Done!")
print("=" * 80)

