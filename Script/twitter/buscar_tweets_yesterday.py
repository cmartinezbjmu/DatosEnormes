#!/usr/bin/python3
import tweepy
import json
import datetime
from pymongo import MongoClient, errors

palabras_clave = ["Coronavirus", "covid19"]

consumer_key = "46m2jsm1TnP9vgRFYcTQzyR1R"
consumer_secret = "Vk6w3xf1D1PIdkpSPpmYxfoovUtqp65VVMAZSt8XF8kwpLASdt"
access_token = "1243367012572827648-EG9oAl55HEBzzYNUf7j7Jzbh0XoJFn"
access_token_secret = "qyuLP1V3iHENsOVMlmNX4eo5drVbEgzEVHGvgaYjSiQ7T"

# consumer_key = "FGqkOJU3o3Rh15alV5Ql4obUX"
# consumer_secret = "2vIiKctsxxezL6kKGo4qtyFPDcY1viFz6M1a2bHLTwWrijVXE5"
# access_token = "151179935-HLh8FmhbS0D3892npnkfiM6UNc1hLZ0NRHKhZCzJ"
# access_token_secret = "tiKTQPpveXHZRsEm0ODUeCJGmlSBqqeUzO7F7cRYKrTp6"

# consumer_key = "hwQLsT9LMp90MPSgYXf7Abvzw"
# consumer_secret = "wSYKwJPPvaAvPD2KL8dGrkm8kJORCIPss5qVLMuLMAZxWGUcb8"
# access_token = "52602353-a7v7fPQ90BvjVNBR1ZYg6ziiHCiyqfmzdcuS150em"
# access_token_secret = "roy6xRVWbYF2K2BNog9Fi04lArpuNLmY8OIMJWkChrEmW"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

cuentas = ['infopresidencia', 'SenadoGovCo', 'AABenedetti', 'minsaludcol', 'CristoBustos', 
'velascoluisf', 'GNavasTalero', 'DavidRacero', 'intiasprilla', 'Bogota', 'AlcaldiadeMed', 
'AlcaldiaDeCali', 'AlcaldiaCTG', 'SectorSalud', 'SaludAntioquia', 'secsaludvalle', 'GobAntioquia', 
'GobValle', 'AlcaldiaBGA', 'CundinamarcaGob', 'MinHacienda', 'colombiacompra', 'MintrabajoCol', 
'GobChoco', 'Goberamazonas', 'noticiascaracol', 'noticiasrcn', 'NoticiasUno', 'bluradioco', 'lafm', 
'eltiempo', 'elespectador', 'revistasemana', 'WRadioColombia', 'alvarouribevel', 'fdbedout']

cuentas_arg = ['alferdez', 'horaciorlarreta', 'msalnacion',
               'CFKArgentina', 'clarincom', 'LANACION', 'LongobardiM',
               'Gatosylvestre', 'JonatanViale', 'SergioMassa', 'proargentina',
               'mauriciomacri', 'FpVNacional', 'UBARectorado', 'mariuvidal',
               'C5N', 'Kicillofok', 'cuervotinelli', 'PatoBullrich', 'marioraulnegri']


def retrieve_replied_tweet(id_tweet):
    resultado = None
    try:
        tweet = api.get_status(id_tweet, tweet_mode='extended')
        resultado = json.dumps({'created_at': tweet._json['created_at'],
                            'id': tweet._json['id'],
                            'full_text': tweet._json['full_text'],
                            'hashtags': tweet._json['entities']['hashtags'],
                            'user_mentions': tweet._json['entities']['user_mentions'],
                            'urls': tweet._json['entities']['urls'],
                            'user': { 'id': tweet._json['user']['id'],
                                        'name': tweet._json['user']['name'],
                                        'screen_name': tweet._json['user']['screen_name'],
                                        'followers_count': tweet._json['user']['followers_count']},
                            'retweet_count': tweet._json['retweet_count'],
                            'favorite_count': tweet._json['favorite_count'],
                            'in_reply_to_status_id': tweet._json['in_reply_to_status_id'],
                            'is_quote_status': tweet._json['is_quote_status'],
                            }, indent=4, ensure_ascii=False)
    except tweepy.error.TweepError as e:
        pass
    
    if resultado:
        return json.loads(resultado)
    else:
        return resultado



def retrieve_initial_tweets(screen_name):
    replys = []
    yesterday = datetime.date.today() - datetime.timedelta(1)
    for tweet in tweepy.Cursor(api.search, q='{}'.format(screen_name), lang="es", tweet_mode='extended').items(10):
        tweet_date = datetime.datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y')
            # Filtro por tweets del dia anterior
        if tweet_date.date() == yesterday:
            if (tweet._json['in_reply_to_status_id']) or (tweet._json['is_quote_status'] == True):
                replys.append(tweet)
            #print(json.dumps(tweet._json, ensure_ascii=False).encode('utf8').decode())
    return replys


def retrieve_all_replys(id_tweet, id_user, initial_replys):
    replys = []
    for tweet in initial_replys:        
        if tweet._json['in_reply_to_status_id'] == id_tweet:            
            resultado = json.dumps({'created_at': tweet._json['created_at'],
                          'id': tweet._json['id'],
                          'text': tweet._json['full_text'],
                          'hashtags': tweet._json['entities']['hashtags'],
                          'user_mentions': tweet._json['entities']['user_mentions'],
                          'urls': tweet._json['entities']['urls'],
                          'user': { 'id': tweet._json['user']['id'],
                                    'name': tweet._json['user']['name'],
                                    'screen_name': tweet._json['user']['screen_name'],
                                    'followers_count': tweet._json['user']['followers_count']},
                          'retweet_count': tweet._json['retweet_count'],
                          'favorite_count': tweet._json['favorite_count'],
                          'in_reply_to_status_id': tweet._json['in_reply_to_status_id'],
                          'is_quote_status': tweet._json['is_quote_status'],
                        }, indent=4, ensure_ascii=False)
            replys.append(json.loads(resultado))            
    
    return replys


def retrieve_all_quotes(id_tweet, id_user, initial_replys):  
    quotes = []
    for tweet in initial_replys:        
        if tweet._json['is_quote_status'] == True:
            try:
                if tweet._json['quoted_status_id'] == id_tweet:
                    resultado = json.dumps({'created_at': tweet._json['created_at'],
                          'id': tweet._json['quoted_status_id'],
                          'text': tweet._json['quoted_status']['full_text'],
                          'hashtags': tweet._json['quoted_status']['entities']['hashtags'],
                          'user_mentions': tweet._json['quoted_status']['entities']['user_mentions'],
                          'urls': tweet._json['quoted_status']['entities']['urls'],
                          'user': { 'id': tweet._json['quoted_status']['user']['id'],
                                    'name': tweet._json['quoted_status']['user']['name'],
                                    'screen_name': tweet._json['quoted_status']['user']['screen_name'],
                                    'followers_count': tweet._json['quoted_status']['user']['followers_count']},
                          'retweet_count': tweet._json['quoted_status']['retweet_count'],
                          'favorite_count': tweet._json['quoted_status']['favorite_count'],
                          'in_reply_to_status_id': tweet._json['quoted_status']['in_reply_to_status_id'],
                          'is_quote_status': tweet._json['quoted_status']['is_quote_status'],
                        }, indent=4, ensure_ascii=False)
                    quotes.append(json.loads(resultado))

            except KeyError as e:
                continue
    
    return quotes



palabra_clave = [
    'covid',
    'covid-19'
    'coronavirus ',
    'aislamiento',
    'cuarentena',
    'empleo',
    'empleos',
    'teletrabajo',
    'negocios',
    'empresas',
    'despidos',
    'trabajo remoto',
    'economía',
    'industria',
    'muerte',
    'gobierno',
    'presidente',
    'pruebas',
    'contagio',
    'educación',
    'liquidéz',
    'confinamiento',
    'e-commerce',
    'comercio electrónico',
    'subsidio',
    'ayuda',
    'miedo',
    'alimentación',
    'alimentos',
    'salud ',
]

yesterday = datetime.date.today() - datetime.timedelta(1)

# Busco los últimos 100 tweets
for i in cuentas:
    tweets = tweepy.Cursor(api.user_timeline, screen_name=i, tweet_mode='extended').items(30)
    initial_tweets = retrieve_initial_tweets(i)
    resultado = dict()
    json_result = dict()

    try:
        client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        client.server_info() # force connection on a request as the
                            # connect=True parameter of MongoClient seems
                            # to be useless here
        db = client.Grupo03
        collection = db.COL_tweets

        for tweet in tweets:    
            #if any(palabra in tweet.full_text.lower() for palabra in palabra_clave): Tue Apr 07 13:09:26 +0000 2020
            tweet_date = datetime.datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y')
            # Filtro por tweets del dia anterior
            if tweet_date.date() == yesterday:
                resultado = json.dumps({'created_at': tweet._json['created_at'],
                                'id': tweet._json['id'],
                                'full_text': tweet._json['full_text'],
                                'hashtags': tweet._json['entities']['hashtags'],
                                'user_mentions': tweet._json['entities']['user_mentions'],
                                'urls': tweet._json['entities']['urls'],
                                'user': { 'id': tweet._json['user']['id'],
                                        'name': tweet._json['user']['name'],
                                        'screen_name': tweet._json['user']['screen_name'],
                                        'followers_count': tweet._json['user']['followers_count']},
                                'retweet_count': tweet._json['retweet_count'],
                                'favorite_count': tweet._json['favorite_count'],
                                'in_reply_to_status_id': tweet._json['in_reply_to_status_id'],
                                'is_quote_status': tweet._json['is_quote_status'],
                            }, indent=4, ensure_ascii=False)
            
                json_result = (json.loads(resultado))
                # Valida si es un reply
                if tweet._json['in_reply_to_status_id'] != None:
                    json_result['status_replied'] = retrieve_replied_tweet(tweet._json['in_reply_to_status_id'])
                # Valida si es una cita
                if tweet._json['is_quote_status'] == True:
                    try:
                        json_result['quoted_status'] = json.loads(json.dumps({'created_at': tweet._json['quoted_status']['created_at'],
                                                                    'id': tweet._json['quoted_status']['id'],
                                                                    'full_text': tweet._json['quoted_status']['full_text'],
                                                                    'hashtags': tweet._json['quoted_status']['entities']['hashtags'],
                                                                    'user_mentions': tweet._json['quoted_status']['entities']['user_mentions'],
                                                                    'urls': tweet._json['quoted_status']['entities']['urls'],
                                                                    'user': { 'id': tweet._json['quoted_status']['user']['id'],
                                                                            'name': tweet._json['quoted_status']['user']['name'],
                                                                            'screen_name': tweet._json['quoted_status']['user']['screen_name'],
                                                                            'followers_count': tweet._json['quoted_status']['user']['followers_count']},
                                                                    'retweet_count': tweet._json['quoted_status']['retweet_count'],
                                                                    'favorite_count': tweet._json['quoted_status']['favorite_count'],
                                                                }, indent=4, ensure_ascii=False))
                    except KeyError as e:
                        continue
                #json_result['replys'] = retrieve_all_replys(tweet._json['id'], tweet._json['user']['id'], initial_tweets)
                #json_result['quotes'] = retrieve_all_quotes(tweet._json['id'], tweet._json['user']['id'], initial_tweets)
                #print(json.dumps(json_result, ensure_ascii=False).encode('utf8').decode())
                post_id = collection.insert_one(json_result).inserted_id
                print('Termino: ' + i)


    except errors.ServerSelectionTimeoutError as err:
        # do whatever you need
        print(err)