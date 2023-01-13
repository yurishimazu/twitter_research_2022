import tweepy

API_KEY = ""
API_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
)
