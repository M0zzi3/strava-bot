import os
import requests
from pathlib import Path

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
LAST_ID_FILE = Path("last_id.txt")


def get_access_token():
    url = "https://www.strava.com/oauth/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]


def get_recent_activities(access_token):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": 10}  # Get last 10
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()


def mute_activity(access_token, activity_id):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"muted": "true"}
    r = requests.put(url, headers=headers, data=data)
    r.raise_for_status()


def read_last_id():
    if LAST_ID_FILE.exists():
        return int(LAST_ID_FILE.read_text().strip())
    return 0


def write_last_id(activity_id):
    LAST_ID_FILE.write_text(str(activity_id))


def main():
    access_token = get_access_token()
    activities = get_recent_activities(access_token)

    last_id = read_last_id()
    new_last_id = last_id

    for activity in activities:
        activity_id = activity["id"]

        # Skip if activity was already precessed
        if activity_id <= last_id:
            continue

        if activity["type"] == "Ride" and not activity.get("muted", False):
            print(f"Muting activity {activity_id} ({activity['name']})")
            mute_activity(access_token, activity_id)

        # Set new latest ID
        if activity_id > new_last_id:
            new_last_id = activity_id

    # Save latest ID
    if new_last_id > last_id:
        write_last_id(new_last_id)


if __name__ == "__main__":
    main()
