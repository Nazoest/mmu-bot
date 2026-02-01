"""
MMU Student Portal Login Bot
This script automates logging into the MMU Student Portal using Selenium WebDriver.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Read from environment variables for security
LOGIN_URL = "https://studentportal.mmu.ac.ke/Student%20Login.aspx"
REGISTRATION_NUMBER = os.getenv("MMU_REG_NUMBER")
PASSWORD = os.getenv("MMU_PASSWORD")

# Validate that credentials are set
if not REGISTRATION_NUMBER or not PASSWORD:
    print("=" * 80)
    print("ERROR: Credentials not found!")
    print("=" * 80)
    print("\nPlease set your credentials as environment variables:")
    print("\nOption 1: Set temporarily (current session only):")
    print("  set MMU_REG_NUMBER=your-registration-number")
    print("  set MMU_PASSWORD=your-password")
    print("\nOption 2: Create a .env file (recommended):")
    print("  1. Copy .env.example to .env")
    print("  2. Edit .env and add your credentials")
    print("\n" + "=" * 80)
    exit(1)

def setup_driver():
    """Initialize and configure the Chrome WebDriver."""
    chrome_options = Options()
    # Uncomment the next line to run in headless mode (no browser window)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    return driver

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
                    print(f"[SUCCESS] Found balance by ID '{element_id}': {balance_text}")
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
                        print(f"[SUCCESS] Found balance by class '{class_name}': {balance_text}")
                        return balance_text
            except NoSuchElementException:
                continue
        
        # Strategy 3: Search for text containing common balance indicators
        balance_keywords = ["Balance:", "Fee Balance:", "Account Balance:", "Ksh", "KES", "Amount:"]
        
        for keyword in balance_keywords:
            try:
                # Use XPath to find elements containing the keyword
                xpath = f"//*[contains(text(), '{keyword}')]"
                elements = driver.find_elements(By.XPATH, xpath)
                
                for element in elements:
                    text = element.text.strip()
                    # Look for the balance in the same element or nearby
                    if text and any(char.isdigit() for char in text):
                        print(f"[SUCCESS] Found balance by keyword '{keyword}': {text}")
                        return text
                    
                    # Also check the next sibling or parent element
                    try:
                        parent = element.find_element(By.XPATH, "..")
                        parent_text = parent.text.strip()
                        if parent_text and any(char.isdigit() for char in parent_text):
                            print(f"[SUCCESS] Found balance in parent element: {parent_text}")
                            return parent_text
                    except:
                        pass
                        
            except NoSuchElementException:
                continue
        
        # Strategy 4: Look for any element with currency symbols or large numbers
        try:
            # Find all span, div, label, and td elements
            all_elements = driver.find_elements(By.CSS_SELECTOR, "span, div, label, td, strong, b")
            
            for element in all_elements:
                text = element.text.strip()
                # Check if text contains currency patterns (e.g., "Ksh 5,000", "5000.00", etc.)
                if text and (
                    ('ksh' in text.lower() or 'kes' in text.lower()) or
                    (any(char.isdigit() for char in text) and (',' in text or '.' in text))
                ):
                    # Filter out non-balance items (like dates)
                    if len(text) < 50 and any(char.isdigit() for char in text):
                        print(f"[SUCCESS] Found potential balance by pattern matching: {text}")
                        return text
        except:
            pass
        
        # Strategy 5: Debug - print page source snippet for manual inspection
        print("[WARNING] Could not find balance using any strategy")
        print("[DEBUG] Saving page source to 'dashboard_source.html' for inspection...")
        
        try:
            with open("dashboard_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("[INFO] Page source saved. Please inspect this file to find balance element.")
        except Exception as e:
            print(f"[WARNING] Could not save page source: {e}")
        
        return "Balance not found"
        
    except Exception as e:
        print(f"[ERROR] Error while checking balance: {e}")
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
        print(f"[INFO] Navigating to: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Click the "Student Login" button on the landing page
        print("[INFO] Looking for 'Student Login' button...")
        student_login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnStudentLogin"))
        )
        print("[INFO] Clicking 'Student Login' button...")
        student_login_button.click()
        
        # Wait a moment for the page to navigate
        time.sleep(2)
        
        # Step 2: Wait for the actual login form to appear
        print("[INFO] Waiting for login form to load...")
        
        # Try to find common input field identifiers
        # We'll need to find the registration number and password fields
        # Common IDs might be: txtUsername, txtRegNo, txtPassword, etc.
        
        # Let's try multiple possible field identifiers
        registration_field = None
        password_field = None
        submit_button = None
        
        # Try to find registration number field (various possible IDs)
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
                print(f"[SUCCESS] Found registration field with ID: {field_id}")
                break
            except NoSuchElementException:
                continue
        
        # If we couldn't find by ID, try by name attribute
        if not registration_field:
            try:
                registration_field = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtRegNo")
                print("[SUCCESS] Found registration field by name attribute")
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
                print(f"[SUCCESS] Found password field with ID: {field_id}")
                break
            except NoSuchElementException:
                continue
        
        # If we couldn't find by ID, try by name attribute
        if not password_field:
            try:
                password_field = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txtPassword")
                print("[SUCCESS] Found password field by name attribute")
            except NoSuchElementException:
                pass
        
        # If we still haven't found the fields, try finding all input elements
        if not registration_field or not password_field:
            print("[INFO] Attempting to find fields by type...")
            input_fields = driver.find_elements(By.TAG_NAME, "input")
            text_inputs = [inp for inp in input_fields if inp.get_attribute("type") in ["text", "password"]]
            
            if len(text_inputs) >= 2:
                if not registration_field:
                    registration_field = text_inputs[0]
                    print("[SUCCESS] Using first text input as registration field")
                if not password_field:
                    password_field = [inp for inp in text_inputs if inp.get_attribute("type") == "password"][0]
                    print("[SUCCESS] Found password field by type")
        
        # Check if we found both fields
        if not registration_field or not password_field:
            print("[ERROR] Could not locate login form fields!")
            print("[INFO] Current page source (first 500 chars):")
            print(driver.page_source[:500])
            return False, "Login failed"
        
        # Step 3: Enter credentials
        print(f"[INFO] Entering registration number: {REGISTRATION_NUMBER}")
        registration_field.clear()
        registration_field.send_keys(REGISTRATION_NUMBER)
        
        print("[INFO] Entering password...")
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        time.sleep(1)  # Small delay before clicking submit
        
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
                print(f"[SUCCESS] Found submit button with ID: {button_id}")
                break
            except NoSuchElementException:
                continue
        
        # Try finding submit button by type
        if not submit_button:
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            if submit_buttons:
                submit_button = submit_buttons[0]
                print("[SUCCESS] Found submit button by type")
        
        if not submit_button:
            print("[ERROR] Could not find submit button!")
            return False, "Login failed"
        
        print("[INFO] Clicking login button...")
        submit_button.click()
        
        # Wait for redirect/login to complete
        time.sleep(3)
        
        # Check if login was successful
        current_url = driver.current_url
        print(f"[INFO] Current URL after login attempt: {current_url}")
        
        # Check for error messages
        try:
            error_element = driver.find_element(By.ID, "ContentPlaceHolder1_lblError")
            error_text = error_element.text
            if error_text:
                print(f"[ERROR] Login error message: {error_text}")
                return False, "Login failed"
        except NoSuchElementException:
            pass
        
        # If URL changed or we're not on login page anymore, likely successful
        if "Login" not in current_url:
            print("[SUCCESS] Login appears successful! You are now logged in.")
            print(f"[INFO] You've been redirected to: {current_url}")
            
            # Check balance after successful login
            print("\n[INFO] Checking account balance...")
            balance = check_balance(driver)
            
            return True, balance
        else:
            print("[WARNING] Still on login page. Please check credentials or website status.")
            return False, "Login failed"
            
    except TimeoutException as e:
        print(f"[ERROR] Timeout waiting for page elements: {e}")
        return False, "Login failed"
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False, "Login failed"

def main():
    """Main execution function."""
    driver = None
    
    try:
        print("=" * 60)
        print("MMU Student Portal Login Bot")
        print("=" * 60)
        
        driver = setup_driver()
        success, balance = login_to_portal(driver)
        
        if success:
            print("\n" + "=" * 60)
            print("Login completed successfully!")
            print(f"💰 Account Balance: {balance}")
            print("The browser will remain open for 30 seconds...")
            print("=" * 60)
            time.sleep(30)
        else:
            print("\n" + "=" * 60)
            print("Login failed. Please check the output above for details.")
            print("The browser will remain open for 10 seconds...")
            print("=" * 60)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user.")
    finally:
        if driver:
            print("[INFO] Closing browser...")
            driver.quit()
            print("[INFO] Done!")

if __name__ == "__main__":
    main()
