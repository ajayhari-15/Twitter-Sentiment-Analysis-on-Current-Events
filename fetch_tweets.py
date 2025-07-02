import requests
import config

def fetch_tweets(query, count=10):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={count}"

    headers = {
        "Authorization": f"Bearer {config.BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tweets = response.json()
        return tweets["data"]
    else:
        print("Error:", response.status_code)
        return []

if __name__ == "__main__":
    query = input("Enter the keyword: ")
    tweets = fetch_tweets(query)
    
    if tweets:
        print("Tweets Fetched Successfully!")
        for tweet in tweets:
            print(tweet["text"])
    else:
        print("No tweets found.")
