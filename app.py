from flask import Flask, render_template, request, jsonify
from chatbot import run_chatbot  # your Gemini function wrapper
from financials import get_financials
import pandas as pd
import json
import os
app = Flask(__name__)
# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('home.html')
# -----------------------------
# CHATBOT UI PAGE
# -----------------------------
@app.route('/chat')
def chat():
    return render_template('chatbot.html')
# -----------------------------
# CHATBOT API ENDPOINT
# -----------------------------
@app.route('/chat_api', methods=['POST'])
def chat_api():
    user_message = request.json.get("message")
    reply = run_chatbot(user_message)
    return jsonify({"reply": reply})
# -----------------------------
# VIEW FINANCIAL DATA (TABLE)
# -----------------------------
@app.route('/financials', methods=['GET', 'POST'])
def financials_page():
    if request.method == 'POST':
        symbol = request.form.get("symbol")
        data = get_financials(symbol)
        return render_template("financials.html", data=data)
    return render_template("financials.html", data=None)
# -----------------------------
# VIEW SAVED SCRAPED DATA
# -----------------------------
@app.route('/data', methods=['GET', 'POST'])
def data_page():
    items = {}
    # Load all saved data sources
    if os.path.exists("data/marketaux.csv"):
        items["marketaux"] = pd.read_csv("data/marketaux.csv").to_dict(orient="records")
    if os.path.exists("data/subreddit_data.csv"):
        items["reddit"] = pd.read_csv("data/subreddit_data.csv").to_dict(orient="records")
    if os.path.exists("data/final_data.json"):
        with open("data/final_data.json", "r") as f:
            items["final"] = json.load(f)
    # Handle POST (search/filter)
    if request.method == "POST":
        query = request.form.get("query", "").lower()
        filtered = {}
        for source, rows in items.items():
            if isinstance(rows, list):  # e.g., CSV → list of dicts
                filtered_rows = []
                for r in rows:
                    # check any column that contains the query
                    if any(query in str(v).lower() for v in r.values()):
                        filtered_rows.append(r)
                filtered[source] = filtered_rows
            else:
                filtered[source] = rows  # JSON dict
        return render_template("data.html", items=filtered, query=query)
    return render_template("data.html", items=items, query=None)
# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)