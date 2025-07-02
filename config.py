import os
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

