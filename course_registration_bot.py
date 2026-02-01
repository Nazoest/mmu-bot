"""
MMU Student Portal - Automated Course Registration Bot
This script logs in, navigates to Unit Registration, and automatically registers for courses.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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

def setup_driver(headless=False):
    """Initialize and configure the Chrome WebDriver."""
    chrome_options = Options()
    
    if headless:
        # Headless mode with CI-compatible flags
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        # Local mode with visible browser
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
        
        # Registration field
        registration_field = None
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        text_inputs = [inp for inp in input_fields if inp.get_attribute("type") in ["text", "password"]]
        if text_inputs:
            registration_field = text_inputs[0]
        
        # Password field
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
    """
    Select registration type from dropdown.
    
    Args:
        driver: Selenium WebDriver instance
        reg_type: Type of registration - "Course Registration", "Supplementary", or "Retake"
    """
    try:
        print(f"\n[INFO] Selecting registration type: {reg_type}")
        
        # Find the registration type dropdown
        dropdown = Select(driver.find_element(By.ID, "Main__ddlRegFor"))
        
        # Map registration type to value
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
        time.sleep(3)  # Wait for response
        
        # Check for SweetAlert error messages (common on this portal)
        try:
            # Look for SweetAlert modal
            swal_modal = driver.find_element(By.CSS_SELECTOR, ".swal2-modal[style*='display: block'], .swal2-modal[aria-hidden='false']")
            
            if swal_modal:
                # Extract error title
                try:
                    error_title = driver.find_element(By.CSS_SELECTOR, ".swal2-modal h2").text
                except:
                    error_title = ""
                
                # Extract error content
                try:
                    error_content = driver.find_element(By.CSS_SELECTOR, ".swal2-modal .swal2-content").text
                except:
                    error_content = ""
                
                if error_title or error_content:
                    print("\n" + "=" * 80)
                    print("⚠️  ERROR MESSAGE DETECTED")
                    print("=" * 80)
                    if error_title:
                        print(f"\n{error_title}")
                    if error_content:
                        print(f"\n{error_content}")
                    print("\n" + "=" * 80)
                    
                    # Close the alert
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, ".swal2-confirm, .swal2-close")
                        time.sleep(1)
                        close_button.click()
                        time.sleep(1)
                    except:
                        pass
                    
                    return False  # Error occurred
        except NoSuchElementException:
            # No SweetAlert, check for other error types
            pass
        
        # Check for page-level error messages
        try:
            error_divs = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .error-message, [style*='color: red'], [style*='color:red']")
            for error_div in error_divs:
                error_text = error_div.text.strip()
                if error_text and len(error_text) > 10:
                    print("\n" + "=" * 80)
                    print("⚠️  ERROR MESSAGE DETECTED")
                    print("=" * 80)
                    print(f"\n{error_text}\n")
                    print("=" * 80)
                    return False
        except:
            pass
        
        time.sleep(2)  # Additional wait for modal or page to load
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not click button: {e}")
        return False

def extract_available_units(driver):
    """Extract and display available units from the modal or page."""
    try:
        print("\n" + "=" * 80)
        print("AVAILABLE UNITS FOR REGISTRATION")
        print("=" * 80)
        
        units_found = False
        
        # Strategy 1: Look for units in dropdowns
        try:
            unit_dropdown_element = driver.find_element(By.ID, "Main__ddlUnits")
            unit_dropdown = Select(unit_dropdown_element)
            
            units = []
            for option in unit_dropdown.options:
                if option.text.strip() and option.text.strip() not in ["", "--Select--"]:
                    units.append({
                        'text': option.text.strip(),
                        'value': option.get_attribute('value')
                    })
            
            if units:
                units_found = True
                print(f"\n[FOUND] {len(units)} units available in dropdown:")
                for i, unit in enumerate(units, 1):
                    print(f"  {i}. {unit['text']}")
                
                print("\n" + "✅" * 40)
                print("✅  UNITS CAN BE REGISTERED!")
                print("✅  Use the dropdown to select and add units")
                print("✅" * 40)
                return units
                
        except NoSuchElementException:
            pass
        
        # Strategy 2: Look for checkboxes (main indicator of registrable units)
        try:
            # Look in modal first
            modal_checkboxes = driver.find_elements(By.CSS_SELECTOR, "#myModalCourseRegister input[type='checkbox']")
            
            if not modal_checkboxes:
                # Look in page
                modal_checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            
            if modal_checkboxes:
                units_found = True
                print(f"\n[FOUND] {len(modal_checkboxes)} selectable units (checkboxes)")
                
                units = []
                for cb in modal_checkboxes:
                    try:
                        # Get unit info from nearby elements
                        parent = cb.find_element(By.XPATH, "..")
                        
                        # Try to find label
                        try:
                            label = parent.find_element(By.TAG_NAME, "label")
                            unit_text = label.text.strip()
                        except:
                            unit_text = parent.text.strip()
                        
                        # Also check table row if checkbox is in a table
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
                            units.append({'element': cb, 'text': unit_text})
                            print(f"  ☑️  {unit_text}")
                    except:
                        continue
                
                if units:
                    print("\n" + "✅" * 40)
                    print("✅  UNITS CAN BE REGISTERED!")
                    print(f"✅  {len(units)} units available for selection")
                    print("✅  Check the boxes for units you want to register")
                    print("✅  Then click 'Submit Registration' button")
                    print("✅" * 40)
                    return units
        except Exception as e:
            print(f"[DEBUG] Checkbox detection error: {e}")
        
        # Strategy 3: Look for units in tables
        try:
            tables = driver.find_elements(By.TAG_NAME, "table")
            
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                if len(rows) > 1:
                    header_text = rows[0].text.lower() if rows else ""
                    
                    if any(keyword in header_text for keyword in ['unit', 'course', 'code']):
                        units_found = True
                        print(f"\n[FOUND] Units table with {len(rows)-1} units:")
                        
                        # Print header
                        header_cells = rows[0].find_elements(By.TAG_NAME, "th")
                        if not header_cells:
                            header_cells = rows[0].find_elements(By.TAG_NAME, "td")
                        
                        header = " | ".join([cell.text.strip() for cell in header_cells])
                        print(f"\n{header}")
                        print("-" * 80)
                        
                        # Print units
                        for row in rows[1:11]:  # First 10 units
                            cells = row.find_elements(By.TAG_NAME, "td")
                            row_text = " | ".join([cell.text.strip() for cell in cells if cell.text.strip()])
                            if row_text:
                                print(f"{row_text}")
                        
                        if len(rows) > 11:
                            print(f"... and {len(rows) - 11} more units")
                        
                        break
        except:
            pass
        
        if not units_found:
            print("\n❌ No units found")
            print("[INFO] This could mean:")
            print("  - No units available for this registration type")
            print("  - Registration not allowed (check error messages above)")
            print("  - Units need to be loaded differently")
        
        # Save page source for debugging
        print("\n[INFO] Saving current page source for inspection...")
        try:
            with open("registration_units_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("[SUCCESS] Page source saved to 'registration_units_page.html'")
        except Exception as e:
            print(f"[WARNING] Could not save page source: {e}")
        
        return []
        
    except Exception as e:
        print(f"[ERROR] Error extracting units: {e}")
        return []

def register_for_units(driver, unit_indices=None, auto_register_all=False):
    """
    Register for units.
    
    Args:
        driver: Selenium WebDriver instance
        unit_indices: List of unit indices to register (1-indexed), or None for manual selection
        auto_register_all: If True, automatically register for all available units
    """
    try:
        units = extract_available_units(driver)
        
        if not units:
            print("\n[WARNING] No units available for registration")
            return False
        
        if auto_register_all:
            print(f"\n[INFO] Auto-registering for ALL {len(units)} units...")
            # Implementation depends on page structure
            # This is a placeholder - actual implementation would select all checkboxes or add all from dropdown
            
        elif unit_indices:
            print(f"\n[INFO] Registering for selected units: {unit_indices}")
            # Implementation would select specific units
            
        else:
            print("\n[INFO] Manual mode - please review units above")
            print("[INFO] Browser will remain open for manual selection")
            print("[INFO] Press Ctrl+C when done")
            time.sleep(300)  # 5 minutes for manual selection
            return True
        
        # Look for submit button
        try:
            submit_button = driver.find_element(By.ID, "Main__btnRegisterCourse")
            print("\n[INFO] Found 'Submit Registration' button")
            print("[WARNING] Auto-submission is DISABLED for safety")
            print("[INFO] Please review selections and click 'Submit Registration' manually")
            time.sleep(60)  # Wait for manual submission
            return True
        except NoSuchElementException:
            print("[WARNING] Submit button not found")
            return False
            
    except Exception as e:
        print(f"[ERROR] Registration error: {e}")
        return False

def main():
    """Main execution function."""
    driver = None
    
    try:
        print("===" * 27)
        print("MMU STUDENT PORTAL - AUTOMATED COURSE REGISTRATION BOT")
        print("===" * 27)
        print("\nThis bot will:")
        print("1. Log into the student portal")
        print("2. Navigate to Unit Registration")
        print("3. Select 'Course Registration' type")
        print("4. Load available units")
        print("5. Display units for your review")
        print("\n" + "===" * 27)
        
        # Automatically use "Course Registration" as the registration type
        selected_reg_type = "Course Registration"
        print(f"\n[INFO] Registration Type: {selected_reg_type}")
        
        # Detect if running in GitHub Actions or CI environment
        is_ci = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"
        headless_mode = is_ci
        
        if is_ci:
            print("[INFO] Running in CI/GitHub Actions mode (headless)")
        else:
            print("[INFO] Running in local mode (with browser UI)")
        
        # Setup browser
        driver = setup_driver(headless=headless_mode)
        
        # Step 1: Login
        if not login_to_portal(driver):
            print("\n[ERROR] Login failed. Exiting...")
            return
        
        # Step 2: Navigate
        if not navigate_to_unit_registration(driver):
            print("\n[ERROR] Navigation failed. Exiting...")
            return
        
        # Step 3: Select registration type
        if not select_registration_type(driver, selected_reg_type):
            print("\n[ERROR] Could not select registration type. Exiting...")
            return
        
        # Step 4: Click button to load units
        if not click_get_units_button(driver):
            print("\n[WARNING] An error occurred or registration not allowed.")
            print("[INFO] Check the error message above for details.")
            
            # Shorter wait time in CI mode
            wait_time = 10 if is_ci else 60
            print(f"\n[INFO] Browser will remain open for {wait_time} seconds for manual review...")
            time.sleep(wait_time)
            return
        
        # Step 5: Display units and allow registration
        print("\n" + "=" * 80)
        print("UNITS LOADED - READY FOR REGISTRATION")
        print("=" * 80)
        
        register_for_units(driver, auto_register_all=False)
        
        print("\n[INFO] Registration process complete!")
        
        # Shorter wait time in CI mode
        wait_time = 5 if is_ci else 30
        print(f"[INFO] Browser will remain open for {wait_time} seconds...")
        time.sleep(wait_time)
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Script interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
    finally:
        if driver:
            print("\n[INFO] Closing browser...")
            driver.quit()
            print("[INFO] Done!")

if __name__ == "__main__":
    main()
