#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 01:29:54 2020

@author: davidsaw
"""

from pymongo import MongoClient, errors
import pandas as pd
#from io import StringIO
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

def quitar_cuentas(a):
    texto=" ".join(filter(lambda x:x[0]!='@', a.split()))
    return texto


def main(pais,modelo):
    #Conexión con las bd de mongo
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    if pais=='MIX':
        collection_col = database["COL_dataset"]
        collection_arg = database["ARG_dataset"]
        ## Pasar de mongo a pandas
        data_col = pd.DataFrame(list(collection_col.find()))
        data_arg = pd.DataFrame(list(collection_arg.find()))
        data=pd.concat([data_col,data_col])
    else:
        collection = database[pais + "_dataset"]
        data = pd.DataFrame(list(collection.find()))
    
    
    ## Definir las columnas de interés
    col = ['reply_or_quote', modelo]
    df = data[col]
    df = df[df[modelo]!='']
    df.columns=['tweet', modelo]
    df = df[pd.notnull(df[modelo])]
    df = df[pd.notnull(df['tweet'])]
    df[modelo] = df[modelo].astype('int')
    df['tweet']=df['tweet'].apply(lambda x: quitar_cuentas(x))

    ## Extraer factores binarios para modelo
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2))
    features = tfidf.fit_transform(df.tweet).toarray()
    labels = df.emocion
    features.shape

   
    ## Comparación de modelos
    models = [
        RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
        LinearSVC(),
        MultinomialNB(),
        LogisticRegression(random_state=0),
    ]
    
    CV = 5
    cv_df = pd.DataFrame(index=range(CV * len(models)))
    entries = []
    for model in models:
      model_name = model.__class__.__name__
      accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
      for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    return cv_df










