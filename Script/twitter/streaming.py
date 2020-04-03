import tweepy

palabras_clave = ["Coronavirus"]
ubicacion = [-79.2393655741,-4.23168726,-66.8799180948,12.7060548104]

class TweetsListener(tweepy.StreamListener):

    def on_connect(self):
        print("Estoy conectado!")

    def on_status(self, status):
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                print('RT')
                print(status.retweeted_status.extended_tweet["full_text"])
            except AttributeError:
                print(status.retweeted_status.text)
        else:
            try:
                print('Twitt extendido')
                print(status.extended_tweet["full_text"])
            except AttributeError:
                print('Twitt corto')
                print(status.text)

    def on_error(self, status_code):
        print("Error", status_code)



consumer_key = "FGqkOJU3o3Rh15alV5Ql4obUX"
consumer_secret = "2vIiKctsxxezL6kKGo4qtyFPDcY1viFz6M1a2bHLTwWrijVXE5"
access_token = "151179935-HLh8FmhbS0D3892npnkfiM6UNc1hLZ0NRHKhZCzJ"
access_token_secret = "tiKTQPpveXHZRsEm0ODUeCJGmlSBqqeUzO7F7cRYKrTp6"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


stream = TweetsListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream, tweet_mode='extended')
streamingApi.filter(
    # follow=["151179935"],
    #track=["Coronavirus"],
    #locations=[-79.2393655741,-4.23168726,-66.8799180948,12.7060548104] # Ciudad de Mexico
    #place_country='CO'
    languages=['es'], track=palabras_clave, locations=ubicacion
)