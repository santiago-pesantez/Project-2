# Import required libraries
import os
import tweepy
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import csv
import warnings
warnings.filterwarnings("ignore")

# Global Parameters
stop_words = set(stopwords.words('english'))
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAAo3fQEAAAAA3VZitXKA19trQga7kgMTbQxExYQ%3Dv6z91zwHMULkx9WTUyfzt5fCREgU1sB7Jjm5njbh4eYjgMSwkm')

# Define reusable functions
def preprocess_tweet_text(tweet):
    tweet.lower()
    # Remove urls
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    tweet = re.sub(r'\@\w+|\#','', tweet)
    # Remove punctuations
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    # Remove stopwords
    tweet_tokens = word_tokenize(tweet)
    filtered_words = [w for w in tweet_tokens if not w in stop_words]
    
    #ps = PorterStemmer()
    #stemmed_words = [ps.stem(w) for w in filtered_words]
    #lemmatizer = WordNetLemmatizer()
    #lemma_words = [lemmatizer.lemmatize(w, pos='a') for w in stemmed_words]
    
    return " ".join(filtered_words)

def polarity_to_string(sentiment):
    if sentiment < 0:
        return "Negative"
    elif sentiment == 0:
        return "Neutral"
    else:
        return "Positive"
    
def get_pd_from_twitter(ticker, n):
    print('Requesting data, please wait...')
    # Get tweets that contain the ticker as a hashtag
    # -is:retweet means we don't want retweets
    # lang:en is asking for the tweets to be in english
    query = f'#{ticker} -is:retweet lang:en'
    tweets = tweepy.Paginator(client.search_recent_tweets, query=query, tweet_fields=['created_at'], max_results=100).flatten(limit=int(n))

    # Define DF structure
    tweets_df = pd.DataFrame(columns=['created_at', 'text', 'sentiment_polarity', 'sentiment_label'])

    for tweet in tweets:
        txt = preprocess_tweet_text(tweet.text)
        polarity = TextBlob(txt).sentiment.polarity
        row = {'created_at': tweet.created_at, 'text': txt, 'sentiment_polarity' : polarity, 'sentiment_label' : polarity_to_string(polarity)}
        tweets_df = tweets_df.append(row, ignore_index = True)
    
    return tweets_df
    
def main():
    # Read from input
    ticker = input("Please enter a crypto ticker: #")
    n = input("How many tweets do you want to retrieve?: ")

    tweets_df = get_pd_from_twitter(ticker, n)

    # Create a CSV file froim the tweets_df
    print('Creating a CSV file...')
    tweets_df.to_csv('twitter_data.csv', index=False)
    print('CSV file created.')