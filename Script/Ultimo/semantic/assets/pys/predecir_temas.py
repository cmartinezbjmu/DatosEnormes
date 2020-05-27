#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:17:22 2020

@author: davidsaw
"""


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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from imblearn.datasets import make_imbalance
import sys
import os
from joblib import dump, load
import pickle
import json

#stopword list to use
spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend(spanish_stopwords)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))


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



hastags_list = []
for sublist in df['hastags'].to_list():
    for item in sublist:
        hastags_list.append(item)

temas=[]
for i in range(len(hastags_list)):
    palabras = re.findall('[A-Z][^A-Z]*', hastags_list[i])
    palabras = [c.lower() for c in palabras if c.lower() not in non_words]
    temas.extend(palabras)

temas = [k for k, v in Counter(temas).items() if v > 1]
temas = [tema for tema in temas if len(tema)>4]        

df['temas']=df['hastags'].apply(lambda x: ' '.join(re.findall('[A-Z][^A-Z]*', ' , '.join(x))).lower())



for i in df.index:
    for palabras in df.at[i,'temas'].split():
        for tema in temas:
            if tema in palabras:
                df.at[i,'temas']=palabras
                
                
## Función de correr el modelo
def correr_modelo(val, X_train_tfidf, y_train):
    if val=='NB':
        clf = MultinomialNB().fit(X_train_tfidf, y_train)
    elif val=='RF':
        clf = RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0).fit(X_train_tfidf, y_train)
    elif val=='LR':
        clf = LogisticRegression(random_state=0).fit(X_train_tfidf, y_train)
    elif val=='SV':
        clf = LinearSVC()().fit(X_train_tfidf, y_train)
    return clf


                

def main(algoritmo,df,modelo, balance):
    modelo='temas'
    balance=1
    algoritmo='NB'
    
    ## Definir las columnas de interés
    col = ['tweet', modelo]
    df = df[col]
    df = df[df[modelo]!='']
    df.columns=['tweet', modelo]
    df = df[pd.notnull(df[modelo])]
    df = df[pd.notnull(df[modelo])]
    df['categoria']=df[modelo].astype('category')
    df[modelo]=df['categoria'].cat.codes
    df[modelo] = df[modelo].astype('int')
    dftemas=df[['categoria',modelo]]
    temas=dftemas.set_index(modelo).to_dict()
    
    #Balancear respuesta
    muestra=df[modelo].value_counts().min()
    X,y=make_imbalance(df,df[modelo],
                   sampling_strategy=
                       [{i:muestra for i in list(df[modelo].value_counts().index)}][0],
                   random_state=0)
    
    ## Train y test para el modelo
    if balance==1:
        X_train, X_test, y_train, y_test = train_test_split(X['tweet'], X[modelo], random_state = 0)
    else:
        X_train, X_test, y_train, y_test = train_test_split(df['tweet'], df[modelo], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    
    clf=correr_modelo(algoritmo, X_train_tfidf, y_train)
    cwd = os.getcwd()
        
    
    dump(clf, cwd + '/assets/pys/modelo_temas.joblib') 
    pickle.dump(count_vect.vocabulary_,open( cwd + "/assets/pys/vocabulario_temas.pkl","wb"))
    with open(cwd + '/assets/pys/temas.json', 'w') as fp:
        json.dump(temas, fp)




                
                
