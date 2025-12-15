import google.generativeai as genai
from financials import get_financials
import pandas as pd
import json
import os
# -----------------------------
# Gemini Configuration
# -----------------------------
genai.configure(api_key="AIzaSyB_A6Kd0TSLAe84cMih9eIgHp3HzkROrR0")  # replace later
tools = [{
    "name": "get_financials",
    "description": "Fetch stock financial, insider trades, sentiment and news",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string"
            }
        },
        "required": ["symbol"]
    }
}]
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools={"function_declarations": tools}
)
# -----------------------------
# Function to save final JSON
# -----------------------------
def save_final_data(symbol, result):
    """Save full financial dataset to final_data.json."""
    filename = "data/final_data.json"
    if isinstance(result.get("articles"), pd.DataFrame):
        result["articles"] = result["articles"].to_dict(orient="records")
    # Ensure directory exists
    os.makedirs("data", exist_ok=True)
    # Load existing file
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                existing = json.load(f)
            except:
                existing = {}
    else:
        existing = {}
    # Save updated data
    existing[symbol] = result
    with open(filename, "w") as f:
        json.dump(existing, f, indent=4)
# -----------------------------
# MAIN CHATBOT FUNCTION
# -----------------------------
def run_chatbot(message: str) -> str:
    """
    Handles user messages, allows Gemini to call get_financials,
    and returns plain text to the Flask endpoint.
    """
    try:
        response = model.generate_content(message)
        # Check if model called a function
        for part in response.parts:
            fn = part.function_call
            if fn:
                name = fn.name
                args = fn.args
                # If Gemini calls get_financials(...)
                if name == "get_financials":
                    symbol = args["symbol"].upper()
                    # Call your real function
                    result = get_financials(symbol)
                    # Save as final_data.json
                    save_final_data(symbol, result)
                    # Return readable summary to chatbot UI
                    summary = (
                        f"Here are the financial details for {symbol}:\n\n"
                        f":pushpin: Sentiment Score: {result['sentiment']}\n"
                        f":pushpin: Sentiment Label: {result['label']}\n"
                        f":pushpin: Current Price: {result['quote'].get('c', 'N/A')}\n"
                        f":pushpin: Open: {result['quote'].get('o', 'N/A')}\n"
                        f":pushpin: High: {result['quote'].get('h', 'N/A')}\n"
                        f":pushpin: Low: {result['quote'].get('l', 'N/A')}\n"
                        f":pushpin: News Articles Fetched: {len(result['articles']) if result['articles'] else 0}\n"
                    )
                    return summary
        # If no function call, return raw model text
        if response.text:
            return response.text
        return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error processing message: {str(e)}"


# import google.generativeai as genai
# from analyzer import getSentiment, labelSentiment
# import finnhub
# import praw
# import csv
# from marketaux import news

# import pandas as pd
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import json

# analyzer = SentimentIntensityAnalyzer()
# df = pd.read_csv('subreddit_data.csv')
# sentimentScore = []
# sentimentLabel = []



# def pubOpinion(symbol):
#     reddit = praw.Reddit(client_id='oL_jGfUjbdA-dzu-VzGaqg',
#                          client_secret='cJWU0Phpaj-Pwp8fzE1EbutqU9X2pg',
#                          user_agent='reddit_scrapper/0.1')
#     with open('subreddit_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['title', 'upvotes', 'url', 'body'])
#         for post in reddit.subreddit('all').search(symbol, limit=50, sort='relevance'):
#             writer.writerow([post.title, post.score, post.url, post.selftext])

#     for text in df["body"]:
#         print(getSentiment(text))
#         if getSentiment(text) != 0:
#             sentimentScore.append(getSentiment(text))
#             sentimentLabel.append(labelSentiment(getSentiment(text)))


#     avgSentiment = sum(sentimentScore) / len(sentimentScore)
#     return avgSentiment, labelSentiment(avgSentiment)

# finnhub = finnhub.Client("d44ivg1r01qr9l8183v0d44ivg1r01qr9l8183vg")
# def get_financials(symbol):
#     sentiment, label = pubOpinion(symbol)
#     return {
#         "symbol": symbol,
#         "quote": finnhub.quote(symbol),
#         "news": finnhub.general_news(symbol),
#         "insider": finnhub.stock_insider_transactions(symbol),
#         "sentiment": sentiment,
#         "label": label,
#         "articles": news(symbol)
#     }
# tools = [{
#     "name": "get_financials",
#     "description": "Fetch stock financial data",
#     "parameters":
#         {
#             "type": "object",
#             "properties": {
#                 "symbol": {
#                     "type": "string"

#                 }
#             },
#             "required": ["symbol"]
#         }
#     }
#     ]


# genai.configure(api_key="AIzaSyB_A6Kd0TSLAe84cMih9eIgHp3HzkROrR0")
# model = genai.GenerativeModel(model_name = "gemini-2.5-flash", tools = {"function_declarations": tools})
# response = model.generate_content("Give me the stock details regarding IBM.")
# print(response)
# for part in response.parts:
#     if fn := part.function_call:
#         args = part.function_call.args
#         name = part.function_call.name
#         if name == "get_financials":
#             result = get_financials(args["symbol"])
#             with open('final_data.json', 'a+') as outfile:
#                 if args["symbol"] not in outfile:
#                     for k, v in result.items():
#                         if isinstance(v, pd.DataFrame):
#                             result[k] = v.to_dict(orient="records")
#                     fr = {}
#                     fr[args["symbol"]] = result
#                     json.dump(result, outfile, indent = 4)



# {
#   "candidates": [
#     {
#       "content": {
#         "parts": [
#           {
#             # 1. If it's normal text:
#             "text": "Let me analyze that portfolio for you..."
#
#             # 2. OR if a function is called:
#             "function_call": {
#                 "name": "optimize_portfolio",        # <-- function name
#                 "args": "{\"stocks\": [{\"symbol\": \"AAPL\"}, {\"symbol\": \"TSLA\"}]}"
#             }
#           }
#         ],
#         "role": "model"
#       },
#       "finish_reason": "stop",
#       "index": 0
#     }
#   ],
#   "prompt_feedback": {
#     "safety_ratings": [...]
#   }
# }
