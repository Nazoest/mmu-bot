# MMU Student Portal Login Bot

This bot automates the login process for the Multimedia University of Kenya (MMU) Student Portal.

## 🚀 Quick Setup for New Users

**Want to use this bot? It's easy!**

1. **Open the setup page:** [setup.html](setup.html) (Download this repo and open the file in your browser)
2. **Enter your credentials** (MMU registration number, password, and email)
3. **Follow the step-by-step instructions** to set up automation on GitHub
4. **Done!** The bot will automatically check course registration every 6 hours

**Benefits:**
- ✅ Automated course registration checking
- ✅ Smart email notifications (only when status changes)
- ✅ Balance tracking and unit registration monitoring  
- ✅ Completely free (runs on GitHub Actions)

---

## 📁 Files

- **`course_registration_bot.py`** - Automated course registration with dropdown selection

## Features

- ✅ Automatically navigates to the student portal
- ✅ Clicks the "Student Login" button
- ✅ Enters your registration number and password
- ✅ Submits the login form
- ✅ Submits the login form
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







### Automated Course Registration

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
