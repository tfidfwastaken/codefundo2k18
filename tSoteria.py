import matplotlib
matplotlib.use('TkAgg')
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re, string
import nltk
import pandas as pd
import geograpy as geo
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')
import requests
import json
from mpl_toolkits.basemap import Basemap

"""
This part of the program takes our dataframe df containing
 tweet data and extracts useful tokens, or meaningful keywords which
 we will be analysing and trying to make sense of
"""
df = pd.read_csv("tweet_data.csv", sep=";",error_bad_lines=False)

tweets_text = df["text"].tolist()
stopwords = stopwords.words('english') # stopwords are useless words like 'the', 'is' and all
english_vocab = set(word.lower() for word in nltk.corpus.words.words())

kerala = pd.read_csv('kerala.csv')
cities = list(kerala['Places'])


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
#for tw in tweets_text:
for tw in tweets_text[:1000]:
        words += process_tweets_texts(tw)
        places.append(geo.get_place_context(text=tw))
city = []
for p in range(len(places)):
    pl = places[p].cities
    for i in pl:
        if i in cities:
            city.append(i)

city_words = ' '.join(city)
city_lower = [i.lower() for i in city]

#Visualising data with wordcloud

#words_vis = ' '.join(words)

#wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(city_words)

#plt.figure(figsize=(10, 7))
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis('off')
#   plt.show()


m = Basemap(projection='mill',
            llcrnrlat = 7.285508,
            llcrnrlon = 72.065156,
            urcrnrlat = 15.449267,
            urcrnrlon = 78.424284,
            resolution='h')
city_distinct = list(set(city))
l=[]
d={}
url = "https://us1.locationiq.com/v1/search.php"
for i in city_distinct:
    parameters = {
            'key': '***REMOVED***',
            'q': i,
            'format': 'json'
            }
    response = requests.get(url,params=parameters)
    lat=float(json.loads(response.text)[0]['lat'])
    lon=float(json.loads(response.text)[0]['lon'])
    d[i]=[city.count(i),lat,lon]

m.drawcoastlines()
m.drawstates(color='b')
m.drawcounties(color='darkred')
'''
for i in d:
    if d[i][0]>5:
        d[i].append(300)
    elif d[i][0] in range(3,5):
        d[i].append(150)
    elif d[i][0] in range(2,3):
        d[i].append(80)
    elif d[i][0] in range(1,2):
        d[i].append(20)
    else:
        d[i].append(3)
        '''
count_list = [i[0] for i in list(d.values())]
max_count=max(count_list)
print(max_count)
m_size=[]
for count in count_list:
    m_size.append(count/max_count*50)
    
for i, j in zip(d, range(len(count_list))):
    xpt,ypt=m(d[i][2],d[i][1])
    plt.plot(xpt, ypt, 'bo', markersize=m_size[j])
    plt.text(xpt, ypt, i, fontsize=12)    


plt.show()
