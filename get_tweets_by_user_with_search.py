import datetime
import glob
import json
import logging

import tweepy

from filter_tweets import searched_tag_to_datetime
from tweepy_initializer import api
from util import process_lock

FILE_NAME = "tweet_data_by_hash_tag.json"

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def search_tweets(query, oldest_tweet_id, fromDate="200603210000", toDate=None, use_premium=False):
    if use_premium:
        return {
            e.id: e._json
            for e in tweepy.Cursor(
                api.search_full_archive,
                query=query,
                label="",
                fromDate=fromDate,
                toDate=toDate,
                maxResults=500,
            ).items()
        }
    else:
        return {
            e.id: e._json
            for e in tweepy.Cursor(
                api.search_tweets,
                q=query,
                count=100,
            ).items()
        }


def get_tweets_by_user_with_search():
    lock = process_lock()
    if not lock:
        print("lock error")
        exit(1)

    with open("user_to_searched_tag.json", mode="r", encoding="utf-8") as f:
        user_to_searched_tag = json.load(f)

    for path in glob.glob("tweet_data_by_user/*.json"):
        with open(path, "r", encoding="utf-8") as f:
            timeline = json.load(f)

        if len(timeline) < 3000:
            continue
        if len(timeline) > 3200:
            continue

        user_id = path.replace("tweet_data_by_user/", "").replace(".json", "")

        screen_name = list(timeline.values())[0]["user"]["screen_name"]
        oldest_tweet_id = min([t for t in timeline])
        toDate = datetime.datetime.strptime(
            timeline[oldest_tweet_id]["created_at"], "%a %b %d %H:%M:%S %z %Y"
        ) + datetime.timedelta(minutes=1)

        if user_id not in user_to_searched_tag:
            fromDate = "202110010000"
            logging.warning(f"{user_id}: searched_tag not found.")
            # maybe retweet
        else:
            searched_tags = user_to_searched_tag[user_id]
            searched_datetime = min([searched_tag_to_datetime(e) for e in searched_tags])
            fromDate = searched_datetime.strftime("%Y%m%d%H%M")

            if searched_datetime > toDate:
                continue

        print(f"{user_id}: total: {len(timeline)}")
        toDate = toDate.strftime("%Y%m%d%H%M")

        # continue

        # new_tweets = search_tweets(f"from:{screen_name}", oldest_tweet_id)
        new_tweets = search_tweets(f"from:{screen_name} -is:retweet", oldest_tweet_id, fromDate, toDate, True)
        if len(new_tweets) > 0:
            timeline.update(new_tweets)
            with open(path, mode="w", encoding="utf-8") as f:
                f.write(json.dumps(timeline, indent=2, ensure_ascii=False))
        print(f"{user_id}: new tweets: {len(new_tweets)},  total: {len(timeline)}")
