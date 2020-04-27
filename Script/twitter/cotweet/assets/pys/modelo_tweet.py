#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 22:34:57 2020

@author: davidsaw
"""

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
from joblib import dump, load
import pickle




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


def main(algoritmo,pais,modelo, balance):
    # modelo='emocion'
    # pais='MIX'
    # balance=1
    # algoritmo='NB'
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
    df = df[pd.notnull(df[modelo])]
    df[modelo] = df[modelo].astype('int')
    df['tweet']=df['tweet'].apply(lambda x: quitar_cuentas(x))
    
    
    
    
    
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
        
    
    if modelo == 'emocion': 
        dump(clf, cwd + '/assets/pys/modelo_sentimientos_'+ pais.lower() +'.joblib') 
        pickle.dump(count_vect.vocabulary_,open( cwd + "/assets/pys/vocabulario_sentimientos_"+ pais.lower()+".pkl","wb"))
    elif modelo == 'tendencia':
        dump(clf, cwd + '/assets/pys/modelo_tendencia_'+ pais.lower() +'.joblib') 
        pickle.dump(count_vect.vocabulary_,open( cwd + "/assets/pys/vocabulario_tendencia_"+ pais.lower()+".pkl","wb"))
    elif modelo == 'coherencia':
        dump(clf, cwd + '/assets/pys/modelo_coherencia_'+ pais.lower() +'.joblib') 
        pickle.dump(count_vect.vocabulary_,open( cwd + "/assets/pys/vocabulario_coherencia_"+ pais.lower()+".pkl","wb"))
    



