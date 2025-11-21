"""
Module-specific tests for each lesson category
Tests HTML Fundamentals, HTML, CSS, and Accessibility modules
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestLessonModules:
    """Test each lesson module comprehensively"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome driver"""
        import os
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Use new headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Try multiple methods to get ChromeDriver
        driver = None
        try:
            # Method 1: Try webdriver-manager
            driver_path = ChromeDriverManager().install()
            # Check if it's a directory and find the executable
            if os.path.isdir(driver_path):
                for root, dirs, files in os.walk(driver_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if 'chromedriver' in file.lower() and os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                            # Check it's actually executable (not a text file)
                            if not file.endswith(('.txt', '.md', '.pdf')):
                                driver_path = full_path
                                break
            if os.path.isfile(driver_path) and os.access(driver_path, os.X_OK):
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            pass
        
        # Method 2: Try system ChromeDriver
        if driver is None:
            try:
                driver = webdriver.Chrome(options=chrome_options)
            except Exception:
                pass
        
        # Method 3: Try finding chromedriver in common locations
        if driver is None:
            common_paths = [
                '/usr/local/bin/chromedriver',
                '/opt/homebrew/bin/chromedriver',
                os.path.expanduser('~/chromedriver'),
            ]
            for path in common_paths:
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    try:
                        service = Service(path)
                        driver = webdriver.Chrome(service=service, options=chrome_options)
                        break
                    except Exception:
                        continue
        
        if driver is None:
            pytest.skip("Could not initialize ChromeDriver. Please install ChromeDriver or Chrome browser.")
        
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="class")
    def base_url(self):
        """Base URL for the website"""
        return "http://localhost:8000/index.html"
    
    def start_lesson(self, driver, base_url):
        """Helper to start a lesson session"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 15)
        
        name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        name_input.clear()
        name_input.send_keys("Test User")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Start Learning')]").click()
        # Wait for lesson to load - check for lesson content or h2 heading
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2")),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".lesson-content")),
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome')]"))
            )
        )
        time.sleep(1)  # Give React time to fully render
        return wait
    
    def navigate_to_section(self, driver, wait, section_name):
        """Helper to navigate to a specific section"""
        try:
            # Wait for progress section to be visible
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Course Progress')]")))
            time.sleep(0.5)
            
            # Try different XPath patterns for section buttons
            section_button = None
            patterns = [
                f"//button[contains(@aria-label, '{section_name}')]",
                f"//button[contains(., '{section_name}')]",
                f"//*[@role='button' and contains(., '{section_name}')]"
            ]
            
            for pattern in patterns:
                try:
                    section_button = wait.until(EC.element_to_be_clickable((By.XPATH, pattern)))
                    break
                except TimeoutException:
                    continue
            
            if section_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", section_button)
                time.sleep(0.3)
                section_button.click()
                time.sleep(1.5)  # Wait for navigation
                return True
            return False
        except (TimeoutException, NoSuchElementException):
            return False
    
    def test_html_fundamentals_module(self, driver, base_url):
        """Test HTML Fundamentals module (4 lessons)"""
        wait = self.start_lesson(driver, base_url)
        
        # Navigate to HTML Fundamentals
        assert self.navigate_to_section(driver, wait, "HTML Fundamentals"), "Could not navigate to HTML Fundamentals"
        
        # Test each lesson in HTML Fundamentals
        for lesson_num in range(4):
            try:
                # Get lesson title
                lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
                assert lesson_title.is_displayed(), f"Lesson {lesson_num + 1} title not displayed"
                
                # Test tooltips
                tooltip_buttons = driver.find_elements(By.CSS_SELECTOR, ".tooltip-wrapper, button[role='button'][aria-describedby]")
                if tooltip_buttons:
                    tooltip_buttons[0].click()
                    time.sleep(0.3)
                
                # Test hint button
                try:
                    hint_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show hint') or contains(text(), 'Hide hint')]")
                    hint_button.click()
                    time.sleep(0.3)
                    hint_button.click()  # Toggle back
                    time.sleep(0.3)
                except NoSuchElementException:
                    pass  # Hint button not always present
                
                # Test code editor
                code_editor = driver.find_element(By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']")
                code_editor.clear()
                
                # Enter appropriate code based on lesson
                if lesson_num == 0:  # Understanding HTML Tags
                    code_editor.clear()
                    code_editor.send_keys("<div>Test</div>")
                elif lesson_num == 1:  # Your First HTML Tag
                    code_editor.clear()
                    code_editor.send_keys("<p>Hello World</p>")
                elif lesson_num == 2:  # Understanding HTML Attributes - now requires both id and class
                    code_editor.clear()
                    code_editor.send_keys('<p>This is a paragraph</p>\n<div id="myDiv">Content</div>\n<div class="container">More content</div>')
                else:  # Common HTML Tags - now requires div with class
                    code_editor.clear()
                    code_editor.send_keys('<p>This is a paragraph</p>\n<div class="container">Test</div><span>Inline</span><strong>Bold</strong>')
                
                # Verify code
                verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify Code')]")
                verify_button.click()
                time.sleep(1)
                
                # Check for success or move to next
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next Lesson')]"))
                    )
                    next_button.click()
                    time.sleep(1)
                except TimeoutException:
                    # If no next button, try skip
                    try:
                        skip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Skip')]")
                        skip_button.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        break  # No more lessons
                        
            except (TimeoutException, NoSuchElementException) as e:
                pytest.fail(f"Error in HTML Fundamentals lesson {lesson_num + 1}: {str(e)}")
    
    def test_html_module(self, driver, base_url):
        """Test HTML module (5 lessons)"""
        wait = self.start_lesson(driver, base_url)
        
        # Navigate to HTML section
        assert self.navigate_to_section(driver, wait, "HTML section"), "Could not navigate to HTML section"
        
        # Test lessons in HTML module
        for lesson_num in range(5):
            try:
                lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
                assert lesson_title.is_displayed(), f"HTML lesson {lesson_num + 1} title not displayed"
                
                # Test all interactive elements
                # Tooltips
                tooltip_buttons = driver.find_elements(By.CSS_SELECTOR, ".tooltip-wrapper, button[role='button'][aria-describedby]")
                if tooltip_buttons:
                    tooltip_buttons[0].click()
                    time.sleep(0.3)
                
                # Hint
                try:
                    hint_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show hint') or contains(text(), 'Hide hint')]")
                    hint_button.click()
                    time.sleep(0.3)
                except NoSuchElementException:
                    pass
                
                # Code editor
                code_editor = driver.find_element(By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']")
                code_editor.clear()
                
                # Enter appropriate code
                if lesson_num == 0:  # HTML Document Structure
                    code_editor.send_keys("<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>")
                elif lesson_num == 1:  # Adding Content
                    code_editor.send_keys("<html><head><title>Test</title></head><body><h1>Title</h1><p>Paragraph</p></body></html>")
                else:
                    code_editor.send_keys("<html><head><title>Test</title></head><body><h1>Test</h1></body></html>")
                
                # Verify
                verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify Code')]")
                verify_button.click()
                time.sleep(1)
                
                # Navigate to next
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next Lesson')]"))
                    )
                    next_button.click()
                    time.sleep(1)
                except TimeoutException:
                    try:
                        skip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Skip')]")
                        skip_button.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        break
                        
            except (TimeoutException, NoSuchElementException) as e:
                pytest.fail(f"Error in HTML lesson {lesson_num + 1}: {str(e)}")
    
    def test_css_module(self, driver, base_url):
        """Test CSS module (5 lessons)"""
        wait = self.start_lesson(driver, base_url)
        
        # Navigate to CSS section
        assert self.navigate_to_section(driver, wait, "CSS section"), "Could not navigate to CSS section"
        
        # Test lessons in CSS module
        for lesson_num in range(5):
            try:
                lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
                assert lesson_title.is_displayed(), f"CSS lesson {lesson_num + 1} title not displayed"
                
                # Test interactive elements
                tooltip_buttons = driver.find_elements(By.CSS_SELECTOR, ".tooltip-wrapper, button[role='button'][aria-describedby]")
                if tooltip_buttons:
                    tooltip_buttons[0].click()
                    time.sleep(0.3)
                
                try:
                    hint_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show hint') or contains(text(), 'Hide hint')]")
                    hint_button.click()
                    time.sleep(0.3)
                except NoSuchElementException:
                    pass
                
                # Code editor with CSS
                code_editor = driver.find_element(By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']")
                code_editor.clear()
                
                # Enter CSS code
                if lesson_num == 0:  # Introduction to CSS
                    code_editor.send_keys("<html><head><style>body { color: blue; }</style></head><body><h1>Test</h1></body></html>")
                else:
                    code_editor.send_keys("<html><head><style>body { color: blue; font-size: 16px; }</style></head><body><h1>Test</h1></body></html>")
                
                # Verify
                verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify Code')]")
                verify_button.click()
                time.sleep(1)
                
                # Navigate to next
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next Lesson')]"))
                    )
                    next_button.click()
                    time.sleep(1)
                except TimeoutException:
                    try:
                        skip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Skip')]")
                        skip_button.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        break
                        
            except (TimeoutException, NoSuchElementException) as e:
                pytest.fail(f"Error in CSS lesson {lesson_num + 1}: {str(e)}")
    
    def test_accessibility_module(self, driver, base_url):
        """Test Accessibility module (6 lessons)"""
        wait = self.start_lesson(driver, base_url)
        
        # Navigate to Accessibility section
        assert self.navigate_to_section(driver, wait, "Accessibility section"), "Could not navigate to Accessibility section"
        
        # Test lessons in Accessibility module
        for lesson_num in range(6):
            try:
                lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
                assert lesson_title.is_displayed(), f"Accessibility lesson {lesson_num + 1} title not displayed"
                
                # Test interactive elements
                tooltip_buttons = driver.find_elements(By.CSS_SELECTOR, ".tooltip-wrapper, button[role='button'][aria-describedby]")
                if tooltip_buttons:
                    tooltip_buttons[0].click()
                    time.sleep(0.3)
                
                try:
                    hint_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Show hint') or contains(text(), 'Hide hint')]")
                    hint_button.click()
                    time.sleep(0.3)
                except NoSuchElementException:
                    pass
                
                # Code editor - get existing code first
                code_editor = driver.find_element(By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']")
                existing_code = code_editor.get_attribute("value") or code_editor.text
                
                # Modify code based on lesson requirements
                if lesson_num == 0:  # Semantic HTML - replace div with main
                    code_editor.clear()
                    code_editor.send_keys("<html>\n<head>\n    <title>My Accessible Webpage</title>\n</head>\n<body>\n    <header>\n        <h1>Welcome</h1>\n    </header>\n    <main>\n        <p>This is my accessible webpage!</p>\n    </main>\n</body>\n</html>")
                elif lesson_num == 1:  # Alt text - add descriptive alt text
                    code_editor.clear()
                    code_editor.send_keys('<html>\n<head>\n    <title>My Accessible Webpage</title>\n</head>\n<body>\n    <header>\n        <h1>Welcome</h1>\n    </header>\n    <main>\n        <img src="https://via.placeholder.com/300" alt="A red sunset over the ocean with clouds">\n    </main>\n</body>\n</html>')
                elif lesson_num == 2:  # Heading hierarchy - add h2
                    code_editor.clear()
                    code_editor.send_keys("<html>\n<head>\n    <title>My Accessible Webpage</title>\n</head>\n<body>\n    <header>\n        <h1>Main Title</h1>\n    </header>\n    <main>\n        <h2>About</h2>\n        <p>Content here</p>\n    </main>\n</body>\n</html>")
                elif lesson_num == 3:  # Keyboard navigation - add focus styles
                    code_editor.clear()
                    code_editor.send_keys("<html>\n<head>\n    <title>My Accessible Webpage</title>\n    <style>\n        a:focus {\n            outline: 2px solid blue;\n            background-color: yellow;\n        }\n    </style>\n</head>\n<body>\n    <header>\n        <h1>Welcome</h1>\n        <nav>\n            <a href=\"#home\">Home</a>\n            <a href=\"#about\">About</a>\n        </nav>\n    </header>\n</body>\n</html>")
                elif lesson_num == 4:  # ARIA labels - add aria-label or role to div
                    code_editor.clear()
                    code_editor.send_keys('<html>\n<head>\n    <title>My Accessible Webpage</title>\n</head>\n<body>\n    <header>\n        <h1>Welcome</h1>\n        <nav role="navigation">\n            <button aria-label="Menu">☰</button>\n        </nav>\n    </header>\n    <main>\n        <div role="button" aria-label="Click to expand">Expand section</div>\n    </main>\n</body>\n</html>')
                else:  # Advanced accessibility - add label
                    code_editor.clear()
                    code_editor.send_keys('<html lang="en">\n<head>\n    <title>My Accessible Webpage</title>\n</head>\n<body>\n    <header>\n        <h1>Welcome</h1>\n    </header>\n    <main>\n        <form>\n            <label for="username">Username:</label>\n            <input type="text" id="username" name="username">\n        </form>\n        <p id="description">This is a description</p>\n        <div aria-describedby="description">Content here</div>\n    </main>\n</body>\n</html>')
                
                # Verify
                verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify Code')]")
                verify_button.click()
                time.sleep(1)
                
                # Navigate to next
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next Lesson')]"))
                    )
                    next_button.click()
                    time.sleep(1)
                except TimeoutException:
                    try:
                        skip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Skip')]")
                        skip_button.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        break
                        
            except (TimeoutException, NoSuchElementException) as e:
                pytest.fail(f"Error in Accessibility lesson {lesson_num + 1}: {str(e)}")
    
    def test_all_external_links(self, driver, base_url):
        """Test all external W3Schools links across all modules"""
        wait = self.start_lesson(driver, base_url)
        
        sections = ["HTML Fundamentals", "HTML section", "CSS section", "Accessibility section"]
        all_links_working = True
        
        for section in sections:
            if not self.navigate_to_section(driver, wait, section):
                continue
            
            # Find all external links
            external_links = driver.find_elements(
                By.XPATH,
                "//a[contains(@href, 'w3schools.com')]"
            )
            
            for link in external_links:
                try:
                    # Check link has proper attributes
                    href = link.get_attribute("href")
                    assert href and "w3schools.com" in href, f"Invalid link: {href}"
                    
                    # Check link text
                    link_text = link.text
                    assert link_text, "Link has no text"
                    
                except AssertionError as e:
                    all_links_working = False
                    print(f"Link issue in {section}: {str(e)}")
        
        assert all_links_working, "Some external links have issues"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=modules_report.html", "--self-contained-html"])

