from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language(text):
    """
    Detects the language of the given text.
    """
    try:
        language = detect(text)
    except Exception as e:
        print(f"Language Detection Error: {e}")  # Debugging ke liye
        language = "unknown"
    return language

def analyze_sentiment(text):
    """
    Performs sentiment analysis on the given text.
    Supports multiple languages (English recommended for best results).
    """
    language = detect_language(text)

    # Convert non-English text to English for sentiment analysis
    if language != "en":
        try:
            translated_text = GoogleTranslator(source="auto", target="en").translate(text)
            if not translated_text:  # Kabhi kabhi empty response milta hai
                raise ValueError("Translation returned empty text")
        except Exception as e:
            print(f"Translation Error: {e}")  # Debugging ke liye
            return {"error": "Translation failed. Please use English text."}
    else:
        translated_text = text

    # Analyze sentiment using TextBlob
    analysis = TextBlob(translated_text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "original_text": text,
        "translated_text": translated_text,
        "detected_language": language,
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity
    }
