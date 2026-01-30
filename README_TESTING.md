# Testing Guide

This directory contains comprehensive Selenium tests for the HTML/CSS Learning Website.

## Setup

1. Install Python dependencies:
```bash
pip install -r test_requirements.txt
```

2. Run the tests (no need to start the server manually):
```bash
# Run all tests — the web server is started automatically (conftest.py)
pytest -v

# Run core tests only (faster)
pytest test_website.py test_translations.py -v

# Run with HTML report
pytest -v --html=report.html --self-contained-html

# Run specific test file
pytest test_website.py -v

# Run specific test
pytest test_website.py::TestWebsite::test_welcome_screen_loads -v
```

The test suite starts the local server (`python3 server.py`) on port 8000 automatically when needed. To use an already-running server, set `BASE_URL` (e.g. `BASE_URL=http://localhost:8000 pytest -v`).

## Test Coverage

### test_website.py
Tests all core functionality:
- Welcome screen and user input
- Tooltips (welcome screen and lessons)
- Name input and lesson start
- Course progress navigation
- Hint button toggle
- Code editor functionality
- Code verification
- Navigation buttons (Next, Back, Skip)
- External links (W3Schools)
- Preview panel
- Progress tracking
- URL persistence

### test_modules.py
Tests each module comprehensively:
- **HTML Fundamentals** (4 lessons)
- **HTML** (5 lessons)
- **CSS** (5 lessons)
- **Accessibility** (6 lessons)

Each module test:
- Navigates through all lessons in the module
- Tests tooltips in each lesson
- Tests hint buttons
- Tests code editor
- Tests code verification
- Tests navigation between lessons
- Verifies all external links

## Test Structure

Tests use:
- **Selenium WebDriver** for browser automation
- **pytest** for test framework
- **ChromeDriver** (managed by webdriver-manager)

## Running Tests in CI/CD

For headless operation (CI/CD), tests automatically run in headless mode. The GitHub workflow starts the server before pytest. Make sure:
1. Chrome/Chromium is installed
2. Port 8000 is available (or set `BASE_URL` to your server URL)

## Troubleshooting

If tests fail:
1. If you see "Web server did not start in time", start the server manually: `python3 server.py` (port 8000), then run pytest again. Or set `BASE_URL=http://localhost:8000` if the server is already running.
2. Check that Chrome/Chromium is installed (required for Selenium tests).
3. Verify all dependencies are installed: `pip install -r test_requirements.txt`
4. Check browser console for JavaScript errors
5. Run tests with `-v` flag for verbose output

## Test Reports

HTML reports are generated with `--html=report.html`. Open the report in a browser to see detailed test results.

