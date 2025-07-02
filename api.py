import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
BASE_URL = "https://api.twitter.com/2/tweets/search/recent"
QUERY = "Twitter"

def get_rate_limit(headers):
    """Extract remaining requests and reset time from headers."""
    limit = headers.get("x-rate-limit-remaining")
    reset_time = headers.get("x-rate-limit-reset")
    
    if limit is not None and reset_time is not None:
        return int(limit), int(reset_time)
    return None, None

def wait_for_limit_reset(reset_time):
    """Wait until the rate limit resets."""
    current_time = time.time()
    wait_time = reset_time - current_time
    if wait_time > 0:
        print(f"Rate limit exceeded. Waiting for {int(wait_time)} seconds...")
        time.sleep(wait_time + 1)  # Extra 1 second buffer

def fetch_tweets():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {"query": QUERY}
    
    max_retries = 3
    attempt = 0
    
    while attempt < max_retries:
        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            status_code = response.status_code
            
            if status_code == 200:
                remaining_requests, reset_time = get_rate_limit(response.headers)
                print(f"✅ Success! Remaining Requests: {remaining_requests}")
                return {"status": "success", "data": response.json()}
            elif status_code == 401:
                return {"status": "error", "message": "Unauthorized: Check Bearer Token"}
            elif status_code == 403:
                return {"status": "error", "message": "Forbidden: Access Denied"}
            elif status_code == 404:
                return {"status": "error", "message": "Not Found: Check URL or Query"}
            elif status_code == 429:
                remaining_requests, reset_time = get_rate_limit(response.headers)
                if reset_time:
                    wait_for_limit_reset(reset_time)
                else:
                    print("Rate limit reached. Retrying in 60 seconds...")
                    time.sleep(60)
            elif status_code == 500:
                return {"status": "error", "message": "Internal Server Error: Try Again Later"}
            else:
                print(f"⚠️ Error {status_code}: {response.json()} - Retrying...")
                time.sleep(5)  # Short delay before retrying
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Request Error: {str(e)}"}
        
        attempt += 1
    
    print("❌ Max retries reached. Could not fetch tweets.")
    return {"status": "error", "message": "Max retries reached"}

if __name__ == "__main__":
    start_time = time.time()
    result = fetch_tweets()
    end_time = time.time()
    
    if result["status"] == "success":
        print(f"✅ Data received in {end_time - start_time:.2f} seconds.")
    print(result)
