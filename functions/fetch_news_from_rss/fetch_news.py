import feedparser
from datetime import datetime
from time import mktime
import yaml
import hashlib
import pickle
import requests
from bs4 import BeautifulSoup
import time
import boto3
import os


def fetch_cnn_body(page):
    print("parsing")
    soup = BeautifulSoup(page.text, 'html.parser')
    full_text = ""
    for div_box in soup.find_all(class_='Paragraph__component'):
        full_text += div_box.text
    return full_text


def fetch_news_from_url(link):
    page = requests.get(link)
    return fetch_cnn_body(page)


# https://stackoverflow.com/a/48945900/15879865
def upload_yaml():
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    for filename in os.listdir("/tmp/"):
        if filename.find(".yaml") != -1:
            data = open("/tmp/"+filename, "rb")
            s3.Bucket('fyp-news-data-bucket').put_object(Key=filename, Body=data)


def fetch_news(url):
    NewsFeed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
    dict_file = {}
    file = open('/tmp/'+str(int(time.time()))+".yaml", "w")
    for news in NewsFeed.entries:
        if "summary" in news.keys():
            # hash_key = news.summary.encode('utf-8')
            hash = news.title

            dt = datetime.fromtimestamp(mktime(news.published_parsed))
            dict_file[hash] = {
                "title": news.title,
                "summary": news.summary,
                "link": news.link,
                "full_text": fetch_news_from_url(news.link),
                "date": {"year":dt.year,"month":dt.month,"day":dt.day,"hour":dt.hour,"minute":dt.minute}

               }

    yaml.dump(dict_file, file)


def lambda_handler(event, context):
    fetch_news("http://rss.cnn.com/rss/edition.rss")
    upload_yaml()
    return True


if __name__ == '__main__':
    lambda_handler(None, None)