import requests
from requests.auth import HTTPBasicAuth
from config import CLIENT_ID, CLIENT_SECRET

def generate_access_token():
    url = "https://api.twitter.com/oauth2/token"
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, auth=auth, data=data)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        print("✅ Access Token:", access_token)
        return access_token
    else:
        print("❌ Error:", response.status_code, response.json())
        return None
