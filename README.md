Strava Auto-Mute Bot – Setup Instructions
This guide explains how to set up the Strava Auto-Mute Bot in your own GitHub repository.

1️⃣ Fork or clone the repository
git clone https://github.com/<your-username>/strava-auto-mute.git
cd strava-auto-mute

2️⃣ Create last_id.txt
echo 0 > last_id.txt
git add last_id.txt
git commit -m "chore: initialize last_id.txt"
git push
This file stores the ID of the last processed activity.

3️⃣ Add Strava API credentials to GitHub
Go to your repository → Settings → Secrets and variables → Actions → New repository secret.
Add the following secrets:
Name	Value
STRAVA_CLIENT_ID	<your Strava client ID>
STRAVA_CLIENT_SECRET	<your Strava client secret>
STRAVA_REFRESH_TOKEN	<your Strava refresh token>

4️⃣ Verify Python script
Ensure mute_rides.py is present.
It already fetches new activities, logs them, and updates last_id.txt.

5️⃣ Configure GitHub Actions
Ensure workflow file .github/workflows/mute.yml exists.
This workflow:
Runs every 5 minutes (adjustable via cron)
Can also be triggered manually via Run workflow
Updates last_id.txt and commits changes with a summary
Set workflow permissions:
Go to Settings → Actions → General → Workflow permissions
Select Read and write permissions
Save changes

6️⃣ Run the bot
Option 1: Manual run
Go to Actions → Auto-Mute Strava Rides → Run workflow
Select branch main (or your branch)
Click Run workflow
Option 2: Scheduled run
The workflow runs automatically according to the cron schedule in .github/workflows/mute.yml.

7️⃣ Check logs
Go to Actions → Auto-Mute Strava Rides → latest run.
Logs show a summary of new activities detected in that run.

8️⃣ Optional
Adjust the cron schedule in .github/workflows/mute.yml if you want a different interval:
schedule:
  - cron: "*/10 * * * *"  # every 10 minutes
Increase per_page in mute_rides.py to fetch more activities if needed.
This is all you need to set up the bot and run it for yourself.
