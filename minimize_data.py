import csv
import datetime
from random import randrange
from zoneinfo import ZoneInfo

from filter_tweets import searched_tag_to_datetime


def minimize_data(src, dest, count):
    with open(dest, "w", newline="", encoding="utf-8") as writer:
        writer = csv.writer(writer)

        with open(src, newline="", encoding="utf-8") as reader:
            reader = csv.reader(reader)
            lines = list(reader)
            writer.writerow(lines[0])
            del lines[0]

            for _ in range(count):
                i = randrange(0, len(lines))
                writer.writerow(lines[i])
                del lines[i]


def trim_data_by_date(src, dest, start, end):
    with open(dest, "w", newline="", encoding="utf-8") as writer:
        writer = csv.writer(writer)

        with open(src, newline="", encoding="utf-8") as reader:
            reader = csv.reader(reader)
            writer.writerow(next(reader))

            for line in reader:
                date = datetime.datetime.strptime(line[0], "%a %b %d %H:%M:%S %z %Y") + datetime.timedelta(minutes=1)
                if start < date and date < end:
                    writer.writerow(line)


def pick_tweet_by_text(src, dest, text):
    with open(f"{dest}_{text}.csv", "w", newline="", encoding="utf-8") as writer:
        writer = csv.writer(writer)

        with open(src, newline="", encoding="utf-8") as reader:
            reader = csv.reader(reader)
            writer.writerow(next(reader))

            for line in reader:
                if text in line[3]:
                    writer.writerow(line)


def trim_data_by_age_of_the_moon(src, dest):
    end = datetime.datetime(2022, 9, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
    writers = [csv.writer(open(f"{dest}_{i:02}.csv", "w", newline="", encoding="utf-8")) for i in range(12)]

    with open(src, newline="", encoding="utf-8") as reader:
        reader = csv.reader(reader)
        header = next(reader)
        for w in writers:
            w.writerow(header)

        for line in reader:
            date = datetime.datetime.strptime(line[0], "%a %b %d %H:%M:%S %z %Y")
            if date > end:
                continue

            searched_datetime = min([searched_tag_to_datetime(e) for e in eval(line[1])])
            age_of_the_moon = (date.month - searched_datetime.month) % 12
            writers[age_of_the_moon].writerow(line)
