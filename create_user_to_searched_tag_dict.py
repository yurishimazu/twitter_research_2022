import json
import logging
from collections import defaultdict
from datetime import date, datetime

logging.basicConfig(level=logging.INFO)


def custom_default(o):
    if hasattr(o, "__iter__"):
        # イテラブルなものはリストに
        return list(o)
    elif isinstance(o, (datetime, date)):
        # 日時の場合はisoformatに
        return o.isoformat()
    else:
        # それ以外は文字列に
        return o


def create_user_to_searched_tag_dict(file_name):
    user_to_searched_tag = defaultdict(set)
    many_tags_users = {}

    with open("user_pages_by_hash_tag_checked_accept_finished.txt", "r", encoding="utf-8") as f:
        user_ids_accepted = [int(e.strip().replace("https://twitter.com/i/user/", "")) for e in f.readlines()]

    with open("hash_tags_finished.txt", "r", encoding="utf-8") as f:
        hash_tags = [e.strip() for e in f.readlines()]

    with open(file_name, mode="r", encoding="utf-8") as f:
        tweet_data = json.loads(f.read())

    if len(tweet_data) == 0:
        return

    for user_id in user_ids_accepted:
        # user_id = 1410770857740312578
        text = [
            e["extended_tweet"]["full_text"]
            if "extended_tweet" in e
            else e["full_text"]
            if "full_text" in e
            else e["text"]
            for e in tweet_data.values()
            if e["user"]["id"] == user_id and "retweeted_status" not in e
        ]

        for hash_tag in hash_tags:
            if any({hash_tag.lower() in e.lower() for e in text}):
                user_to_searched_tag[user_id].add(hash_tag)

        if len(user_to_searched_tag[user_id]) > 1:
            many_tags_users[f"https://twitter.com/i/user/{user_id}"] = [str(user_to_searched_tag[user_id]), *text]

    with open("user_to_searched_tag.json", mode="w", encoding="utf-8") as f:
        f.write(json.dumps(user_to_searched_tag, indent=2, ensure_ascii=False, default=custom_default))

    with open("user_to_searched_tag_many_tags_users.json", mode="w", encoding="utf-8") as f:
        f.write(json.dumps(many_tags_users, indent=2, ensure_ascii=False, default=custom_default))

    return user_to_searched_tag


def main():
    create_user_to_searched_tag_dict("tweet_data_by_hash_tag.json")


if __name__ == "__main__":
    main()
