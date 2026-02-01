"""
MMU Student Portal - Unit Registration Notifier (Headless)
Checks if units are available for registration and sends notifications.
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
import sys
import json

# Configuration - Read from environment variables for security
LOGIN_URL = "https://studentportal.mmu.ac.ke/Student%20Login.aspx"
UNIT_REGISTRATION_URL = "https://studentportal.mmu.ac.ke/UnitRegistration.aspx"
REGISTRATION_NUMBER = os.getenv("MMU_REG_NUMBER")
PASSWORD = os.getenv("MMU_PASSWORD")
GITHUB_OUTPUT = os.getenv("GITHUB_OUTPUT")  # For GitHub Actions notifications

# Validate that credentials are set
if not REGISTRATION_NUMBER or not PASSWORD:
    print("=" * 80)
    print("ERROR: Credentials not found!")
    print("=" * 80)
    print("\nPlease set your credentials as environment variables:")
    print("  set MMU_REG_NUMBER=your-registration-number")
    print("  set MMU_PASSWORD=your-password")
    print("\n" + "=" * 80)
    sys.exit(1)

def setup_driver(headless=True):
    """Initialize and configure the Chrome WebDriver."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_portal(driver):
    """Log into the MMU Student Portal."""
    try:
        print(f"[INFO] Navigating to: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        
        wait = WebDriverWait(driver, 10)
        
        # Click "Student Login" button
        print("[INFO] Clicking 'Student Login' button...")
        student_login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnStudentLogin"))
        )
        student_login_button.click()
        time.sleep(2)
        
        # Find and fill login fields
        print("[INFO] Entering credentials...")
        
        registration_field = None
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        text_inputs = [inp for inp in input_fields if inp.get_attribute("type") in ["text", "password"]]
        if text_inputs:
            registration_field = text_inputs[0]
        
        password_field = None
        password_inputs = [inp for inp in input_fields if inp.get_attribute("type") == "password"]
        if password_inputs:
            password_field = password_inputs[0]
        
        if not registration_field or not password_field:
            print("[ERROR] Could not locate login form fields!")
            return False
        
        registration_field.clear()
        registration_field.send_keys(REGISTRATION_NUMBER)
        password_field.clear()
        password_field.send_keys(PASSWORD)
        time.sleep(1)
        
        # Submit
        submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
        if submit_buttons:
            print("[INFO] Clicking login button...")
            submit_buttons[0].click()
            time.sleep(3)
        
        # Check login success
        current_url = driver.current_url
        if "Login" not in current_url:
            print("[SUCCESS] Login successful!")
            return True
        else:
            print("[WARNING] Login may have failed.")
            return False
            
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return False

def navigate_to_unit_registration(driver):
    """Navigate to the Unit Registration page."""
    try:
        print(f"\n[INFO] Navigating to Unit Registration page...")
        driver.get(UNIT_REGISTRATION_URL)
        time.sleep(3)
        print(f"[SUCCESS] On Unit Registration page")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to navigate: {e}")
        return False

def select_registration_type(driver, reg_type="Course Registration"):
    """Select registration type from dropdown."""
    try:
        print(f"\n[INFO] Selecting registration type: {reg_type}")
        
        dropdown = Select(driver.find_element(By.ID, "Main__ddlRegFor"))
        
        reg_type_map = {
            "Course Registration": "0",
            "Supplementary": "2",
            "Retake": "3"
        }
        
        if reg_type in reg_type_map:
            dropdown.select_by_value(reg_type_map[reg_type])
            print(f"[SUCCESS] Selected: {reg_type}")
            time.sleep(1)
            return True
        else:
            print(f"[ERROR] Invalid registration type: {reg_type}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Could not select registration type: {e}")
        return False

def click_get_units_button(driver):
    """Click the 'Get Units To Register' button and check for errors."""
    try:
        print("\n[INFO] Clicking 'Get Units To Register' button...")
        
        button = driver.find_element(By.ID, "Main__btnRegister")
        button.click()
        
        print("[SUCCESS] Button clicked, checking for errors or loading units...")
        time.sleep(3)
        
        # Check for SweetAlert error messages
        try:
            swal_modal = driver.find_element(By.CSS_SELECTOR, ".swal2-modal[style*='display: block'], .swal2-modal[aria-hidden='false']")
            
            if swal_modal:
                try:
                    error_title = driver.find_element(By.CSS_SELECTOR, ".swal2-modal h2").text
                except:
                    error_title = ""
                
                try:
                    error_content = driver.find_element(By.CSS_SELECTOR, ".swal2-modal .swal2-content").text
                except:
                    error_content = ""
                
                if error_title or error_content:
                    error_msg = f"{error_title}\n{error_content}".strip()
                    print(f"\n[ERROR] {error_msg}")
                    
                    # Close the alert
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, ".swal2-confirm, .swal2-close")
                        time.sleep(1)
                        close_button.click()
                        time.sleep(1)
                    except:
                        pass
                    
                    return False, error_msg
        except NoSuchElementException:
            pass
        
        time.sleep(2)
        return True, None
        
    except Exception as e:
        error_msg = f"Could not click button: {e}"
        print(f"[ERROR] {error_msg}")
        return False, error_msg

def check_units_available(driver):
    """
    Check if units are available for registration.
    Returns: (can_register, unit_count, units_list, message)
    """
    try:
        print("\n[INFO] Checking for available units...")
        
        # Strategy 1: Check for checkboxes (main indicator)
        modal_checkboxes = driver.find_elements(By.CSS_SELECTOR, "#myModalCourseRegister input[type='checkbox']")
        
        if not modal_checkboxes:
            modal_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        
        if modal_checkboxes:
            units = []
            for cb in modal_checkboxes:
                try:
                    parent = cb.find_element(By.XPATH, "..")
                    
                    try:
                        label = parent.find_element(By.TAG_NAME, "label")
                        unit_text = label.text.strip()
                    except:
                        unit_text = parent.text.strip()
                    
                    try:
                        row = cb.find_element(By.XPATH, "ancestor::tr")
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if cells:
                            row_text = " | ".join([cell.text.strip() for cell in cells if cell.text.strip()])
                            if row_text:
                                unit_text = row_text
                    except:
                        pass
                    
                    if unit_text and len(unit_text) > 3:
                        units.append(unit_text)
                except:
                    continue
            
            if units:
                message = f"✅ UNITS CAN BE REGISTERED! {len(units)} units available with checkboxes."
                print(f"\n{'=' * 80}")
                print(message)
                print('=' * 80)
                for i, unit in enumerate(units, 1):
                    print(f"  {i}. {unit}")
                print('=' * 80)
                
                return True, len(units), units, message
        
        # Strategy 2: Check for dropdown
        try:
            unit_dropdown_element = driver.find_element(By.ID, "Main__ddlUnits")
            unit_dropdown = Select(unit_dropdown_element)
            
            units = []
            for option in unit_dropdown.options:
                if option.text.strip() and option.text.strip() not in ["", "--Select--"]:
                    units.append(option.text.strip())
            
            if units:
                message = f"✅ UNITS CAN BE REGISTERED! {len(units)} units available in dropdown."
                print(f"\n{'=' * 80}")
                print(message)
                print('=' * 80)
                for i, unit in enumerate(units, 1):
                    print(f"  {i}. {unit}")
                print('=' * 80)
                
                return True, len(units), units, message
                
        except NoSuchElementException:
            pass
        
        message = "❌ No units available for registration at this time."
        print(f"\n{message}")
        return False, 0, [], message
        
    except Exception as e:
        message = f"Error checking units: {e}"
        print(f"[ERROR] {message}")
        return False, 0, [], message

def write_github_output(key, value):
    """Write output for GitHub Actions."""
    if GITHUB_OUTPUT:
        with open(GITHUB_OUTPUT, "a") as f:
            f.write(f"{key}={value}\n")

def main():
    """Main execution function."""
    driver = None
    
    try:
        print("=" * 80)
        print("MMU STUDENT PORTAL - UNIT REGISTRATION NOTIFIER")
        print("Running in HEADLESS mode")
        print("=" * 80)
        
        # Setup headless browser
        driver = setup_driver(headless=True)
        
        # Step 1: Login
        if not login_to_portal(driver):
            print("\n[ERROR] Login failed. Exiting...")
            write_github_output("registration_status", "login_failed")
            write_github_output("can_register", "false")
            sys.exit(1)
        
        # Step 2: Navigate
        if not navigate_to_unit_registration(driver):
            print("\n[ERROR] Navigation failed. Exiting...")
            write_github_output("registration_status", "navigation_failed")
            write_github_output("can_register", "false")
            sys.exit(1)
        
        # Step 3: Select registration type
        if not select_registration_type(driver, "Course Registration"):
            print("\n[ERROR] Could not select registration type. Exiting...")
            write_github_output("registration_status", "selection_failed")
            write_github_output("can_register", "false")
            sys.exit(1)
        
        # Step 4: Click button to load units
        success, error_msg = click_get_units_button(driver)
        if not success:
            print(f"\n[WARNING] Error occurred: {error_msg}")
            write_github_output("registration_status", "error")
            write_github_output("error_message", error_msg or "Unknown error")
            write_github_output("can_register", "false")
            
            # Save page source for debugging
            try:
                with open("registration_error_page.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("[INFO] Page source saved to 'registration_error_page.html'")
            except:
                pass
            
            driver.quit()
            sys.exit(0)  # Not a failure, just can't register yet
        
        # Step 5: Check if units are available
        can_register, unit_count, units, message = check_units_available(driver)
        
        # Write outputs for GitHub Actions
        write_github_output("can_register", "true" if can_register else "false")
        write_github_output("unit_count", str(unit_count))
        write_github_output("registration_status", "available" if can_register else "not_available")
        write_github_output("message", message)
        
        if can_register and units:
            units_json = json.dumps(units[:10])  # First 10 units
            write_github_output("units_list", units_json)
        
        print(f"\n{'=' * 80}")
        print("FINAL STATUS:")
        print(f"  Can Register: {'YES ✅' if can_register else 'NO ❌'}")
        print(f"  Unit Count: {unit_count}")
        print(f"  Message: {message}")
        print('=' * 80)
        
        if can_register:
            print("\n🔔 NOTIFICATION: Units are available for registration!")
            print("    Check your email or GitHub for details.")
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Script interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        write_github_output("registration_status", "error")
        write_github_output("can_register", "false")
    finally:
        if driver:
            print("\n[INFO] Closing browser...")
            driver.quit()
            print("[INFO] Done!")

if __name__ == "__main__":
    main()
