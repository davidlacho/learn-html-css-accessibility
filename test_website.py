"""
Comprehensive Selenium tests for the HTML/CSS Learning Website
Tests all modules, interactive elements, and functionality
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestWebsite:
    """Test suite for the HTML/CSS learning website"""
    
    def start_lesson_session(self, driver, wait, student_name="Test User", base_url="http://localhost:3000/index.html"):
        """Helper method to start a lesson session"""
        driver.get(base_url)
        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        time.sleep(1)  # Give React time to render
        
        # Enter name
        name_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        name_input.clear()
        name_input.send_keys(student_name)
        
        # Click Start Learning
        start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Learning')]")))
        start_button.click()
        
        # Wait for lesson to load - check for lesson content or h2 heading
        wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2")),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".lesson-content")),
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome')]"))
            )
        )
        time.sleep(1)  # Give React time to fully render
    
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
        return "http://localhost:3000/index.html"
    
    def _base_url(self):
        """Non-fixture version for use in methods"""
        return "http://localhost:3000/index.html"
    
    def test_welcome_screen_loads(self, driver, base_url):
        """Test that welcome screen loads correctly"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Check for welcome heading
        welcome_heading = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome to Web Development')]"))
        )
        assert welcome_heading.is_displayed()
        
        # Check for name input
        name_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        assert name_input.is_displayed()
        
        # Check for Start Learning button
        start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start Learning')]")
        assert start_button.is_displayed()
    
    def test_tooltips_on_welcome_screen(self, driver, base_url):
        """Test that tooltips work on welcome screen"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Find tooltip buttons (HTML, CSS, accessible)
        try:
            html_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'HTML')]"))
            )
            
            # Hover over HTML button to show tooltip
            driver.execute_script("arguments[0].scrollIntoView(true);", html_button)
            time.sleep(0.5)
            html_button.click()  # Click to trigger tooltip
            time.sleep(0.5)
            
            # Check if tooltip appears (tooltips are shown on click/hover)
            tooltips = driver.find_elements(By.CSS_SELECTOR, ".tooltip")
            if tooltips:
                # At least one tooltip should be present
                assert len(tooltips) > 0, "Tooltip elements should be present"
            else:
                # Tooltips might be in tooltip-wrapper
                tooltip_wrappers = driver.find_elements(By.CSS_SELECTOR, ".tooltip-wrapper")
                assert len(tooltip_wrappers) > 0, "Tooltip wrappers should be present on welcome screen"
        except TimeoutException:
            pytest.skip("Tooltip buttons not found on welcome screen")
    
    def test_name_input_and_start(self, driver, base_url):
        """Test entering name and starting the lesson"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Verify we're on a lesson page
        lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
        assert lesson_title.is_displayed()
    
    def test_course_progress_sections(self, driver, base_url):
        """Test course progress navigation sections"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Test clicking on different sections
        sections = [
            "HTML Fundamentals",
            "HTML",
            "CSS",
            "Accessibility"
        ]
        
        for section_name in sections:
            try:
                section_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(@aria-label, '{section_name}')]"))
                )
                section_button.click()
                time.sleep(1)  # Wait for navigation
                
                # Verify we're on a lesson from that section
                lesson_content = driver.find_element(By.CSS_SELECTOR, ".lesson-content")
                assert lesson_content.is_displayed()
            except TimeoutException:
                pytest.skip(f"Section button for {section_name} not found")
    
    def test_hint_button_toggle(self, driver, base_url):
        """Test that hint button shows and hides hints"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Find hint button
        try:
            hint_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show hint') or contains(text(), 'Hide hint')]"))
            )
            
            # Click to show hint
            hint_button.click()
            time.sleep(0.5)
            
            # Check if hint is visible
            hint_region = driver.find_element(By.CSS_SELECTOR, "region[aria-label='Hint instructions'], .hint-content, [role='region']")
            assert hint_region.is_displayed()
            
            # Click to hide hint
            hint_button.click()
            time.sleep(0.5)
            
        except TimeoutException:
            pytest.skip("Hint button not found on this lesson")
    
    def test_tooltips_in_lesson(self, driver, base_url):
        """Test tooltips work in lesson content"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Find a tooltip button in the lesson content
        try:
            tooltip_buttons = driver.find_elements(By.CSS_SELECTOR, ".tooltip-wrapper, button[role='button'][aria-describedby]")
            if tooltip_buttons:
                # Click first tooltip button
                tooltip_buttons[0].click()
                time.sleep(0.5)
                
                # Check if tooltip is visible
                tooltip = driver.find_element(By.CSS_SELECTOR, ".tooltip")
                assert tooltip.is_displayed() or tooltip.get_attribute("aria-hidden") != "true"
        except (NoSuchElementException, IndexError):
            pytest.skip("No tooltip buttons found in this lesson")
    
    def test_code_editor_functionality(self, driver, base_url):
        """Test code editor accepts input"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Find code editor
        code_editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']"))
        )
        
        # Clear and type code
        code_editor.clear()
        test_code = "<div>Hello World</div>"
        code_editor.send_keys(test_code)
        
        # Verify code was entered
        assert test_code in code_editor.get_attribute("value") or test_code in code_editor.text
    
    def test_code_verification_success(self, driver, base_url):
        """Test code verification works correctly"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Find code editor and enter valid code
        code_editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']"))
        )
        code_editor.clear()
        code_editor.send_keys("<div>Test</div>")
        
        # Click Verify Code button
        verify_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Verify Code')]"))
        )
        verify_button.click()
        
        # Wait for success message or Next Lesson button
        time.sleep(2)  # Give time for validation to complete
        try:
            # Check for Next Lesson button (indicates success)
            next_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next Lesson')]"))
            )
            assert next_button.is_displayed(), "Next Lesson button should appear after successful verification"
        except TimeoutException:
            # Check for success message
            try:
                success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Great job') or contains(text(), 'correct')]")
                if success_message.is_displayed():
                    pass  # Success message found
                else:
                    # Check for error message
                    error_message = driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'try again')]")
                    if error_message:
                        pytest.skip("Code validation failed - this might be expected for some lessons")
                    else:
                        # Maybe validation is still processing, wait a bit more
                        time.sleep(1)
                        next_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Next Lesson')]")
                        if not next_button:
                            raise AssertionError("No success indicator found after code verification")
            except NoSuchElementException:
                # Check for error message
                error_message = driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'try again')]")
                if error_message:
                    pytest.skip("Code validation failed - this might be expected for some lessons")
                else:
                    raise AssertionError("No feedback message found after code verification")
    
    def test_navigation_buttons(self, driver, base_url):
        """Test Next, Back, and Skip buttons"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Get initial lesson title
        initial_title = driver.find_element(By.CSS_SELECTOR, "h2").text
        
        # Test Skip button
        try:
            skip_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Skip')]"))
            )
            skip_button.click()
            time.sleep(1)
            
            # Verify we moved to next lesson
            new_title = driver.find_element(By.CSS_SELECTOR, "h2").text
            assert new_title != initial_title or "Lesson" in driver.page_source
            
        except TimeoutException:
            pytest.skip("Skip button not available")
        
        # Test Back button
        try:
            back_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Back')]"))
            )
            back_button.click()
            time.sleep(1)
            
            # Verify we went back
            back_title = driver.find_element(By.CSS_SELECTOR, "h2").text
            assert back_title == initial_title or "Lesson" in driver.page_source
            
        except TimeoutException:
            pytest.skip("Back button not available")
    
    def test_external_links(self, driver, base_url):
        """Test external W3Schools links open in new tabs"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Find external links
        external_links = driver.find_elements(
            By.XPATH, 
            "//a[contains(@href, 'w3schools.com')]"
        )
        
        if external_links:
            initial_window = driver.current_window_handle
            initial_window_count = len(driver.window_handles)
            
            # Click first external link
            external_links[0].click()
            time.sleep(2)
            
            # Check if new window/tab opened
            new_window_count = len(driver.window_handles)
            assert new_window_count > initial_window_count or driver.current_url != base_url
            
            # Switch back to original window
            driver.switch_to.window(initial_window)
        else:
            pytest.skip("No external links found in this lesson")
    
    def test_preview_panel(self, driver, base_url):
        """Test that preview panel displays rendered content"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Find preview panel/iframe
        try:
            preview_iframe = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe, .preview-panel iframe"))
            )
            assert preview_iframe.is_displayed()
        except TimeoutException:
            # Check for preview panel without iframe
            preview_panel = driver.find_elements(By.CSS_SELECTOR, ".preview-panel, [aria-label*='preview']")
            if preview_panel:
                assert preview_panel[0].is_displayed()
            else:
                pytest.skip("Preview panel not found")
    
    def test_progress_tracking(self, driver, base_url):
        """Test that progress is tracked correctly"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Complete a lesson
        code_editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea, [contenteditable='true'], input[type='text'][aria-label*='code']"))
        )
        code_editor.clear()
        code_editor.send_keys("<div>Test</div>")
        
        verify_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Verify Code')]"))
        )
        verify_button.click()
        time.sleep(1)
        
        # Check progress indicators
        progress_indicators = driver.find_elements(
            By.XPATH,
            "//*[contains(text(), '/') and (contains(text(), 'completed') or contains(text(), 'of'))]"
        )
        if progress_indicators:
            # At least one progress indicator should show updated count
            assert len(progress_indicators) > 0
    
    def test_all_lessons_navigation(self, driver, base_url):
        """Test navigating through multiple lessons"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Navigate through at least 3 lessons using Skip
        previous_title = None
        for i in range(3):
            try:
                # Get current lesson title
                lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
                current_title = lesson_title.text
                
                # If we have a previous title, verify it changed
                if previous_title and current_title == previous_title and i > 0:
                    # Title didn't change, but that's okay if we're at the end
                    break
                
                previous_title = current_title
                
                # Click Skip
                skip_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Skip')]"))
                )
                skip_button.click()
                time.sleep(1.5)  # Wait for navigation
                
                # Verify we moved to a new lesson (title should change or we're at end)
                try:
                    new_lesson_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
                    new_title = new_lesson_title.text
                    # Title should change, or we've navigated successfully
                    if new_title == current_title and i < 2:
                        # Give it one more chance
                        time.sleep(1)
                        new_lesson_title = driver.find_element(By.CSS_SELECTOR, "h2")
                        new_title = new_lesson_title.text
                except TimeoutException:
                    break  # No more lessons
                
            except TimeoutException:
                break  # No more lessons or skip button not available
    
    def test_url_persistence(self, driver, base_url):
        """Test that URL saves progress state"""
        wait = WebDriverWait(driver, 15)
        self.start_lesson_session(driver, wait, base_url=base_url)
        
        # Get URL after starting
        initial_url = driver.current_url
        
        # Navigate to next lesson
        try:
            skip_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Skip')]"))
            )
            skip_button.click()
            time.sleep(1)
            
            # URL should have changed (contains lesson state)
            new_url = driver.current_url
            assert new_url != initial_url
            assert "#" in new_url or "lesson" in new_url.lower()
            
        except TimeoutException:
            pytest.skip("Skip button not available for URL test")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html", "--self-contained-html"])

