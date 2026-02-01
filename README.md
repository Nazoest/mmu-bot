# MMU Student Portal Login Bot

This bot automates the login process for the Multimedia University of Kenya (MMU) Student Portal.

## 📁 Files

- **`student_portal_login.py`** - One-time login with visible browser (for testing)
- **`auto_login_background.py`** - Automatic login every 45 minutes in background (headless mode)
- **`unit_registration.py`** - Extract and display available units from Unit Registration page
- **`course_registration_bot.py`** - Automated course registration with dropdown selection
- **`run_background.bat`** - Easy launcher for the background bot

## Features

- ✅ Automatically navigates to the student portal
- ✅ Clicks the "Student Login" button
- ✅ Enters your registration number and password
- ✅ Submits the login form
- ✅ **NEW**: Auto-login every 45 minutes in background mode (no visible browser)
- ✅ **NEW**: Logging to file for monitoring
- ✅ **NEW**: Account balance checking after login
- ✅ **NEW**: Unit registration page navigation and unit extraction
- ✅ **NEW**: Automated course registration with dropdown selection
- ✅ Handles multiple possible form field identifiers
- ✅ Provides detailed console output for debugging
- ✅ Error handling and timeout management

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- ChromeDriver (will be managed automatically)

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\natha\mmubot
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `selenium` - Web automation framework
   - `webdriver-manager` - Automatically manages ChromeDriver

## Usage

### Option 1: One-Time Login (Visible Browser)

For testing or manual login:

```bash
python student_portal_login.py
```

The script will:
1. Open Chrome browser
2. Navigate to the login page
3. Click "Student Login"
4. Enter credentials (registration number: `cit-223-101/2023`, password: `nathan115`)
5. Submit the login form
6. Keep the browser open for 30 seconds if successful

### Option 2: Automatic Background Login (Recommended)

**For continuous auto-login every 45 minutes in background (no visible browser):**

#### Quick Start (Windows):
Just double-click: **`run_background.bat`**

#### Or run manually:
```bash
python auto_login_background.py
```

**What it does:**
- 🔄 Automatically logs in every 45 minutes
- 👻 Runs in headless mode (no browser window visible)
- 📝 Saves logs to `mmu_login_bot.log`
- ♾️ Keeps running until you stop it (Ctrl+C)
- 🔁 Shows next scheduled login time after each run

**To stop the bot:**
- Press `Ctrl+C` in the terminal
- Or close the command window

**To check logs:**
- Open `mmu_login_bot.log` in the same folder
- Shows timestamp, status, and any errors for each login attempt

### Option 3: View and Extract Units

**To view available units for registration:**

```bash
python unit_registration.py
```

**What it does:**
- 🔐 Logs into the student portal
- 📚 Navigates to Unit Registration page
- 🔍 Extracts available units using multiple detection strategies:
  - Dropdown/select menus
  - Unit tables
  - Checkboxes/radio buttons
  - Pattern matching for unit codes
- 📋 Displays all found units in terminal
- 💾 Saves page source to `unit_registration_page.html` for inspection
- ⏱️ Keeps browser open for 60 seconds for manual review

### Option 4: Automated Course Registration

**To register for courses:**

```bash
python course_registration_bot.py
```

**What it does:**
- 🔐 Logs into the student portal
- 📚 Navigates to Unit Registration page
- 📋 Shows interactive registration type selection menu:
  - Course Registration
  - Supplementary
  - Retake
- ✅ Automatically selects registration type from dropdown
- 🔘 Clicks "Get Units To Register" button
- 📖 Extracts and displays all available units
- ⚠️ **Safety Feature**: Manual review required before submission
- 🖱️ Browser stays open for you to review and manually submit

**Safety Notice:** The bot loads and displays units but requires manual confirmation before submitting registration. This prevents accidental registrations.

### Customizing Credentials

To use different credentials, edit the configuration section in `student_portal_login.py`:

```python
# Configuration
LOGIN_URL = "https://studentportal.mmu.ac.ke/Student%20Login.aspx"
REGISTRATION_NUMBER = "your-registration-number"
PASSWORD = "your-password"
```

### Running in Headless Mode

To run without opening a visible browser window, uncomment this line in the `setup_driver()` function:

```python
chrome_options.add_argument("--headless")
```

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver errors:

1. Make sure Chrome browser is installed
2. Update Chrome to the latest version
3. The `webdriver-manager` package should automatically download the correct ChromeDriver

### Login Fails

If the login fails:

1. Check the console output for error messages
2. Verify your credentials are correct
3. The website might have changed its structure - check the element IDs in the script
4. Ensure you have internet connection

### Finding Form Field IDs

If the script can't find form fields:

1. The script tries multiple common field identifiers
2. If still failing, you can inspect the login page manually:
   - Open Chrome
   - Go to the login page
   - Right-click on input fields → Inspect
   - Find the `id` or `name` attribute
   - Update the lists in the script accordingly

## Script Behavior

- **Success**: Browser stays open for 30 seconds after successful login
- **Failure**: Browser stays open for 10 seconds to review errors
- **Interrupt**: Press `Ctrl+C` to stop the script at any time

## Security Note

⚠️ **Important**: This script contains your login credentials in plain text. Keep this file secure and do not share it publicly.

Consider using environment variables for better security:

```python
import os
REGISTRATION_NUMBER = os.getenv("MMU_REG_NUMBER")
PASSWORD = os.getenv("MMU_PASSWORD")
```

## License

This is a personal automation script. Use responsibly and in accordance with MMU's terms of service.
