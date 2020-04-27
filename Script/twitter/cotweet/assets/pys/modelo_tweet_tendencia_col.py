#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:52:12 2020

@author: davidsaw
"""

from pymongo import MongoClient, errors
import pandas as pd
#from io import StringIO
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

def quitar_cuentas(a):
    texto=" ".join(filter(lambda x:x[0]!='@', a.split()))
    return texto

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

def query():
    while True:
        try:
            client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
            client.server_info() # force connection on a request as the
        except errors.ServerSelectionTimeoutError as err:
            print(err)
        finally:
            if client.server_info():            
                break

    database = client["Grupo03"]
    collection = database["COL_dataset"]
    query = {}
    query["tendencia"] = {
        u"$ne": u""
    }
    query["$and"] = [
        {
            u"tendencia": {
                u"$exists": True
            }
        }
    ]

    cursor = collection.find(query)
    data = []

    try:
        for doc in cursor:
            data.append([doc['reply_or_quote'].lower(), doc['tendencia']])
    finally:
        client.close()
    df = pd.DataFrame(data,columns=['tweet', 'tendencia'])
    return df

def main(algoritmo)
    df = query()

    df['tendencia'] = df['tendencia'].astype('int')
    df['tweet']=df['tweet'].apply(lambda x: quitar_cuentas(x))

    ## Train y test para el modelo
    X_train, X_test, y_train, y_test = train_test_split(df['tweet'], df['tendencia'], random_state = 0)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf=correr_modelo(algoritmo, X_train_tfidf, y_train)
    cwd = os.getcwd()

    from joblib import dump, load
    dump(clf, cwd + '/assets/pys/modelo_tendencia_col.joblib') 

    import pickle
    pickle.dump(count_vect.vocabulary_,open( cwd + "/assets/pys/vocabgit 