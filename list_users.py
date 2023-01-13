import json
import logging


def list_users():
    logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

    file_name = "tweet_data_by_hash_tag.json"

    with open(file_name, mode="r", encoding="utf-8") as f:
        tweet_data = json.loads(f.read())

    # for tweet in tweet_data.values():
    #     flg_is_retweet = 'retweeted_status' in tweet
    #     text = tweet['text'] = 'extended_tweet' not in tweet

    set_users_all = {e["user"]["id"] for e in tweet_data.values()}
    set_users_not_retweet = {e["user"]["id"] for e in tweet_data.values() if "retweeted_status" not in e}
    set_users_retweet = {e for e in set_users_all if e not in set_users_not_retweet}

    with open("user_pages_by_hash_tag_all.txt", mode="w", encoding="utf-8") as f:
        f.writelines([f"https://twitter.com/i/user/{e}\n" for e in set_users_all])

    with open("user_pages_by_hash_tag_not_retweet.txt", mode="w", encoding="utf-8") as f:
        f.writelines([f"https://twitter.com/i/user/{e}\n" for e in set_users_not_retweet])

    with open("user_pages_by_hash_tag_users_retweet.txt", mode="w", encoding="utf-8") as f:
        f.writelines([f"https://twitter.com/i/user/{e}\n" for e in set_users_retweet])

    with open("user_pages_by_hash_tag_checked.txt", mode="r", encoding="utf-8") as f:
        set_users_checked = {int(e.replace("https://twitter.com/i/user/", "")) for e in f.readlines()}

    with open("user_pages_by_hash_tag_checked_accept.txt", mode="r", encoding="utf-8") as f:
        set_users_checked_accepted = {int(e.replace("https://twitter.com/i/user/", "")) for e in f.readlines()}

    with open("user_pages_by_hash_tag_checked_rejected.txt", mode="r", encoding="utf-8") as f:
        set_users_checked_rejected = {int(e.replace("https://twitter.com/i/user/", "")) for e in f.readlines()}

    set_users_not_checked = {
        e
        for e in set_users_not_retweet
        if e not in set_users_checked and e not in set_users_checked_accepted and e not in set_users_checked_rejected
    }

    with open("user_pages_by_hash_tag_not_checked.txt", mode="w", encoding="utf-8") as f:
        f.writelines([f"https://twitter.com/i/user/{e}\n" for e in set_users_not_checked])
