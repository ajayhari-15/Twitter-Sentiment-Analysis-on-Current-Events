import os
import sys
import subprocess

REQUIRED_PACKAGES = ["flask", "requests", "pandas", "textblob"]

def install_packages():
    """Check and install required packages automatically."""
    try:
        for package in REQUIRED_PACKAGES:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("\n✅ All required packages are installed!")
    except Exception as e:
        print(f"\n❌ Error installing packages: {e}")

def check_sentiment_module():
    """Check if the sentiment module exists."""
    if not os.path.exists("sentiment/sentiment.py"):
        print("\n❌ Sentiment module is missing! Make sure 'sentiment/sentiment.py' exists.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n🔍 Checking setup...")
    install_packages()
    check_sentiment_module()
    print("\n✅ Setup completed successfully! Run `python app.py` now.")
