# GitHub Actions Deployment Guide

This guide explains how to deploy the MMU Student Portal bots to GitHub Actions for automatic execution every 6 hours.

## Overview

The GitHub Actions workflows will:
- ✅ Run automatically every 6 hours
- ✅ Use headless Chrome (no UI needed)
- ✅ Securely store credentials in GitHub Secrets
- ✅ Upload logs as artifacts for review
- ✅ Can be triggered manually anytime

---

## Setup Instructions

### Step 1: Push Code to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   cd C:\Users\natha\mmubot
   git init
   git add .
   git commit -m "Initial commit: MMU Student Portal bots"
   ```

2. **Create GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `mmu-portal-bot`)
   - Don't initialize with README (we already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/mmu-portal-bot.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Set Up GitHub Secrets

GitHub Secrets are used to store your credentials securely. They are encrypted and never exposed in logs.

1. **Go to your repository on GitHub**
2. **Click** `Settings` → `Secrets and variables` → `Actions`
3. **Click** `New repository secret`
4. **Add the following secrets**:

   | Secret Name | Value |
   |-------------|-------|
   | `MMU_REG_NUMBER` | Your registration number (e.g., `cit-223-101/2023`) |
   | `MMU_PASSWORD` | Your student portal password |

   **To add each secret:**
   - Click "New repository secret"
   - Enter the name exactly as shown
   - Paste your value
   - Click "Add secret"

---

### Step 3: Enable GitHub Actions

1. **Go to** `Actions` tab in your repository
2. **You should see two workflows**:
   - `MMU Portal Auto-Login`
   - `MMU Portal Balance Check`
3. **Click** on each workflow and enable it if prompted

---

### Step 4: Test the Workflows

**Option A: Wait for scheduled run** (next 6-hour interval)

**Option B: Trigger manually**:
1. Go to `Actions` tab
2. Click on `MMU Portal Auto-Login`
3. Click `Run workflow` dropdown
4. Click the green `Run workflow` button

---

## Workflow Details

### Auto-Login Workflow (`auto-login.yml`)

- **Schedule**: Every 6 hours (0:00, 6:00, 12:00, 18:00 UTC)
- **What it does**:
  - Logs into MMU Student Portal
  - Checks balance
  - Uploads logs as artifacts
- **Manual trigger**: Yes

### Balance Check Workflow (`balance-check.yml`)

- **Schedule**: Every 6 hours (1:00, 7:00, 13:00, 19:00 UTC) - offset by 1 hour
- **What it does**:
  - Logs in and checks account balance
  - Uploads logs as artifacts
- **Manual trigger**: Yes

---

## Viewing Logs

After each workflow run:

1. Go to `Actions` tab
2. Click on the workflow run (e.g., "MMU Portal Auto-Login")
3. Click on the job name (e.g., "auto-login")
4. View the console output in the step logs
5. Download artifacts if logs were generated

---

## Customizing Schedule

To change the schedule, edit the `cron` expression in the workflow files:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

**Common schedules**:
- Every 6 hours: `'0 */6 * * *'`
- Every 12 hours: `'0 */12 * * *'`
- Every day at 8am UTC: `'0 8 * * *'`
- Every Monday at 9am UTC: `'0 9 * * 1'`

**Cron syntax**: `minute hour day month day-of-week`

---

## Important Notes

### ⚠️ Security

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use GitHub Secrets** for credentials, not code
3. **GitHub Secrets are encrypted** and never shown in logs
4. **Rotate your password** if you suspect it's compromised

### 🔋 GitHub Actions Limits

- **Free tier**: 2,000 minutes/month for private repos
- **Public repos**: Unlimited
- Each bot run takes ~1-2 minutes
- Running every 6 hours = 4 runs/day = ~120 runs/month = ~240 minutes/month

### 🌍 Timezone

- GitHub Actions uses **UTC timezone**
- Kenya is **UTC+3**
- So `0:00 UTC` = `3:00 AM EAT` (East Africa Time)

**Schedule in EAT**:
- `0 */6 * * *` runs at: 3am, 9am, 3pm, 9pm EAT

---

## Troubleshooting

### Workflow fails with "Credentials not found"

**Solution**: Check that GitHub Secrets are set correctly:
- Exact names: `MMU_REG_NUMBER` and `MMU_PASSWORD`
- No extra spaces
- Values are correct

### Chrome/ChromeDriver issues

**Solution**: The workflow automatically installs Chrome. If it fails:
- Check the "Install Chrome and ChromeDriver" step logs
- Ensure `selenium>=4.6.0` in requirements.txt

### Workflow doesn't run automatically

**Solution**:
1. Ensure workflows are enabled (Actions tab)
2. Check cron syntax is valid
3. GitHub Actions may delay up to 15 minutes from scheduled time
4. Repository must have activity in the last 60 days

### Login fails

**Solution**:
- Verify credentials in GitHub Secrets
- Check if MMU portal changed their login process
- Review workflow logs for specific errors

---

## Disabling Workflows

To temporarily disable:

1. Go to `Actions` tab
2. Click on workflow name
3. Click `...` (three dots) → `Disable workflow`

To permanently remove:

```bash
# Delete workflow files
rm .github/workflows/auto-login.yml
rm .github/workflows/balance-check.yml
git commit -am "Remove GitHub Actions workflows"
git push
```

---

## Cost Comparison

| Option | Cost | Setup | Maintenance |
|--------|------|-------|-------------|
| **Local PC running 24/7** | ~$10-20/month in electricity | Easy | Medium (PC must stay on) |
| **GitHub Actions (free tier)** | $0 | Medium | Low (fully automated) |
| **Cloud VM** | ~$5-10/month | Hard | Medium |

**Recommendation**: Use GitHub Actions for free, automated, maintenance-free operation!

---

## Next Steps

After deployment:

1. ✅ Monitor first few runs to ensure everything works
2. ✅ Check artifacts/logs after each run
3. ✅ Adjust schedule if needed
4. ✅ Consider adding notifications (email, Discord, Telegram)
5. ✅ Keep repository private if it contains sensitive code

---

## Support

If you encounter issues:

1. Check workflow logs in GitHub Actions
2. Review this guide
3. Check GitHub Actions documentation: https://docs.github.com/en/actions
4. Verify MMU portal is accessible

---

**Your bots are now running automatically in the cloud! 🚀**
