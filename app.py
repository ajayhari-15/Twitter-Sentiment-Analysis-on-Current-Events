from flask import Flask, request, jsonify, render_template
from sentiment import analyze_sentiment  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")  # Load HTML page

@app.route('/analyze', methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Text is required!"}), 400

        text = data["text"].strip()
        if not text:
            return jsonify({"error": "Text cannot be empty!"}), 400

        # Sentiment Analysis Call
        result = analyze_sentiment(text)
        return jsonify(result)

    except ConnectionError:
        return jsonify({"error": "Connection Error! API is unreachable."}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
