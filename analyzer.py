# import pandas as pd
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#
# analyzer = SentimentIntensityAnalyzer()
# df = pd.read_csv('subreddit_data.csv')
# sentimentScore = []
# sentimentLabel = []
#
# def getSentiment(text):
#   if not isinstance(text, str):
#     return 0
#   return analyzer.polarity_scores(text)["compound"]
#
# def labelSentiment(score):
#   if score >= 0.05:
#     return "positive"
#   elif score <= -0.05:
#     return "negative"
#   else:
#     return "neutral"
#
# for text in df["body"]:
#     if getSentiment(text) != 0:
#         sentimentScore.append(getSentiment(text))
#         sentimentLabel.append(labelSentiment(getSentiment(text)))
#
#
# avgSentiment = sum(sentimentScore) / len(sentimentScore)
# print(sentimentLabel)
# df['sentimentScore'] = pd.DataFrame(sentimentScore)
# df['sentimentLabel'] = pd.DataFrame(sentimentLabel)
# df['average'] = avgSentiment
# print('success')
# df.to_csv('subreddit_data.csv', index = True)

import os
import csv
from typing import Tuple, List
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# Determine CSV location relative to this file:
# If analyzer.py is at Application/Tools_Logic/analyzer.py
# then CSV will be Application/subreddit_data.csv
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_NAME = "subreddit_data.csv"
CSV_PATH = os.path.join(BASE_DIR, CSV_NAME)
def ensure_csv_exists():
    """Create CSV with header if it doesn't exist yet."""
    if not os.path.exists(CSV_PATH):
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "upvotes", "url", "body"])
def load_subreddit_df() -> pd.DataFrame:
    """
    Safely load subreddit CSV. Returns an empty DataFrame with expected columns
    if the file doesn't exist or can't be read.
    """
    ensure_csv_exists()
    try:
        df = pd.read_csv(CSV_PATH)
        # Ensure expected columns exist
        for col in ["title", "upvotes", "url", "body"]:
            if col not in df.columns:
                df[col] = ""
        return df
    except Exception as e:
        print(f"Warning: failed to read {CSV_PATH}: {e}")
        return pd.DataFrame(columns=["title", "upvotes", "url", "body"])
def getSentiment(text) -> float:
    """Return compound sentiment score (float). Non-strings -> 0."""
    if not isinstance(text, str):
        return 0.0
    try:
        return float(analyzer.polarity_scores(text)["compound"])
    except Exception:
        return 0.0
def labelSentiment(score: float) -> str:
    """Label sentiment score into positive/negative/neutral."""
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"
def analyze_dataframe(df: pd.DataFrame) -> Tuple[float, List[float], List[str]]:
    """
    Given a DataFrame with a 'body' column, compute sentiment scores and labels.
    Returns (avg_score, list_of_scores, list_of_labels).
    """
    scores = []
    labels = []
    if "body" not in df.columns:
        return 0.0, scores, labels
    for text in df["body"].fillna("").astype(str):
        s = getSentiment(text)
        if s != 0.0:
            scores.append(s)
            labels.append(labelSentiment(s))
    if len(scores) == 0:
        avg = 0.0
    else:
        avg = sum(scores) / len(scores)
    return avg, scores, labels
def write_dataframe(df: pd.DataFrame):
    """Overwrite the subreddit CSV with the provided dataframe (safe)."""
    ensure_csv_exists()
    try:
        df.to_csv(CSV_PATH, index=False)
    except Exception as e:
        print(f"Warning: failed to write {CSV_PATH}: {e}")
# Optional: keep a small test interface when run directly
if __name__ == "__main__":
    print("Running analyzer.py self-test...")
    df = load_subreddit_df()
    avg, scores, labels = analyze_dataframe(df)
    print(f"rows: {len(df)}  scored: {len(scores)}  avg_sentiment: {avg}")
    # If you want, add test writing:
    # df['sentimentScore'] = pd.Series(scores + [""] * (len(df)-len(scores)))
    # df['sentimentLabel'] = pd.Series(labels + [""] * (len(df)-len(labels)))
    # write_dataframe(df)