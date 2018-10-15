from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re, string
import nltk
import pandas as pd
import geograpy as geo

"""
This part of the program takes our dataframe df containing
tweet data and extracts useful tokens, or meaningful keywords which
we will be analysing and trying to make sense of
"""

df = pd.read_csv("tweet_data.csv", sep=";",error_bad_lines=False)
#print(df["text"])
tweets_text = df["text"].tolist()
stopwords = stopwords.words('english') # stopwords are useless words like 'the', 'is' and all
english_vocab = set(word.lower() for word in nltk.corpus.words.words())

def process_tweets_texts(tweet):
    if tweet.startswith('@null'):
        return "[Tweet is unavailable]"
    # Just some regular expressions that strips out more noise
    tweet = re.sub(r'\$\w*','',tweet) # Remove tickers
    tweet = re.sub(r'https?:\/\/.*\/\w*','',tweet) # Remove hyperlinks
    tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # Remove punctuations
    twtok = TweetTokenizer(strip_handles=True, reduce_len=True)
    tokens = twtok.tokenize(tweet)
    tokens = [i.lower() for i in tokens if i not in stopwords and len(i) > 2 and 
                                                                i in english_vocab]
    return tokens

words = []
places = []

for tw in tweets_text[:10]:
    words += process_tweets_texts(tw)
    places.append(geo.get_place_context(text=tw))

print(tweets_text[0])
for p in range(len(places)):
    print(places[p].regions)
