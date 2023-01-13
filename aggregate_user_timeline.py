import csv
import itertools
import logging
import unicodedata
from pathlib import Path

import emoji

from filter_tweets import load_filtered_tweets
from normalize_neologd import normalize_neologd


def aggregate_user_timeline(path, file_name, user_to_searched_tags):
    i = 0

    with open("user_pages_by_hash_tag_checked_accept_finished.txt", "r", encoding="utf-8") as f:
        user_ids_accepted = [e.strip().replace("https://twitter.com/i/user/", "") for e in f.readlines()]
    user_count = len(user_ids_accepted)

    with open(file_name, mode="w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["created_at", "searched_tags", "user_id", "text"])

        for user_id in user_ids_accepted:
            i += 1
            data_path = Path(path) / f"{user_id}.json"
            tweet_data = load_filtered_tweets(data_path, user_to_searched_tags, True)

            if len(tweet_data) == 0:
                logging.info(f"{i}/{user_count}: {data_path} skipped")
                continue

            created_at = [e["created_at"] for e in tweet_data.values()]
            user_ids = [e["user"]["id"] for e in tweet_data.values()]
            searched_tags = itertools.repeat(user_to_searched_tags[user_id], len(user_ids))
            text = [
                e["full_text"]
                if "full_text" in e
                else e["extended_tweet"]["full_text"]
                if "extended_tweet" in e
                else e["text"]
                for e in tweet_data.values()
            ]
            text = [normalize(e) for e in text]

            writer.writerows([e for e in zip(created_at, searched_tags, user_ids, text)])

            logging.info(f"{i}/{user_count}: {data_path}")


dict_trans = {}
with open("置換対応表.txt", mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for line in reader:
        dict_trans[line[0]] = line[1]

tr = str.maketrans(dict(zip("()!", "（）！")))


def normalize(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(tr)
    text = emoji.demojize(text)
    text = normalize_neologd(text)
    for k, v in dict_trans.items():
        text = text.replace(k, v)
    return text
