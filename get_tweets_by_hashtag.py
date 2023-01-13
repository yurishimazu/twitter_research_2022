import json
import logging
from pathlib import Path

import tweepy

from tweepy_initializer import api
from util import process_lock

FILE_NAME = "tweet_data_by_hash_tag.json"

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def search_tweets(query):
    return {
        e.id: e._json
        for e in tweepy.Cursor(
            api.search_full_archive,
            label="",
            query=query,
            fromDate="200603210000",
            # maxResults=100 # for free
            maxResults=500,  # for premium
        ).items()
    }

    # standard search api. limited for past 7 days.
    # return {e.id: e._json for e in tweepy.Cursor(api.search_tweets,q=query,lang='ja').items()}

    # API v2
    # tweet_data = []
    # for page in tweepy.Paginator(client.search_recent_tweets, query=query, lang='ja', start_time=datetime.date.min, max_results=100):
    #     tweet_data.extend(page.data)
    #     time.sleep(1)
    # return tweet_data


def get_tweets_by_hashtag():
    lock = process_lock()
    if not lock:
        print("lock error")
        exit(1)

    tweet_data = {}
    if Path(FILE_NAME).exists():
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            tweet_data = json.load(f)

    with open("hash_tags.txt", "r", encoding="utf-8") as f:
        hash_tags = f.readlines()

    try:
        for hash_tag in list(hash_tags):
            # if False:
            tweet_data.update(search_tweets(hash_tag.strip()))

            with open(FILE_NAME, mode="w", encoding="utf-8") as f:
                f.write(json.dumps(tweet_data, indent=2, ensure_ascii=False))

            hash_tags.remove(hash_tag)
            logging.info(f"tag finnished: {hash_tag}")
            with open("hash_tags_finished.txt", "a", encoding="utf-8") as f:
                f.write(f"{hash_tag}")
    except:
        pass

    with open("hash_tags.txt", "w", encoding="utf-8") as f:
        for hash_tag in list(hash_tags):
            f.write(f"{hash_tag}")
