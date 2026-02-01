"""
MMU Student Portal - Unit Registration Script
This script logs into the MMU Student Portal, navigates to the Unit Registration page,
extracts available units, and displays them in the terminal.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Read from environment variables for security
LOGIN_URL = "https://studentportal.mmu.ac.ke/Student%20Login.aspx"
UNIT_REGISTRATION_URL = "https://studentportal.mmu.ac.ke/UnitRegistration.aspx"
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
    
    # Detect if running in GitHub Actions or CI environment
    is_ci = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"
    
    if is_ci:
        # Headless mode with CI-compatible flags
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        print("[INFO] Running in CI/GitHub Actions mode (headless)")
    else:
        # Local mode with visible browser
        chrome_options.add_argument("--start-maximized")
        print("[INFO] Running in local mode (with browser UI)")
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_portal(driver):
    """
    Log into the MMU Student Portal.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        bool: True if login successful, False otherwise
    """
    try:
        print(f"[INFO] Navigating to: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        
        wait = WebDriverWait(driver, 10)
        
        # Click "Student Login" button
        print("[INFO] Looking for 'Student Login' button...")
        student_login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnStudentLogin"))
        )
        print("[INFO] Clicking 'Student Login' button...")
        student_login_button.click()
        
        time.sleep(2)
        
        # Find and fill login fields
        print("[INFO] Waiting for login form...")
        
        # Find registration field
        registration_field = None
        possible_reg_ids = [
            "ContentPlaceHolder1_txtRegNo",
            "txtRegNo",
            "ContentPlaceHolder1_txtUsername",
            "txtUsername"
        ]
        
        for field_id in possible_reg_ids:
            try:
                registration_field = driver.find_element(By.ID, field_id)
                print(f"[SUCCESS] Found registration field: {field_id}")
                break
            except NoSuchElementException:
                continue
        
        if not registration_field:
            input_fields = driver.find_elements(By.TAG_NAME, "input")
            text_inputs = [inp for inp in input_fields if inp.get_attribute("type") in ["text", "password"]]
            if text_inputs:
                registration_field = text_inputs[0]
                print("[SUCCESS] Using first text input as registration field")
        
        # Find password field
        password_field = None
        possible_pwd_ids = ["ContentPlaceHolder1_txtPassword", "txtPassword"]
        
        for field_id in possible_pwd_ids:
            try:
                password_field = driver.find_element(By.ID, field_id)
                print(f"[SUCCESS] Found password field: {field_id}")
                break
            except NoSuchElementException:
                continue
        
        if not password_field:
            input_fields = driver.find_elements(By.TAG_NAME, "input")
            password_inputs = [inp for inp in input_fields if inp.get_attribute("type") == "password"]
            if password_inputs:
                password_field = password_inputs[0]
                print("[SUCCESS] Found password field by type")
        
        if not registration_field or not password_field:
            print("[ERROR] Could not locate login form fields!")
            return False
        
        # Enter credentials
        print(f"[INFO] Entering credentials...")
        registration_field.clear()
        registration_field.send_keys(REGISTRATION_NUMBER)
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        time.sleep(1)
        
        # Find and click submit button
        submit_button = None
        possible_submit_ids = ["ContentPlaceHolder1_btnLogin", "btnLogin"]
        
        for button_id in possible_submit_ids:
            try:
                submit_button = driver.find_element(By.ID, button_id)
                print(f"[SUCCESS] Found submit button: {button_id}")
                break
            except NoSuchElementException:
                continue
        
        if not submit_button:
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            if submit_buttons:
                submit_button = submit_buttons[0]
        
        if not submit_button:
            print("[ERROR] Could not find submit button!")
            return False
        
        print("[INFO] Clicking login button...")
        submit_button.click()
        
        time.sleep(3)
        
        # Check if login was successful
        current_url = driver.current_url
        print(f"[INFO] Current URL: {current_url}")
        
        if "Login" not in current_url:
            print("[SUCCESS] Login successful!")
            return True
        else:
            print("[WARNING] Still on login page. Login may have failed.")
            return False
            
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return False

def navigate_to_unit_registration(driver):
    """
    Navigate to the Unit Registration page.
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        bool: True if navigation successful
    """
    try:
        print(f"\n[INFO] Navigating to Unit Registration page...")
        driver.get(UNIT_REGISTRATION_URL)
        time.sleep(3)
        
        print(f"[SUCCESS] Navigated to: {driver.current_url}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to navigate to Unit Registration: {e}")
        return False

def extract_and_display_units(driver):
    """
    Extract available units from the Unit Registration page and display them.
    
    Args:
        driver: Selenium WebDriver instance
    """
    try:
        print("\n" + "=" * 80)
        print("AVAILABLE UNITS")
        print("=" * 80)
        
        # Strategy 1: Look for dropdown/select elements containing units
        print("\n[INFO] Searching for unit selection elements...")
        
        # Try to find unit dropdowns
        selects = driver.find_elements(By.TAG_NAME, "select")
        
        for idx, select_elem in enumerate(selects):
            try:
                select = Select(select_elem)
                options = select.options
                
                # Filter out empty or placeholder options
                unit_options = [opt for opt in options if opt.text.strip() and opt.text.strip() not in ["Select", "-- Select --", ""]]
                
                if unit_options:
                    print(f"\n[FOUND] Unit Selection Dropdown {idx + 1}:")
                    for i, option in enumerate(unit_options, 1):
                        print(f"  {i}. {option.text}")
            except:
                continue
        
        # Strategy 2: Look for tables containing unit information
        print("\n[INFO] Searching for unit tables...")
        
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        for idx, table in enumerate(tables):
            try:
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                # Check if this table has unit-related content
                if len(rows) > 0:
                    header_text = rows[0].text.lower()
                    
                    if any(keyword in header_text for keyword in ['unit', 'course', 'code', 'name', 'credit']):
                        print(f"\n[FOUND] Unit Table {idx + 1}:")
                        print("-" * 80)
                        
                        for row in rows[:15]:  # Limit to first 15 rows
                            cells = row.find_elements(By.TAG_NAME, "td")
                            if not cells:
                                cells = row.find_elements(By.TAG_NAME, "th")
                            
                            row_text = " | ".join([cell.text.strip() for cell in cells if cell.text.strip()])
                            if row_text:
                                print(f"  {row_text}")
                        
                        print("-" * 80)
            except:
                continue
        
        # Strategy 3: Look for checkboxes with unit labels
        print("\n[INFO] Searching for unit checkboxes/radio buttons...")
        
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'], input[type='radio']")
        
        unit_checkboxes = []
        for checkbox in checkboxes:
            try:
                # Get the label or nearby text for this checkbox
                checkbox_id = checkbox.get_attribute('id')
                if checkbox_id:
                    # Try to find associated label
                    try:
                        label = driver.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
                        label_text = label.text.strip()
                        if label_text and len(label_text) > 3:
                            unit_checkboxes.append(label_text)
                    except:
                        # Try to get text from parent or sibling
                        parent = checkbox.find_element(By.XPATH, "..")
                        parent_text = parent.text.strip()
                        if parent_text and len(parent_text) > 3 and len(parent_text) < 200:
                            unit_checkboxes.append(parent_text)
            except:
                continue
        
        if unit_checkboxes:
            print(f"\n[FOUND] {len(unit_checkboxes)} Units with Selection Options:")
            for i, unit in enumerate(unit_checkboxes[:20], 1):  # Limit to first 20
                print(f"  {i}. {unit}")
        
        # Strategy 4: Look for any list items or divs with unit information
        print("\n[INFO] Searching for unit listings...")
        
        # Search for common unit code patterns (e.g., CIT 101, BICT 201, etc.)
        all_text_elements = driver.find_elements(By.CSS_SELECTOR, "div, span, li, td")
        
        unit_codes = set()
        for elem in all_text_elements:
            text = elem.text.strip()
            # Look for patterns like "CIT 101", "BICT-201", etc.
            import re
            matches = re.findall(r'\b[A-Z]{2,5}[\s-]?\d{3}\b', text)
            for match in matches:
                if len(text) < 300:  # Avoid capturing large blocks
                    unit_codes.add(text)
        
        if unit_codes:
            print(f"\n[FOUND] Potential Unit Entries:")
            for i, code in enumerate(sorted(list(unit_codes))[:30], 1):
                if len(code) > 5:  # Filter very short entries
                    print(f"  {i}. {code}")
        
        # Strategy 5: Save page source for manual inspection if needed
        print("\n[INFO] Saving page source to 'unit_registration_page.html' for detailed inspection...")
        try:
            with open("unit_registration_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("[SUCCESS] Page source saved!")
        except Exception as e:
            print(f"[WARNING] Could not save page source: {e}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"[ERROR] Failed to extract units: {e}")

def register_units(driver):
    """
    Attempt to register units (automated registration).
    This is a placeholder that can be customized based on actual requirements.
    
    Args:
        driver: Selenium WebDriver instance
    """
    print("\n[INFO] Unit registration functionality can be added here based on page structure")
    print("[INFO] For safety, automatic registration is disabled by default")
    print("[INFO] Please review the extracted units and page source to implement registration logic")

def main():
    """Main execution function."""
    driver = None
    
    try:
        print("=" * 80)
        print("MMU STUDENT PORTAL - UNIT REGISTRATION TOOL")
        print("=" * 80)
        
        driver = setup_driver()
        
        # Step 1: Login
        if not login_to_portal(driver):
            print("\n[ERROR] Login failed. Exiting...")
            return
        
        # Step 2: Navigate to Unit Registration
        if not navigate_to_unit_registration(driver):
            print("\n[ERROR] Could not navigate to Unit Registration page. Exiting...")
            return
        
        # Step 3: Extract and display units
        extract_and_display_units(driver)
        
        # Step 4: Registration (placeholder)
        # register_units(driver)
        
        # Keep browser open for inspection
        print("\n[INFO] Browser will remain open for 60 seconds for inspection...")
        print("[INFO] Press Ctrl+C to close immediately")
        time.sleep(60)
        
    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
    finally:
        if driver:
            print("\n[INFO] Closing browser...")
            driver.quit()
            print("[INFO] Done!")

if __name__ == "__main__":
    main()
