# Email Notification Examples

This document shows what emails you'll receive from the Unit Registration Checker.

---

## 1. Units Available ✅

**Subject:** `✅ MMU Units Available!`

**Email Preview:**

```
┌─────────────────────────────────────────┐
│   📚 MMU Unit Registration Check         │
│   Automated Status Report                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ✅ UNITS CAN BE REGISTERED!              │
│                                          │
│ 5 units available with checkboxes.      │
└─────────────────────────────────────────┘

📊 Check Details
┌──────────────────┬─────────────────────┐
│ Status:          │ available           │
│ Can Register:    │ ✅ YES              │
│ Units Found:     │ 5                   │
│ Checked At:      │ 2026-02-01 16:00:00 │
└──────────────────┴─────────────────────┘

📋 Available Units
[
  "CIT 101 | Introduction to Computing",
  "CIT 102 | Programming Fundamentals",
  "CIT 103 | Web Development",
  ...
]

[🔗 Go to Registration Page]

────────────────────────────────────────
Next Check: In 6 hours
This is an automated status report from 
your MMU Portal Bot.

🤖 Powered by GitHub Actions | 📧 Notification System Active
```

---

## 2. Error Occurred ⚠️

**Subject:** `⚠️ MMU Registration Check - Error`

**Email Preview:**

```
┌─────────────────────────────────────────┐
│   📚 MMU Unit Registration Check         │
│   Automated Status Report                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ⚠️ Error Occurred                        │
│                                          │
│ You need to pay 5% of your tution fee   │
│ before registering for units. You       │
│ should pay at least Ksh.9,142           │
└─────────────────────────────────────────┘

📊 Check Details
┌──────────────────┬─────────────────────┐
│ Status:          │ error               │
│ Can Register:    │ ❌ NO               │
│ Units Found:     │ 0                   │
│ Checked At:      │ 2026-02-01 16:00:00 │
└──────────────────┴─────────────────────┘

❗ Error Message

You need to pay 5% of your tution fee
before registering for units. You should
pay at least Ksh.9,142

This usually means you need to meet payment
requirements before registering.

────────────────────────────────────────
Next Check: In 6 hours
This is an automated status report from 
your MMU Portal Bot.

🤖 Powered by GitHub Actions | 📧 Notification System Active
```

---

## 3. No Units Yet ℹ️

**Subject:** `ℹ️ MMU Registration Check - No Units Yet`

**Email Preview:**

```
┌─────────────────────────────────────────┐
│   📚 MMU Unit Registration Check         │
│   Automated Status Report                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ℹ️ No Units Available Yet                │
│                                          │
│ Registration is not open at this time.  │
└─────────────────────────────────────────┘

📊 Check Details
┌──────────────────┬─────────────────────┐
│ Status:          │ not_available       │
│ Can Register:    │ ❌ NO               │
│ Units Found:     │ 0                   │
│ Checked At:      │ 2026-02-01 16:00:00 │
└──────────────────┴─────────────────────┘

────────────────────────────────────────
Next Check: In 6 hours
This is an automated status report from 
your MMU Portal Bot.

🤖 Powered by GitHub Actions | 📧 Notification System Active
```

---

## Email Features

✅ **Always Sent** - Every 6 hours, regardless of status
✅ **Styled HTML** - Professional, easy-to-read format
✅ **Color Coded** - Green (available), Orange (error), Gray (not available)
✅ **Detailed Info** - Status, unit count, timestamp
✅ **Error Messages** - Shows exact payment/requirement messages
✅ **List of Units** - When available, shows all units
✅ **Direct Link** - Button to go to registration page
✅ **Next Check Time** - Reminds you when the next check is

---

## What Each Status Means

### ✅ Units Available
- **Action Required:** Register immediately!
- **What to do:** Click the link, select units, submit

### ⚠️ Error  
- **Common Causes:**
  - Payment requirement not met
  - Account hold
  - System maintenance
- **What to do:** Address the error message (usually payment)

### ℹ️ No Units Yet
- **Meaning:** Registration period hasn't started
- **What to do:** Wait for next check (6 hours)

---

## Frequency

You'll receive an email:
- ⏰ Every 6 hours
- 📅 4 emails per day
- 📊 ~120 emails per month

**Note:** Emails will continue until you disable the workflow or move the repository.

---

## Managing Email Volume

If you find the emails too frequent:

1. **Change Schedule** - Edit the cron in workflow file
   ```yaml
   - cron: '0 */12 * * *'  # Every 12 hours instead
   ```

2. **Email Filter** - Create Gmail filter
   - Filter: `from:(your-bot-email) subject:(MMU)`
   - Action: Apply label "MMU Bot", Skip Inbox
   - Check labels when convenient

3. **Disable Emails** - Keep GitHub Issues only
   - Comment out email step in workflow
   - Check GitHub Issues tab instead

---

## Troubleshooting

### Not Receiving Emails?

1. Check spam folder
2. Verify GitHub Secrets are set correctly
3. Check workflow logs for email errors
4. Try a different email service

### Getting Too Many Emails?

- Adjust the schedule (less frequent)
- Use email filters to organize
- Switch to GitHub Issues only

---

**You'll always know the registration status! 📧✨**
