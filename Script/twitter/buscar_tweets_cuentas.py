import tweepy
import json
from pprint import pprint

palabras_clave = ["Coronavirus", "covid19"]

consumer_key = "FGqkOJU3o3Rh15alV5Ql4obUX"
consumer_secret = "2vIiKctsxxezL6kKGo4qtyFPDcY1viFz6M1a2bHLTwWrijVXE5"
access_token = "151179935-HLh8FmhbS0D3892npnkfiM6UNc1hLZ0NRHKhZCzJ"
access_token_secret = "tiKTQPpveXHZRsEm0ODUeCJGmlSBqqeUzO7F7cRYKrTp6"

# consumer_key = "hwQLsT9LMp90MPSgYXf7Abvzw"
# consumer_secret = "wSYKwJPPvaAvPD2KL8dGrkm8kJORCIPss5qVLMuLMAZxWGUcb8"
# access_token = "52602353-a7v7fPQ90BvjVNBR1ZYg6ziiHCiyqfmzdcuS150em"
# access_token_secret = "roy6xRVWbYF2K2BNog9Fi04lArpuNLmY8OIMJWkChrEmW"

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

def retrieve_all_replys(id_tweet, id_user):
    #print('llego')
    replys = []
    for tweet in tweepy.Cursor(api.search, q='claudialopez filter:replies', result_type='recent').items(100):
        #print(tweet._json['in_reply_to_status_id'])
        if tweet._json['in_reply_to_status_id'] == id_tweet:
            resultado = json.dumps({'created_at': tweet._json['created_at'],
                          'id': tweet._json['id'],
                          'text': tweet._json['text'],
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
tweets = tweepy.Cursor(api.user_timeline, id=cuentas['claudia_lopez'], tweet_mode='extended').items(10)
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

        json_result['replys'] = retrieve_all_replys(tweet._json['id'], tweet._json['user']['id'])

        print(json.dumps(json_result, ensure_ascii=False).encode('utf8').decode())
