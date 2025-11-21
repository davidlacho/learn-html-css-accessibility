# Learn HTML, CSS & Accessible Web Design

An interactive, hands-on tutorial that teaches you the fundamentals of web development through building a webpage step by step. Complete in approximately 1.5 hours.

## 📚 About This Tutorial

This tutorial was built and designed by **Asher Lacho** for teaching workshops, but can be taken on its own as a self-paced learning experience. You'll learn HTML, CSS, and accessibility best practices through interactive lessons with real-time code verification and live preview.

## ✨ Features

- **Interactive Learning**: Write code and see it work in real-time
- **Live Preview**: See your webpage update as you type
- **Code Verification**: Get instant feedback on your code
- **Progress Tracking**: Track your progress through each section
- **Tooltips**: Hover over terms to see definitions
- **Hints Available**: Get help when you're stuck
- **Accessible Design**: The tutorial itself follows accessibility best practices
- **No Setup Required**: Works entirely in your browser

## 🎯 What You'll Learn

### HTML Fundamentals (4 lessons)
- Understanding HTML tags and structure
- Your first HTML tag
- HTML attributes (id, class, and more)
- Common HTML tags (div, span, strong, em)

### HTML (5 lessons)
- HTML document structure
- Headings and paragraphs
- Creating lists
- Adding links
- Adding images

### CSS (5 lessons)
- Introduction to CSS
- Styling text
- Backgrounds and borders
- Spacing with margin and padding
- CSS selectors (IDs and classes)

### Accessibility (6 lessons)
- Semantic HTML
- Alt text for images
- Proper heading hierarchy
- Keyboard navigation and focus
- ARIA labels and roles
- Additional accessibility features

**Total: 20 interactive lessons**

## 🚀 Getting Started

### Option 1: Run Local Web Server (Recommended)

Due to browser security (CORS), you need to run a local web server:

```bash
# Quick start - Python (no installation needed)
python3 server.py

# Or use Python's built-in server
python3 -m http.server 8000

# Then open: http://localhost:8000
```

**Note:** Opening `index.html` directly (double-click) will cause CORS errors. Use a server!

### Option 2: Create Standalone Version

For a single file that works without a server:

```bash
python3 embed_translations.py
# Opens: index-standalone.html
```

### Option 3: Use Local Server

For the best experience, you can run a local server:

```bash
# Using Python 3
python3 -m http.server 3000

# Using Python 2
python -m SimpleHTTPServer 3000

# Using Node.js (if you have http-server installed)
npx http-server -p 3000
```

Then open `http://localhost:3000/index.html` in your browser.

## 📖 How to Use This Tutorial

1. **Start**: Enter your name on the welcome screen
2. **Read**: Each lesson explains a concept with clear descriptions
3. **Code**: Write HTML and CSS in the code editor
4. **Preview**: See your code rendered in real-time
5. **Verify**: Click "Verify Code" to check if your solution is correct
6. **Learn**: Use hints and tooltips when you need help
7. **Progress**: Track your completion through each section
8. **Navigate**: Use "Skip" to move forward or "Back" to review

### Tips for Success

- **Read the descriptions carefully**: Each lesson explains why concepts are important
- **Use tooltips**: Hover over highlighted terms to see definitions
- **Check the preview**: Your code updates live as you type
- **Don't skip steps**: Each lesson builds on previous knowledge
- **Experiment**: Try different values and see what happens!

## 🛠️ Requirements

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- No coding experience required!
- No additional software or installations needed

## 🎓 Course Structure

The tutorial is organized into four main sections:

1. **HTML Fundamentals** - Learn the basics of HTML tags and structure
2. **HTML** - Build complete HTML documents with content
3. **CSS** - Style your webpages with colors, fonts, and layout
4. **Accessibility** - Make your websites usable by everyone

Each section builds on the previous one, so it's recommended to complete them in order.

## 💡 Key Concepts Covered

- HTML tags, elements, and attributes
- Document structure (`<html>`, `<head>`, `<body>`)
- Semantic HTML (`<header>`, `<main>`, `<nav>`, etc.)
- CSS selectors, properties, and values
- The CSS box model (margin, padding, border)
- ID and class selectors
- Accessibility best practices
- ARIA attributes
- Keyboard navigation
- Screen reader compatibility

## 🔗 Additional Resources

Each lesson includes links to relevant W3Schools tutorials for deeper learning. The tutorial also includes:

- Interactive tooltips for key terms
- Code templates to get you started
- Real-time validation and feedback
- Progress tracking

## 🧪 For Developers

This repository includes automated tests to ensure the tutorial works correctly.

### Running Tests

```bash
# Install dependencies
pip install -r test_requirements.txt

# Run all tests
pytest test_website.py test_modules.py -v

# Run with HTML report
pytest test_website.py test_modules.py -v --html=report.html
```

See `README_TESTING.md` for more details on testing.

## 📝 File Structure

```
learn-html-css/
├── index.html              # Main tutorial file (open this in your browser)
├── README.md               # This file
├── README_TESTING.md       # Testing documentation
├── test_website.py         # End-to-end tests
├── test_modules.py         # Module-specific tests
├── test_requirements.txt    # Python dependencies for tests
├── pytest.ini              # Pytest configuration
└── .gitignore              # Git ignore file
```

## 🙏 Credits

**Built and designed by Asher Lacho**

This tutorial was originally created for teaching workshops but is designed to be accessible as a standalone learning resource.

## 📄 License

This tutorial is provided as-is for educational purposes. Feel free to use it for learning or teaching web development.

## 🎉 Completion

When you complete all 20 lessons, you'll receive a certificate of completion! You'll have learned:

- How to structure HTML documents
- How to style webpages with CSS
- How to make websites accessible to everyone
- Best practices for web development

## 🤝 Contributing

If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## 📧 Support

If you encounter any problems or have questions while using this tutorial, please check:

1. That you're using a modern web browser
2. That JavaScript is enabled
3. The browser console for any error messages

---

**Happy Learning! 🚀**

Start your web development journey today by opening `index.html` in your browser.

