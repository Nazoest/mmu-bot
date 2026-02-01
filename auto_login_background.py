"""
MMU Student Portal Auto-Login Bot (Background Mode)
This script automatically logs into the MMU Student Portal every 45 minutes
in headless mode (no visible browser window).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import logging
from datetime import datetime
import sys
import os

# Configuration - Read from environment variables for security
LOGIN_URL = "https://studentportal.mmu.ac.ke/Student%20Login.aspx"
REGISTRATION_NUMBER = os.getenv("MMU_REG_NUMBER")
PASSWORD = os.getenv("MMU_PASSWORD")
LOGIN_INTERVAL_MINUTES = int(os.getenv("MMU_LOGIN_INTERVAL", "45"))  # Default to 45 minutes

# Validate that credentials are set
if not REGISTRATION_NUMBER or not PASSWORD:
    print("=" * 80)
    print("ERROR: Credentials not found!")
    print("=" * 80)
    print("\nPlease set your credentials as environment variables:")
    print("\nOption 1: Set temporarily (current session only):")
    print("  set MMU_REG_NUMBER=your-registration-number")
    print("  set MMU_PASSWORD=your-password")
    print("  set MMU_LOGIN_INTERVAL=45  (optional, defaults to 45)")
    print("\nOption 2: Create a .env file (recommended):")
    print("  1. Copy .env.example to .env")
    print("  2. Edit .env and add your credentials")
    print("\n" + "=" * 80)
    sys.exit(1)

# Setup logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mmu_login_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_driver():
    """Initialize and configure the Chrome WebDriver in headless mode."""
    chrome_options = Options()
    
    # Run in headless mode (no visible browser window)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Additional stealth options
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Suppress unnecessary logs
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        return None

def check_balance(driver):
    """
    Extract account balance from the dashboard.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        str: Balance amount or "Balance not found"
    """
    try:
        # Give page time to fully load
        time.sleep(2)
        
        # Strategy 1: Try common balance element IDs
        possible_balance_ids = [
            "ContentPlaceHolder1_lblBalance",
            "lblBalance",
            "ContentPlaceHolder1_lblFeeBalance", 
            "lblFeeBalance",
            "ContentPlaceHolder1_lblAccountBalance",
            "lblAccountBalance",
            "balance",
            "fee_balance",
            "account_balance"
        ]
        
        for element_id in possible_balance_ids:
            try:
                balance_element = driver.find_element(By.ID, element_id)
                balance_text = balance_element.text.strip()
                if balance_text:
                    logger.info(f"Found balance by ID '{element_id}': {balance_text}")
                    return balance_text
            except NoSuchElementException:
                continue
        
        # Strategy 2: Try common class names
        possible_balance_classes = [
            "balance",
            "fee-balance",
            "account-balance",
            "student-balance",
            "lblBalance"
        ]
        
        for class_name in possible_balance_classes:
            try:
                balance_elements = driver.find_elements(By.CLASS_NAME, class_name)
                for element in balance_elements:
                    balance_text = element.text.strip()
                    if balance_text and any(char.isdigit() for char in balance_text):
                        logger.info(f"Found balance by class '{class_name}': {balance_text}")
                        return balance_text
            except NoSuchElementException:
                continue
        
        # Strategy 3: Search for text containing common balance indicators
        balance_keywords = ["Balance:", "Fee Balance:", "Account Balance:", "Ksh", "KES", "Amount:"]
        
        for keyword in balance_keywords:
            try:
                xpath = f"//*[contains(text(), '{keyword}')]"
                elements = driver.find_elements(By.XPATH, xpath)
                
                for element in elements:
                    text = element.text.strip()
                    if text and any(char.isdigit() for char in text):
                        logger.info(f"Found balance by keyword '{keyword}': {text}")
                        return text
                    
                    try:
                        parent = element.find_element(By.XPATH, "..")
                        parent_text = parent.text.strip()
                        if parent_text and any(char.isdigit() for char in parent_text):
                            logger.info(f"Found balance in parent element: {parent_text}")
                            return parent_text
                    except:
                        pass
                        
            except NoSuchElementException:
                continue
        
        # Strategy 4: Look for currency patterns
        try:
            all_elements = driver.find_elements(By.CSS_SELECTOR, "span, div, label, td, strong, b")
            
            for element in all_elements:
                text = element.text.strip()
                if text and (
                    ('ksh' in text.lower() or 'kes' in text.lower()) or
                    (any(char.isdigit() for char in text) and (',' in text or '.' in text))
                ):
                    if len(text) < 50 and any(char.isdigit() for char in text):
                        logger.info(f"Found potential balance by pattern matching: {text}")
                        return text
        except:
            pass
        
        logger.warning("Could not find balance using any strategy")
        return "Balance not found"
        
    except Exception as e:
        logger.error(f"Error while checking balance: {e}")
        return "Balance not found"


def login_to_portal(driver):
    """
    Main login function that handles the complete login process.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        tuple: (success: bool, balance: str)
    """
    try:
        logger.info(f"Navigating to: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 15)
        
        # Step 1: Click the "Student Login" button on the landing page
        logger.info("Looking for 'Student Login' button...")
        student_login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnStudentLogin"))
        )
        logger.info("Clicking 'Student Login' button...")
        student_login_button.click()
        
        # Wait a moment for the page to navigate
        time.sleep(2)
        
        # Step 2: Wait for the actual login form to appear
        logger.info("Waiting for login form to load...")
        
        registration_field = None
        password_field = None
        submit_button = None
        
        # Try to find registration number field
        possible_reg_ids = [
            "ContentPlaceHolder1_txtRegNo",
            "txtRegNo",
            "ContentPlaceHolder1_txtUsername",
            "txtUsername",
            "ContentPlaceHolder1_txtStudentID",
            "txtStudentID"
        ]
        
        for field_id in possible_reg_ids:
            try:
                registration_field = driver.find_element(By.ID, field_id)
                logger.info(f"Found registration field with ID: {field_id}")
                break
            except NoSuchElementException:
                continue
        
        if not registration_field:
            try:
                registration_field = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtRegNo")
                logger.info("Found registration field by name attribute")
            except NoSuchElementException:
                pass
        
        # Try to find password field
        possible_pwd_ids = [
            "ContentPlaceHolder1_txtPassword",
            "txtPassword",
            "ContentPlaceHolder1_txtPass",
            "txtPass"
        ]
        
        for field_id in possible_pwd_ids:
            try:
                password_field = driver.find_element(By.ID, field_id)
                logger.info(f"Found password field with ID: {field_id}")
                break
            except NoSuchElementException:
                continue
        
        if not password_field:
            try:
                password_field = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtPassword")
                logger.info("Found password field by name attribute")
            except NoSuchElementException:
                pass
        
        # Fallback: try finding all input elements
        if not registration_field or not password_field:
            logger.info("Attempting to find fields by type...")
            input_fields = driver.find_elements(By.TAG_NAME, "input")
            text_inputs = [inp for inp in input_fields if inp.get_attribute("type") in ["text", "password"]]
            
            if len(text_inputs) >= 2:
                if not registration_field:
                    registration_field = text_inputs[0]
                    logger.info("Using first text input as registration field")
                if not password_field:
                    password_field = [inp for inp in text_inputs if inp.get_attribute("type") == "password"][0]
                    logger.info("Found password field by type")
        
        # Check if we found both fields
        if not registration_field or not password_field:
            logger.error("Could not locate login form fields!")
            return False, "Login failed"
        
        # Step 3: Enter credentials
        logger.info(f"Entering registration number: {REGISTRATION_NUMBER}")
        registration_field.clear()
        registration_field.send_keys(REGISTRATION_NUMBER)
        
        logger.info("Entering password...")
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        time.sleep(1)
        
        # Step 4: Find and click the submit/login button
        possible_submit_ids = [
            "ContentPlaceHolder1_btnLogin",
            "btnLogin",
            "ContentPlaceHolder1_btnSubmit",
            "btnSubmit"
        ]
        
        for button_id in possible_submit_ids:
            try:
                submit_button = driver.find_element(By.ID, button_id)
                logger.info(f"Found submit button with ID: {button_id}")
                break
            except NoSuchElementException:
                continue
        
        if not submit_button:
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            if submit_buttons:
                submit_button = submit_buttons[0]
                logger.info("Found submit button by type")
        
        if not submit_button:
            logger.error("Could not find submit button!")
            return False, "Login failed"
        
        logger.info("Clicking login button...")
        submit_button.click()
        
        # Wait for redirect/login to complete
        time.sleep(3)
        
        # Check if login was successful
        current_url = driver.current_url
        logger.info(f"Current URL after login attempt: {current_url}")
        
        # Check for error messages
        try:
            error_element = driver.find_element(By.ID, "ContentPlaceHolder1_lblError")
            error_text = error_element.text
            if error_text:
                logger.error(f"Login error message: {error_text}")
                return False, "Login failed"
        except NoSuchElementException:
            pass
        
        # If URL changed or we're not on login page anymore, likely successful
        if "Login" not in current_url:
            logger.info(f"✅ Login successful! Redirected to: {current_url}")
            
            # Check balance after successful login
            logger.info("Checking account balance...")
            balance = check_balance(driver)
            
            return True, balance
        else:
            logger.warning("Still on login page. Login may have failed.")
            return False, "Login failed"
            
    except TimeoutException as e:
        logger.error(f"Timeout waiting for page elements: {e}")
        return False, "Login failed"
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
        return False, "Login failed"
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return False, "Login failed"

def run_login_cycle():
    """Run a single login cycle."""
    driver = None
    try:
        logger.info("=" * 60)
        logger.info("Starting login cycle...")
        logger.info("=" * 60)
        
        driver = setup_driver()
        if not driver:
            logger.error("Failed to setup driver. Skipping this cycle.")
            return False
        
        success, balance = login_to_portal(driver)
        
        if success:
            logger.info(f"✅ Login cycle completed successfully! Balance: {balance}")
        else:
            logger.error("❌ Login cycle failed!")
        
        return success
        
    except Exception as e:
        logger.error(f"Error in login cycle: {e}")
        return False
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("Browser closed.")
            except:
                pass

def main():
    """Main execution function with automatic scheduling."""
    logger.info("=" * 60)
    logger.info("MMU Student Portal Auto-Login Bot (Background Mode)")
    logger.info(f"Login interval: Every {LOGIN_INTERVAL_MINUTES} minutes")
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("Press Ctrl+C to stop the bot")
    logger.info("=" * 60)
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            logger.info(f"\n📍 Cycle #{cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Run login
            run_login_cycle()
            
            # Calculate next run time
            next_run = datetime.now().timestamp() + (LOGIN_INTERVAL_MINUTES * 60)
            next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"⏰ Next login scheduled at: {next_run_time}")
            logger.info(f"💤 Sleeping for {LOGIN_INTERVAL_MINUTES} minutes...")
            logger.info("-" * 60)
            
            # Sleep until next cycle
            time.sleep(LOGIN_INTERVAL_MINUTES * 60)
            
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot stopped by user (Ctrl+C)")
        logger.info(f"Total cycles completed: {cycle_count}")
    except Exception as e:
        logger.error(f"Critical error in main loop: {e}")
        logger.info(f"Total cycles completed before error: {cycle_count}")

if __name__ == "__main__":
    main()
