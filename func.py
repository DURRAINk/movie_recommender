import pandas as pd
import numpy as np 
import random
import requests
import warnings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

key=os.getenv('TMDB_API_KEY')
warnings.filterwarnings('ignore')

lang=["English", "Spanish", "Norwegian", "Japanese", "Korean", "Russian", "Cantonese", "Ukrainian", "Italian", "German", "French", "Finnish", "Catalan", "Valencian", "Icelandic", "Indonesian", "Dutch", "Flemish", "Portuguese", "Telugu", "Polish", "Danish", "Turkish", "Chinese", "Thai", "Romanian", "Tagalog", "Macedonian", "Swedish", "Tamil", "Vietnamese", "Hindi", "Arabic", "Serbian", "NoLanguage", "Galician", "Greek", "Hungarian", "Malayalam", "Marathi", "Oriya", "Bengali", "Persian", "Bokmål", "Norwegian", "NorwegianBokmål", "Latvian", "Basque", "Malay", "CentralKhmer", "Irish", "Czech", "Gujarati", "Kannada", "Serbo-Croatian", "Latin", "Dzongkha", "Slovak"]

year=[2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000, 1999, 1998, 1997, 1996, 1995, 1994, 1993, 1992, 1991, 1990, 1989, 1988, 1987, 1986, 1985, 1984, 1983, 1982, 1981, 1980, 1979, 1978, 1977, 1976, 1975, 1974, 1973, 1972, 1971, 1970, 1969, 1968, 1967, 1966, 1965, 1964, 1963, 1962, 1961, 1960, 1959, 1958, 1957, 1956, 1955, 1954, 1953, 1952, 1951, 1950, 1949, 1948, 1947, 1946, 1945, 1944, 1943, 1942, 1941, 1940, 1939, 1938, 1937, 1936, 1935, 1934, 1933, 1932, 1931, 1930, 1929, 1928, 1927, 1926, 1925, 1924, 1923, 1920, 1919, 1918, 1917, 1916, 1915, 1907, 1903]

df=pd.read_csv('tmdb_movies.csv')
df['genre']=df['genre'].astype('U')
df['Cast']=df['Cast'].apply(lambda x: x.replace('[','').replace(']','').replace("'",'').split(', '))
title=df['Title']

def recommend1(df,genre,lang=None):

    cd=CountVectorizer()
    mov1=[]
    mov2=[]
    if lang:
        new_data=df[df['Language']==lang.strip()].reset_index(drop=True)
        sparse_met=cd.fit_transform(new_data['genre'])
    else:
        sparse_met=cd.fit_transform(df['genre'])
    sparse_genre=cd.transform([genre])
    cos_sim=cosine_similarity(sparse_met,sparse_genre)
    similarity=sorted(list(enumerate(cos_sim)),reverse=True,key=lambda x:x[1])
    for i, j in similarity:
        if j[0]>0.85:
            mov1.append(i)
    if len(mov1)<5:
        for i, j in similarity:
            if j[0]>0.7:
                mov2.append(i)
        if lang:
            return new_data.iloc[mov2,:]
        else:
            return df.iloc[mov2,:]
        
    else:
        if lang:
            return new_data.iloc[mov1,:]
        else:
            return df.iloc[mov1,:]

def recommend2(title,df):
    req=requests.get(f'https://omdbapi.com/?t={title}&apikey={key}')
    dic=req.json()
    genre=dic.get('Genre')
    lang=dic.get('Language')
    lang=lang.split(',')[0]
    print(lang)
    countv=CountVectorizer()
    mov1=[]
    mov2=[]
    if lang:
        new_data=df[df['Language']==lang].reset_index(drop=True)
        sparse_met=countv.fit_transform(new_data['genre'])
        
    else:
        sparse_met=countv.fit_transform(df['genre'])
    sparse_genre=countv.transform([genre])
    cos_sim=cosine_similarity(sparse_met,sparse_genre)
    similarity=sorted(list(enumerate(cos_sim)),reverse=True,key=lambda x:x[1])
    for i, j in similarity:
        if j[0]>0.85:
            mov1.append(i)
    if len(mov1)<5:
        for i, j in similarity:
            if j[0]>0.7:
                mov2.append(i)
        if lang:
            return new_data.iloc[mov2,:]
        else:
            return df.iloc[mov2,:]
        
    else:
        if lang:
            return new_data.iloc[mov1,:]
        else:
            return df.iloc[mov1,:]

def posters(df):
    lst_title=[]
    lst_src=[]
    a=df[df['release_year']==2024]
    b= df[df['release_year']==2023]
    pos_df=pd.concat((a,b),ignore_index=True)['Title']
    rand=random.sample(range(145),5)
    for i in rand:
        lst_title.append(pos_df[i])
    for i in lst_title:
        req=requests.get(f'https://omdbapi.com/?t={i}&apikey={key}')
        pos=req.json()
        lst_src.append(pos.get('Poster'))
    return lst_src

def cast_items(df):
    lst=[]
    for i in df['Cast']:
        lst=lst+i
    return set(lst)

cast=list(cast_items(df))
def cast_search(x):
    count=CountVectorizer()
    met=count.fit_transform(cast)
    pred=count.transform([x])
    sim=cosine_similarity(met,pred)
    var=sorted(list(enumerate(sim)),reverse=True,key=lambda x:x[1])[0]
    return cast[var[0]]

def recommender3(artist):
    artist_list=[artist]
    data1=df[df['Cast'].apply(lambda x: set(artist_list).issubset(x))]
    return data1