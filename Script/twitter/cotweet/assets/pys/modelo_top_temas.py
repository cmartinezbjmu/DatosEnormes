from pymongo import MongoClient
from bson.code import Code
import pandas as pd

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import plotly.express as px

def query(pais):
    if pais != 'CA':
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection = database[pais + "_dataset"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection:
                    break
        query = {}
        projection = {}
        projection["reply_or_quote"] = 1.0

        data = []
        cursor = collection.find(query, projection = projection)
        try:
            for doc in cursor:
                data.append([doc['_id'], doc['reply_or_quote']])
        finally:
            client.close()
        df = pd.DataFrame(data,columns=['_id', 'text'])
        return df
    else:
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection_col = database["COL_dataset"]
                collection_arg = database["ARG_dataset"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection_col and collection_arg:
                    break
        query = {}
        projection = {}
        projection["reply_or_quote"] = 1.0

        data = []
        cursor_col = collection_col.find(query, projection = projection)
        cursor_arg = collection_arg.find(query, projection = projection)
        try:
            for doc in cursor_col:
                data.append([doc['_id'], doc['reply_or_quote']])
            for doc in cursor_arg:
                data.append([doc['_id'], doc['reply_or_quote']])    
        finally:
            client.close()
        df = pd.DataFrame(data,columns=['_id', 'text'])
        return df


def remove_links(tweet):
    '''Takes a string and removes web links from it'''
    tweet = re.sub(r'http\S+', '', tweet) # remove http links
    tweet = re.sub(r'bit.ly/\S+', '', tweet) # rempve bitly links
    tweet = tweet.strip('[link]') # remove [links]
    return tweet

def remove_users(tweet):
    '''Takes a string and removes retweet and @user information'''
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove retweet
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove tweeted at
    return tweet

# cleaning master function
def clean_tweet(tweet, bigrams=False):
    my_stopwords = nltk.corpus.stopwords.words('spanish')
    stopwords = ['d', 'x', 'pa', 'q', 'si', 'usted', 'tan', 'solo', 'ser', 'bien', 'así', 'mas', 'va', 'van', 'señor', 'hace', 'hacer', 
                'siempre', 'gracias', 'favor', 'puede', 'dio', 'como', 'aquí', 'ahí']
    my_stopwords.extend(stopwords)
    word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
    my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'

    tweet = remove_users(tweet)
    tweet = remove_links(tweet)
    tweet = tweet.lower() # lower case
    tweet = re.sub('['+my_punctuation + ']+', ' ', tweet) # strip punctuation
    tweet = re.sub('\s+', ' ', tweet) #remove double spacing
    tweet = re.sub('([0-9]+)', '', tweet) # remove numbers
    tweet_token_list = [word for word in tweet.split(' ')
                            if word not in my_stopwords] # remove stopwords

    tweet_token_list = [word_rooter(word) if '#' not in word else word
                        for word in tweet_token_list] # apply word rooter
    if bigrams:
        tweet_token_list = tweet_token_list+[tweet_token_list[i]+'_'+tweet_token_list[i+1]
                                            for i in range(len(tweet_token_list)-1)]
    tweet = ' '.join(tweet_token_list)
    return tweet

def display_topics(model, feature_names, no_top_words):
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["Topic %d words" % (topic_idx)]= ['{}'.format(feature_names[i])
                        for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict["Topic %d weights" % (topic_idx)]= ['{:.1f}'.format(topic[i])
                        for i in topic.argsort()[:-no_top_words - 1:-1]]
    return pd.DataFrame(topic_dict)

def top_temas_funcion(pais):
    df = query(pais)
    df['clean_tweet'] = df.text.apply(clean_tweet)

    from sklearn.feature_extraction.text import CountVectorizer

    # the vectorizer object will be used to transform text to vector form
    vectorizer = CountVectorizer(max_df=0.9, min_df=25, token_pattern='\w+|\$[\d\.]+|\S+')

    # apply transformation
    tf = vectorizer.fit_transform(df['clean_tweet']).toarray()

    # tf_feature_names tells us what word each column in the matric represents
    tf_feature_names = vectorizer.get_feature_names()


    from sklearn.decomposition import LatentDirichletAllocation

    number_of_topics = 10

    model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)
    model.fit(tf)

    no_top_words = 10
    df_topics = display_topics(model, tf_feature_names, no_top_words)
    nuevo_df = pd.DataFrame()

    valores = []
    pesos = []
    temas = []
    for i in range(no_top_words):
        valores+= (df_topics['Topic {} words'.format(str(i))].values.tolist()) 
        pesos+= (df_topics['Topic {} weights'.format(str(i))].values.tolist()) 
        for j in range(len(df_topics['Topic {} weights'.format(str(i))].values.tolist())):
            temas.append('tema{}'.format(str(i)))
        i+=i

    nuevo_df['valores'] = valores
    nuevo_df['pesos'] = pesos
    nuevo_df['temas'] = temas
    fig = px.treemap(nuevo_df, path=['temas', 'valores'], values='pesos')
    return fig