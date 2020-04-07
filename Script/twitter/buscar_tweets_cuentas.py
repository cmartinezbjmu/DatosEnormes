import tweepy
import json
from pprint import pprint

palabras_clave = ["Coronavirus", "covid19"]

consumer_key = "FGqkOJU3o3Rh15alV5Ql4obUX"
consumer_secret = "2vIiKctsxxezL6kKGo4qtyFPDcY1viFz6M1a2bHLTwWrijVXE5"
access_token = "151179935-HLh8FmhbS0D3892npnkfiM6UNc1hLZ0NRHKhZCzJ"
access_token_secret = "tiKTQPpveXHZRsEm0ODUeCJGmlSBqqeUzO7F7cRYKrTp6"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

cuentas = {
    "claudia_lopez": "137908875",
}



def retrieve_replied_tweet(id_tweet):
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
    
    return json.loads(resultado)


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

# Busco los últimos 100 tweets
tweets = tweepy.Cursor(api.user_timeline, id=cuentas['claudia_lopez'], tweet_mode='extended').items(100)
resultado = dict()
json_result = dict()

for tweet in tweets:    
    if any(palabra in tweet.full_text.lower() for palabra in palabra_clave):
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
            print(json.dumps(json_result, ensure_ascii=False).encode('utf8').decode())

        # Valida si es una cita
        if tweet._json['is_quote_status'] == True:
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





        
        #print(resultado.encode('utf8').decode())

#print(prueba[0])





#print((json.dumps({'tweet_corto': status.text}, ensure_ascii=False).encode('utf8')).decode())