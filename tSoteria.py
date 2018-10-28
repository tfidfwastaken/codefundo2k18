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
import numpy as np
from math import *
import warnings
warnings.filterwarnings('ignore')

"""
This part of the program takes our dataframe df containing
 tweet data and extracts useful tokens, or meaningful keywords which
 we will be analysing and trying to make sense of
"""
df = pd.read_csv("tweet_data.csv", sep=";",error_bad_lines=False, warn_bad_lines=False)

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
for tw in tweets_text[:500]:
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

words_vis = ' '.join(words)

wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(city_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()


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
            'key': '\'tis secret',
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
#print(max_count)
m_size=[]
for count in count_list:
    m_size.append(count/max_count*50)
    
for i, j in zip(d, range(len(count_list))):
    xpt,ypt=m(d[i][2],d[i][1])
    plt.plot(xpt, ypt, 'bo', markersize=m_size[j])
    plt.text(xpt, ypt, i, fontsize=12)    


plt.show()

li = ['SMR Vinay City','English and Foreign Languages University, Hyderabad','Banjara Hills, Hyderabad','Tata Institute of Social Science, SR Sankaran Block, Hyderabad','Central University of Hyderabad','Ganga Vertica, Neeladri main Road, Electronic City','Avohi, Venus Building, Kalyana Mandapa Road, Jakkasandra Ext, Koramangala','Confederation of Indian Industry, CII, 12 Main, HAL 2nd Stage, Indiranagar','Keli Cultural Association, Pruksa Silvana, Nimbekaipura Road, Budigere Cross, Old Madras Road, Bangalore','20, Basapura Road, HOSA Road Jn, Basapura, Bengaluru, Karnataka 560100','KRC Road Doddagubbi Main Road, Post, Kothanur, Bengaluru, Karnataka 560077','Indian Social Institute, 24 Benson Road, Benson Town, Bengaluru','SCM-India, 29, 2nd Cross, CSI compound, Mission Road, Bengaluru','Lions Club, No 9 Hanumanthappa Road, Sonangi Layout, Kammanahalli Main Road, Bengaluru-33','Elamkulam Road, Kadavanthra P.O., Ernakulam District, Kochi, Kerala 682020','Kaloor, Ernakulam, Kerala 682017','Idukki District, Kuyilimala, Kerala 685603','Collectrotae Wayanad, North Kalpetta P.O. Wayanad','Keltron House, Vellayambalam, Thiruvananthapuram, Kerala 695033','Mahathma Gandhi Rd, Overbridge, Santhi Nagar, Thampanoor, Thiruvananthapuram, Kerala 695001','Near Tagore Theatre, Vazhuthacaud, Thiruvananthapuram, Kerala 695010','YMCA Rd, Statue, Palayam, Thiruvananthapuram, Kerala 695001','Cotton Hill Road, Opp. Carmel Monastery, Cotton Hill, Vazhuthacaud, Thiruvananthapuram, Kerala 695010','CV Raman Pillai Rd, Vazhuthacaud, Thycaud P.O, Thiruvananthapuram, Kerala 695014','Salem - Kochi - Kanyakumari Hwy, Karyavattom, Thiruvananthapuram, Kerala 695581','SH 1, Nalanchira, Parottukonam, Thiruvananthapuram, Kerala 695015','Rosscote Bungalow, Rosscote Lane, Opp Trivandrum club, Vazhuthacaud, Thiruvananthapuram, Kerala 695010','Kerala State Branch Opp. General Hospital, Red Cross Road, Vanchiyoor, Thiruvananthapuram, Kerala 695035','Kunjulekshmi Towers, Kattakkada, Kerala','Pattom, Thiruvananthapuram, Kerala 695004','Technopark Campus, Kazhakkoottam, Kerala 695001','Thellakom, Kerala','St Marys College Rd, Chembukkav, Thrissur, Kerala 680020']


d={}
lats = []
lons = []
for i in li:
    parameters = {
            'key': '340cf83a6d6dfc',
            'q': i,
            'format': 'json'
            }
    response = requests.get(url,params=parameters)
    lat=float(json.loads(response.text)[0]['lat'])
    lon=float(json.loads(response.text)[0]['lon'])
    d[i]=[lat,lon]
    lats.append(lat)
    lons.append(lon)


lats2 = np.array(lats)
lons2 = np.array(lons)
#place = input('Please enter where you are: ')

for place in city_distinct:
    parameters = {
                'key': '340cf83a6d6dfc',
                'q': place,
                'format': 'json'
                }
    response = requests.get(url,params=parameters)
    lat1 = float(json.loads(response.text)[0]['lat']) #parsing json to obtain latitude and longitude of the place the user is at.
    lon1 = float(json.loads(response.text)[0]['lon'])
#print(lat1, lon1)

    dlat = np.array([radians(x-lat1) for x in lats])
    dlon = np.array([radians(x-lon1) for x in lons])

    a = np.array(np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lats2) * np.sin(dlon/2)**2)  #Haversine Formula
    c = 2 * np.arcsin(np.sqrt(np.abs(a)))
    r = 6371 #radius of Earth in kilometres.
    distances = list(r*c)

    index = distances.index(min(distances))
    print('Nearest Relief centre to', place,' is: ',li[index])
