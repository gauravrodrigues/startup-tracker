# Automation Setup Guide

This guide explains how to set up daily automated data refresh for the Startup Tracker dashboard.

## Option 1: GitHub Actions (Recommended)

### Setup Instructions

1. **Create the workflow directory structure:**
   ```bash
   mkdir -p .github/workflows
   ```

2. **Create the workflow file** `.github/workflows/daily-refresh.yml`:

   ```yaml
   name: Daily Startup Data Refresh

   on:
     schedule:
       # Run daily at 9 AM UTC (4 AM EST)
       - cron: '0 9 * * *'
     workflow_dispatch: # Allow manual trigger

   jobs:
     refresh-data:
       runs-on: ubuntu-latest
       
       steps:
       - name: Checkout repository
         uses: actions/checkout@v3
       
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.11'
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -r requirements.txt
       
       - name: Trigger data refresh
         env:
           APP_URL: ${{ secrets.APP_URL }}
         run: |
           if [ -n "$APP_URL" ]; then
             echo "Triggering data refresh on deployed app..."
             curl -X POST "$APP_URL/api/refresh" -H "Content-Type: application/json"
           else
             echo "APP_URL secret not set. Configure it in repository secrets."
           fi
       
       - name: Log completion
         run: |
           echo "Daily refresh completed at $(date)"
   ```

3. **Configure GitHub Secrets:**
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `APP_URL`
   - Value: Your deployed app URL (e.g., `https://startup-tracker.onrender.com`)
   - Save

4. **Test the workflow:**
   - Go to Actions tab in GitHub
   - Select "Daily Startup Data Refresh"
   - Click "Run workflow" to test manually

### Customizing the Schedule

Modify the cron expression to change the refresh frequency:
- `0 9 * * *` - Daily at 9 AM UTC
- `0 */6 * * *` - Every 6 hours
- `0 9 * * 1` - Every Monday at 9 AM UTC

## Option 2: Render Cron Jobs

If using Render.com for hosting, you can set up a cron job:

1. **Update render.yaml** to include a cron job:

   ```yaml
   services:
     - type: web
       name: startup-tracker
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT

     - type: cron
       name: startup-tracker-refresh
       env: python
       schedule: "0 9 * * *"
       buildCommand: pip install -r requirements.txt
       startCommand: curl -X POST https://startup-tracker.onrender.com/api/refresh
   ```

2. Commit and push the changes - Render will automatically detect and configure the cron job.

## Option 3: External Cron Service

Use services like:
- **UptimeRobot** - Free tier allows checking every 5 minutes
- **Cronitor** - Dedicated cron job monitoring
- **EasyCron** - Simple cron job service

Configuration:
- Method: POST
- URL: `https://your-app-url.onrender.com/api/refresh`
- Schedule: Daily at your preferred time

## Verification

To verify the automation is working:

1. **Check the API response:**
   ```bash
   curl https://your-app-url.onrender.com/api/dashboard
   ```
   Check the `last_updated` timestamp.

2. **Monitor GitHub Actions:**
   - Go to the Actions tab
   - View workflow run history
   - Check logs for any errors

3. **Dashboard UI:**
   - Open the dashboard
   - Check the "Last Updated" timestamp at the top

## Troubleshooting

### Workflow not running
- Ensure GitHub Actions is enabled in repository settings
- Check that the cron schedule is valid
- Verify the APP_URL secret is set correctly

### Refresh endpoint failing
- Check Render logs for the web service
- Ensure the app is not sleeping (Render free tier)
- Verify the API endpoint is accessible

### Data not updating
- Check the application logs
- Verify data source APIs are accessible
- Ensure no rate limiting is occurring

## Next Steps

After setting up automation:
1. Deploy the app to Render or your preferred hosting
2. Configure the GitHub Actions workflow
3. Set the APP_URL secret
4. Run a test workflow
5. Monitor the first few automated runs

---

**Note**: The free tier of Render.com may have the service sleep after 15 minutes of inactivity. Consider using the cron job to keep it active or upgrade to a paid plan.
