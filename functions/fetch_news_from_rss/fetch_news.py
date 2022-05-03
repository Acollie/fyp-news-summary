import feedparser
from datetime import datetime
from time import mktime
import yaml
import requests
from bs4 import BeautifulSoup
import time
import boto3
import os


# This function reformats the HTML body using BeautifulSoup
# Which allows for the useful HTML to be extracted.
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

# This function uploads the local contents to s3 bucket
# https://stackoverflow.com/a/48945900/15879865
def upload_yaml():

    s3 = boto3.resource('s3')
    # This location is used because a limitation of serverless function
    for filename in os.listdir("/tmp/"):
        if filename.find(".yaml") != -1:
            data = open("/tmp/"+filename, "rb")
            s3.Bucket('fyp-news-data-bucket').put_object(Key=filename, Body=data)

# This function fetches the news from the CNN RSS feed.
# Then places it inside a YAML file which is a form of markup lanauge so it can be easily read by a human
def fetch_news():
    NewsFeed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
    dict_file = {}
    file = open('/tmp/'+str(int(time.time()))+".yaml", "w")
    for news in NewsFeed.entries:
        if "summary" in news.keys():
            # hash_key = news.summary.encode('utf-8')
            item_key = news.title

            dt = datetime.fromtimestamp(mktime(news.published_parsed))
            # Saving the item into a dictionary
            dict_file[item_key] = {
                "title": news.title,
                "summary": news.summary,
                "link": news.link,
                "full_text": fetch_news_from_url(news.link),
                "date": {
                    "year":dt.year,"month":dt.month,
                    "day":dt.day,
                    "hour":dt.hour,
                    "minute":dt.minute}

               }
    # This saves the dictionary into a file
    yaml.dump(dict_file, file)

# This is the entry point the lamda function expects
def lambda_handler(event, context):
    fetch_news()
    upload_yaml()
    return True

# This is used for testing the function when run without the lamda function.
if __name__ == '__main__':
    lambda_handler(None, None)