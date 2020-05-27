# Requires pymongo 3.6.0+
from pymongo import MongoClient
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation
from nltk.corpus import wordnet as wn
from sematch.semantic.similarity import WordNetSimilarity
from collections import Counter
# wns = WordNetSimilarity()
# nltk.download('wordnet')


#stopword list to use
spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend(spanish_stopwords)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

def tokenize(texto):
    texto = re.sub(r"http\S+", " ", texto)
    texto = re.sub(r'(.)\1+', r'\1\1', texto)
    tokens =  word_tokenize(texto)
    tokens = [c for c in tokens if c not in non_words]
    return tokens

def similitud(frase_1,frase_2):
    promedio=[]
    mejor=0
    for f1 in frase_1:
        for f2 in frase_2:
            if len(wn.synsets(f1,lang='spa'))==0 or len(wn.synsets(f2,lang='spa'))==0:
                s=0
            else:
                palabrafrase1 = wn.synsets(f1,lang='spa')[0]
                palabrafrase2 = wn.synsets(f2,lang='spa')[0]
                s = palabrafrase1.wup_similarity(palabrafrase2)
                if s is None:
                    s=0
                promedio.append(s)
                mejor= sum(promedio)/len(promedio)
    return mejor

def get_base():
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    collection = database["COL_tweets"]
    
    query = {}
    projection = {}
    projection["created_at"] = 1.0
    projection["user"] = 1.0
    projection["full_text"] = 1.0
    projection["hashtags"] = 1.0
    projection["id"] = 1.0
    
    cursor = collection.find(query, projection = projection)
    data = []
    hashtag = []
    try:
        for doc in cursor:
            for i in range(len(doc['hashtags'])):
                hashtag.append(doc['hashtags'][i]['text'])
            data.append([doc['id'], doc['created_at'], doc['user']['screen_name'], doc['full_text'], hashtag])
            hashtag = []
    finally:
        client.close()
    
    df = pd.DataFrame(data,columns=['id', 'created_at', 'screen_name', 'tweet', 'hastags'])
    df = df.drop_duplicates(['id'], keep='last')
    return df


def matriz_correlacion(df):
    dfnetwork=pd.DataFrame()
    for i in df.index: 
        for j in df.index:    
            dfnetwork.at[i,j]=similitud(tokenize(df.at[i,'tweet']),tokenize(df.at[j,'tweet']))
            # print(similitud(tokenize(df.at[i,'tweet']),tokenize(df.at[j,'tweet'])))
    return dfnetwork


def obtener_matriz_persona(persona):
    # dffiltro=df[df['screen_name']==persona]
    dffiltro=df[1:10]
    return matriz_correlacion(dffiltro)

def pares_correlacion(df,val):
    network=[]
    texto=dict()
    simil=0.0
    for i in df.index: 
        for j in df.index: 
            simil = similitud(tokenize(df.at[i,'tweet']),tokenize(df.at[j,'tweet']))
            if simil > val and i != j:
                element = tuple((i,j))
                network.append(element)
                texto.update( {i : df.at[i,'tweet']} )
    return network,texto


def obtener_pares_persona(persona,val):
    # dffiltro=df[df['screen_name']==persona]
    dffiltro=df[1:10]
    return pares_correlacion(dffiltro,val)

