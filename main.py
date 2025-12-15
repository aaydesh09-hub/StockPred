import praw
import csv
import pandas as pd
reddit = praw.Reddit(client_id='oL_jGfUjbdA-dzu-VzGaqg',
                     client_secret='cJWU0Phpaj-Pwp8fzE1EbutqU9X2pg',
                     user_agent='reddit_scrapper/0.1')
keyword = input('Enter keyword: ')
with open('subreddit_data.csv', 'w', newline='', encoding ='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'upvotes', 'url', 'body'])
    for post in reddit.subreddit('all').search(keyword, limit = 50, sort = 'relevance'):
        writer.writerow([post.title, post.score, post.url, post.selftext])
        print(post.title)

def pubOpinion(symbol):
    reddit = praw.Reddit(client_id='oL_jGfUjbdA-dzu-VzGaqg',
                         client_secret='cJWU0Phpaj-Pwp8fzE1EbutqU9X2pg',
                         user_agent='reddit_scrapper/0.1')
    with open('subreddit_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['title', 'upvotes', 'url', 'body'])
        for post in reddit.subreddit('all').search(symbol, limit=50, sort='relevance'):
            writer.writerow([post.title, post.score, post.url, post.selftext])
            print(post.title)
