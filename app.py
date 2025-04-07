from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

def fetch_live_headlines():
    try:
        response = requests.get(NEWS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        headlines = [article["title"] for article in articles if article.get("title")][:5]
        return headlines
    except requests.RequestException as e:
        return [f"Error fetching news: {e}"]

@app.route("/", methods=["GET", "POST"])
def index():
    headlines = fetch_live_headlines()
    feedback = None
    if request.method == "POST":
        feedback = request.form.get("feedback")
        print(f"User Feedback: {feedback}")
    return render_template("index.html", headlines=headlines, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
