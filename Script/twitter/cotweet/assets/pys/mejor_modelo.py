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

#Conexión con las bd de mongo
client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
database = client["Grupo03"]
collection = database["COL_tweets"]
collection_dataset = database["COL_dataset"]

## Pasar de mongo a pandas
data = pd.DataFrame(list(collection_dataset.find()))

## Definir las columnas de interés
col = ['reply_or_quote', 'emocion']
df = data[col]
df = df[df['emocion']!='']
df.columns=['tweet', 'emocion']
df = df[pd.notnull(df['emocion'])]
df = df[pd.notnull(df['tweet'])]
df['emocion'] = df['emocion'].astype('int')
df['tweet']=df['tweet'].apply(lambda x: quitar_cuentas(x))




###Código de prueba
from joblib import dump, load
clf = load('/home/davidsaw/uniandes-bigdata/DatosEnormes/Script/twitter/cotweet/assets/pys/modelo_sentimientos.joblib') 
X_train=pd.read_csv('/home/davidsaw/uniandes-bigdata/DatosEnormes/Script/twitter/cotweet/assets/pys/sentimientos_train.csv')

count_vect = CountVectorizer(ngram_range=(1,1), min_df=1)
count_vect._validate_vocabulary()
count_vect.fit_transform(X_train)


count_vect.transform([df.at[5,'tweet']])

for i in df.index:
    print(i)
    print(clf.predict(count_vect.transform([df.at[i,'tweet']])))
########################################################################

## Extraer factores binarios para modelo
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2))
features = tfidf.fit_transform(df.tweet).toarray()
labels = df.emocion
features.shape


## Crear histograma de emociones
fig = plt.figure(figsize=(8,6))
df.groupby('Product').Consumer_complaint_narrative.count().plot.bar(ylim=0)
plt.show()





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
import seaborn as sns
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
              size=8, jitter=True, edgecolor="gray", linewidth=2)
plt.show()








