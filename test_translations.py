"""
Tests for translation functionality
Tests language switching, translation loading, and translated content
"""

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestTranslations:
    """Test translation functionality"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome driver"""
        import os
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = None
        try:
            driver_path = ChromeDriverManager().install()
            if os.path.isdir(driver_path):
                for root, dirs, files in os.walk(driver_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if 'chromedriver' in file.lower() and os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                            if not file.endswith(('.txt', '.md', '.pdf')):
                                driver_path = full_path
                                break
            if os.path.isfile(driver_path) and os.access(driver_path, os.X_OK):
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            # Fallback to system chromedriver
            driver = webdriver.Chrome(options=chrome_options)
        
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="class")
    def base_url(self):
        """Base URL for the website"""
        return "http://localhost:8000/index.html"
    
    def test_translations_file_exists(self):
        """Test that translations.json file exists and is valid JSON"""
        import os
        translations_path = os.path.join(os.path.dirname(__file__), 'translations.json')
        assert os.path.exists(translations_path), "translations.json file should exist"
        
        with open(translations_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        
        assert 'en' in translations, "English translations should exist"
        assert 'fr' in translations, "French translations should exist"
        assert 'ui' in translations['en'], "English UI translations should exist"
        assert 'ui' in translations['fr'], "French UI translations should exist"
        assert 'categories' in translations['en'], "English category translations should exist"
        assert 'categories' in translations['fr'], "French category translations should exist"
        assert 'lessons' in translations['en'], "English lesson translations should exist"
        assert 'lessons' in translations['fr'], "French lesson translations should exist"
    
    def test_language_dropdown_exists(self, driver, base_url):
        """Test that language dropdown is present on the page"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Wait for page to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#language-select, select#language-select-main")))
        time.sleep(1)
        
        # Find language selector (could be either ID)
        try:
            lang_select = driver.find_element(By.ID, "language-select")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select-main")
        
        assert lang_select.is_displayed(), "Language selector should be visible"
        
        # Check that both English and French options exist
        select = Select(lang_select)
        options = [opt.text for opt in select.options]
        assert "English" in options, "English option should be available"
        assert "Français" in options, "French option should be available"
    
    def test_default_language_is_english(self, driver, base_url):
        """Test that default language is English"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#language-select, select#language-select-main")))
        time.sleep(1)
        
        try:
            lang_select = driver.find_element(By.ID, "language-select")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select-main")
        
        select = Select(lang_select)
        assert select.first_selected_option.get_attribute("value") == "en", "Default language should be English"
        
        # Check HTML lang attribute
        html_lang = driver.execute_script("return document.documentElement.lang")
        assert html_lang == "en", f"HTML lang attribute should be 'en', got '{html_lang}'"
    
    def test_switch_to_french(self, driver, base_url):
        """Test switching language to French"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#language-select, select#language-select-main")))
        time.sleep(1)
        
        try:
            lang_select = driver.find_element(By.ID, "language-select")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select-main")
        
        select = Select(lang_select)
        select.select_by_value("fr")
        time.sleep(1)  # Wait for translation to apply
        
        # Check HTML lang attribute updated
        html_lang = driver.execute_script("return document.documentElement.lang")
        assert html_lang == "fr", f"HTML lang attribute should be 'fr' after switching, got '{html_lang}'"
        
        # Check that French text appears
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Bienvenue" in page_text or "Apprendre" in page_text, "French text should appear on page"
    
    def test_welcome_screen_translations(self, driver, base_url):
        """Test that welcome screen text is translated"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#language-select, select#language-select-main")))
        time.sleep(1)
        
        try:
            lang_select = driver.find_element(By.ID, "language-select")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select-main")
        
        select = Select(lang_select)
        
        # Test English
        select.select_by_value("en")
        time.sleep(1)
        welcome_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Welcome to Web Development!" in welcome_text or "Welcome" in welcome_text, "English welcome text should appear"
        assert "Start Learning" in welcome_text, "English 'Start Learning' button should appear"
        
        # Test French
        select.select_by_value("fr")
        time.sleep(1)
        welcome_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Bienvenue" in welcome_text, "French welcome text should appear"
        assert "Commencer l'Apprentissage" in welcome_text, "French 'Start Learning' button should appear"
    
    def test_lesson_content_translations(self, driver, base_url):
        """Test that lesson content is translated when language is switched"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Start a lesson session
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        time.sleep(1)
        
        name_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        name_input.clear()
        name_input.send_keys("Test User")
        
        start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Learning') or contains(text(), 'Commencer')]")))
        start_button.click()
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2, .lesson-content")))
        time.sleep(1)
        
        # Find language selector
        try:
            lang_select = driver.find_element(By.ID, "language-select-main")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select")
        
        select = Select(lang_select)
        
        # Test English lesson content
        select.select_by_value("en")
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Understanding HTML Tags" in page_text or "HTML Tags" in page_text, "English lesson title should appear"
        assert "Verify Code" in page_text, "English 'Verify Code' button should appear"
        
        # Test French lesson content
        select.select_by_value("fr")
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Comprendre les Balises HTML" in page_text or "Balises HTML" in page_text, "French lesson title should appear"
        assert "Vérifier le Code" in page_text, "French 'Verify Code' button should appear"
    
    def test_category_names_translated(self, driver, base_url):
        """Test that category names are translated"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Start a lesson session
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        time.sleep(1)
        
        name_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        name_input.clear()
        name_input.send_keys("Test User")
        
        start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Learning') or contains(text(), 'Commencer')]")))
        start_button.click()
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".progress-label")))
        time.sleep(1)
        
        # Find language selector
        try:
            lang_select = driver.find_element(By.ID, "language-select-main")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select")
        
        select = Select(lang_select)
        
        # Test English categories
        select.select_by_value("en")
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "HTML Fundamentals" in page_text, "English 'HTML Fundamentals' should appear"
        assert "Accessibility" in page_text, "English 'Accessibility' should appear"
        
        # Test French categories
        select.select_by_value("fr")
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Fondamentaux HTML" in page_text, "French 'Fondamentaux HTML' should appear"
        assert "Accessibilité" in page_text, "French 'Accessibilité' should appear"
    
    def test_ui_elements_translated(self, driver, base_url):
        """Test that UI elements (buttons, labels) are translated"""
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Start a lesson session
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
        time.sleep(1)
        
        name_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        name_input.clear()
        name_input.send_keys("Test User")
        
        start_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Learning') or contains(text(), 'Commencer')]")))
        start_button.click()
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button")))
        time.sleep(1)
        
        # Find language selector
        try:
            lang_select = driver.find_element(By.ID, "language-select-main")
        except NoSuchElementException:
            lang_select = driver.find_element(By.ID, "language-select")
        
        select = Select(lang_select)
        
        # Test English UI elements
        select.select_by_value("en")
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Verify Code" in page_text, "English 'Verify Code' button should appear"
        assert "Skip" in page_text, "English 'Skip' button should appear"
        
        # Navigate to second lesson to test Back button
        skip_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Skip')]")))
        skip_button.click()
        time.sleep(1)
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Back" in page_text or "← Back" in page_text, "English 'Back' button should appear on second lesson"
        
        # Test French UI elements
        select.select_by_value("fr")
        time.sleep(1)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Vérifier le Code" in page_text, "French 'Vérifier le Code' button should appear"
        assert "Passer" in page_text, "French 'Passer' button should appear"
        assert "Retour" in page_text or "← Retour" in page_text, "French 'Retour' button should appear on second lesson"

