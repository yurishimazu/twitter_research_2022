import datetime
import json
from zoneinfo import ZoneInfo

from aggregate_user_timeline import aggregate_user_timeline
from create_user_to_searched_tag_dict import create_user_to_searched_tag_dict
from get_tweets_by_hashtag import get_tweets_by_hashtag
from get_tweets_by_user import get_tweets_by_user
from get_tweets_by_user_with_search import get_tweets_by_user_with_search
from list_users import list_users
from minimize_data import minimize_data, pick_tweet_by_text, trim_data_by_age_of_the_moon, trim_data_by_date


def main():
    # # 指定した tagを使用した tweet の収集
    # get_tweets_by_hashtag()

    # # ユーザーページ一覧の作成
    # list_users()

    # # 収集された tweet のユーザーを目視で確認して選択

    # # tweet data の取得
    # get_tweets_by_user()

    # # 1ユーザーあたり 3200件を超えるtweet data の取得
    # get_tweets_by_user_with_search()

    # ユーザーと使用したtagの対応付けの出力
    create_user_to_searched_tag_dict("tweet_data_by_hash_tag.json")

    # ユーザーと使用したtagの対応付けの目視確認と、複数tag使用時の取捨選択

    # ユーザーと使用したtagの対応付けの読み込み
    with open("user_to_searched_tag_checked.json", mode="r", encoding="utf-8") as f:
        user_to_searched_tags = json.loads(f.read())

    # 解析対象 tweet の csvへの集計
    aggregate_user_timeline(
        "tweet_data_by_user",
        "tweet_data_by_user.csv",
        user_to_searched_tags,
    )

    # 解析対象 tweet の csvへの集計 から、出産月後の tweetのみ取得
    trim_data_by_date(
        "tweet_data_by_user.csv",
        "tweet_data_by_user_trim_by_date.csv",
        datetime.datetime(2022, 8, 1, tzinfo=ZoneInfo("Asia/Tokyo")),
        datetime.datetime(2022, 9, 1, tzinfo=ZoneInfo("Asia/Tokyo")),
    )

    # 解析対象 tweet の csvへの集計 から、出産月後の tweetのみ取得
    minimize_data("tweet_data_by_user_trim_by_date.csv", "tweet_data_by_user_trim_by_date_100000.csv", 100000)

    # 該当単語を含む tweet の取得
    pick_tweet_by_text("tweet_data_by_user_trim_by_date.csv", "picked_tweet", "ワンオペ")
    pick_tweet_by_text("tweet_data_by_user_trim_by_date.csv", "picked_tweet", "ストレス")

    # 月齢単位での取得
    trim_data_by_age_of_the_moon("tweet_data_by_user.csv", "tweet_data_by_user_trim_by_age_of_the_moon_")


if __name__ == "__main__":
    main()
