# from .analyzer import getSentiment, labelSentiment
#
# import finnhub
# import praw
# import csv
# from .marketaux import news
#
# import pandas as pd
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#
# analyzer = SentimentIntensityAnalyzer()
# df = pd.read_csv('subreddit_data.csv')
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# CSV_NAME = "subreddit_data.csv"
# CSV_PATH = os.path.join(BASE_DIR, CSV_NAME)
# sentimentScore = []
# sentimentLabel = []
#
# def pubOpinion(symbol):
#     reddit = praw.Reddit(client_id='oL_jGfUjbdA-dzu-VzGaqg',
#                          client_secret='cJWU0Phpaj-Pwp8fzE1EbutqU9X2pg',
#                          user_agent='reddit_scrapper/0.1')
#     with open('subreddit_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['title', 'upvotes', 'url', 'body'])
#         for post in reddit.subreddit('all').search(symbol, limit=50, sort='relevance'):
#             writer.writerow([post.title, post.score, post.url, post.selftext])
#
#     for text in df["body"]:
#         print(getSentiment(text))
#         if getSentiment(text) != 0:
#             sentimentScore.append(getSentiment(text))
#             sentimentLabel.append(labelSentiment(getSentiment(text)))
#
#
#     avgSentiment = sum(sentimentScore) / len(sentimentScore)
#     return avgSentiment, labelSentiment(avgSentiment)
#
#
#
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

import csv
import pandas as pd
import finnhub
import praw
from marketaux import news
# import analyzer helpers
from analyzer import getSentiment, labelSentiment
CSV_FILE = "subreddit_data.csv"   # must be in the same folder as app.py
# ---- HARDCODED KEYS YOU POSTED ----
FINNHUB_API_KEY = "d44ivg1r01qr9l8183v0d44ivg1r01qr9l8183vg"
REDDIT_CLIENT_ID = "oL_jGfUjbdA-dzu-VzGaqg"
REDDIT_CLIENT_SECRET = "cJWU0Phpaj-Pwp8fzE1EbutqU9X2pg"
REDDIT_USER_AGENT = "reddit_scrapper/0.1"
# Initialize API clients
finnhub_client = finnhub.Client(FINNHUB_API_KEY)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)
def pubOpinion(symbol):
    """
    Fetch Reddit posts and compute sentiment.
    """
    # --- STEP 1: FETCH POSTS + SAVE TO CSV (overwrite) ---
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "upvotes", "url", "body"])
        for post in reddit.subreddit("all").search(symbol, limit=50, sort="relevance"):
            writer.writerow([post.title, post.score, post.url, post.selftext or ""])
    # --- STEP 2: READ CSV BACK ---
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return 0.0, "neutral"
    sentiment_scores = []
    # --- STEP 3: SENTIMENT ANALYSIS ---
    for text in df["body"].fillna(""):
        score = getSentiment(text)
        if score != 0:
            sentiment_scores.append(score)
    if len(sentiment_scores) == 0:
        return 0.0, "neutral"
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    label = labelSentiment(avg_sentiment)
    return avg_sentiment, label
def get_financials(symbol):
    """
    Fetch full stock data pack + sentiment.
    """
    # Sentiment
    sentiment_score, sentiment_label = pubOpinion(symbol)
    # Finnhub data
    try:
        quote = finnhub_client.quote(symbol)
    except:
        quote = {}
    try:
        general_news = finnhub_client.general_news(symbol)
    except:
        general_news = []
    try:
        insider = finnhub_client.stock_insider_transactions(symbol)
    except:
        insider = []
    # Marketaux news
    try:
        articles = news(symbol)
    except:
        articles = []
    return {
        "symbol": symbol,
        "quote": quote,
        "news": general_news,
        "insider": insider,
        "sentiment": sentiment_score,
        "label": sentiment_label,
        "articles": articles,
    }