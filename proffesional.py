import finnhub
import pandas as pd

finnhub = finnhub.Client("d44ivg1r01qr9l8183v0d44ivg1r01qr9l8183vg")
symbol = 'AAPL'
# quote = finnhub.quote(symbol)
# print(quote)
# news = finnhub.general_news(symbol,"all")
# print(news)
# recs = finnhub.recommendation_trends(symbol)
# print(recs)
# profile = finnhub.company_profile2(symbol = symbol)
# print(profile)
insider = finnhub.stock_insider_transactions(symbol)
print(insider)
