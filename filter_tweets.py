import json
import logging
from datetime import date, datetime, timezone
from glob import glob
from pathlib import Path

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
        return str(o)


def load_filtered_tweets(file_name, user_to_searched_tags, is_filter_retweets: bool):
    if not Path(file_name).exists():
        return {}

    with open(file_name, mode="r", encoding="utf-8") as f:
        tweet_data = json.loads(f.read())

    if len(tweet_data) == 0:
        return {}

    user_ids = {e["user"]["id"] for e in tweet_data.values()}
    if len(user_ids) > 1:
        raise Exception(f"too many user in file. : {file_name}")

    user_id = str(list(user_ids)[0])
    if user_id not in user_to_searched_tags or len(user_to_searched_tags[user_id]) == 0:
        logging.warning(f"searched_tags not found: {user_id}")
        return {}

    searched_tags = user_to_searched_tags[user_id]
    searched_datetime = min([searched_tag_to_datetime(e) for e in searched_tags])

    tweet_data = {
        k: v
        for k, v in tweet_data.items()
        if searched_datetime
        < datetime.strptime(v["created_at"], "%a %b %d %H:%M:%S %z %Y")
    }

    if is_filter_retweets:
        tweet_data = {
            k: v for k, v in tweet_data.items() if "retweeted_status" not in v
        }

    return tweet_data


def save_filter_tweets(file_name):
    tweet_data = load_filtered_tweets(file_name, True)

    old_path = Path(file_name)
    new_path = (
        old_path.parent.parent / (old_path.parent.name + "_filtered") / old_path.name
    )
    with open(new_path, mode="w", encoding="utf-8") as f:
        f.write(
            json.dumps(tweet_data, indent=2, ensure_ascii=False, default=custom_default)
        )


def searched_tag_to_datetime(searched_tag):
    return datetime.strptime(searched_tag, "#%Y%b_baby").astimezone(timezone.utc)


def filter_all_json():
    i = 0
    file_count = len(glob("tweet_data_by_user_with_serched_tag/*.json"))
    for path in glob("tweet_data_by_user_with_serched_tag/*.json"):
        save_filter_tweets(path)
        i += 1
        logging.info(f"{i}/{file_count}: {path}")


def main():
    filter_all_json()


if __name__ == "__main__":
    main()
