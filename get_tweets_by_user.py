import json
import logging

import tweepy

from tweepy_initializer import api
from util import process_lock

file_name = "tweet_data_by_user.json"


def get_user_timeline(user_id):
    try:
        return {
            e.id: e._json
            for e in tweepy.Cursor(api.user_timeline, user_id=user_id, count=200, tweet_mode="extended").items()
        }
    except tweepy.errors.Unauthorized:
        logging.info(f"user_id: {user_id} Unauthorized. The user's time line is maybe private.")
    return {}


def get_tweets_by_user():
    lock = process_lock()
    if not lock:
        print("lock error")
        exit(1)

    set_users_checked_accepted = read_user_ids("user_pages_by_hash_tag_checked_accept.txt")
    set_users_checked_accepted_finished = read_user_ids("user_pages_by_hash_tag_checked_accept_finished.txt")

    for user_id in list(set_users_checked_accepted):
        try:
            timeline = get_user_timeline(user_id)
            with open(f"tweet_data_by_user/{user_id}.json", mode="w", encoding="utf-8") as f:
                f.write(json.dumps(timeline, indent=2, ensure_ascii=False))

            set_users_checked_accepted.remove(user_id)
            set_users_checked_accepted_finished.add(user_id)

            write_user_pages(set_users_checked_accepted, "user_pages_by_hash_tag_checked_accept.txt")

            write_user_pages(
                set_users_checked_accepted_finished,
                "user_pages_by_hash_tag_checked_accept_finished.txt",
            )

        except Exception:
            logging.exception("")
            pass


def read_user_ids(path):
    with open(path, "r", encoding="utf-8") as f:
        return {int(e.replace("https://twitter.com/i/user/", "")) for e in f.readlines()}


def write_user_pages(user_ids, path):
    with open(path, mode="w", encoding="utf-8") as f:
        f.writelines([f"https://twitter.com/i/user/{e}\n" for e in sorted(user_ids)])
