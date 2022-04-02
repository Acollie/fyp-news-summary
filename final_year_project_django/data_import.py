import os
from final_year_project_django.models import News
import datetime
import boto3
import yaml
import django

def add_data_bbc():
    for topic in os.listdir('data/BBC News Summary/News Articles')[1:]:
        for file_name in os.listdir('data/BBC News Summary/News Articles/'+topic):
            file = open('data/BBC News Summary/News Articles/'+topic+"/"+file_name, 'rb')
            title = file.readlines()[0]
            file = open('data/BBC News Summary/News Articles/' + topic + "/" + file_name, 'rb')
            # body = file.read().replace(title, "").replace("\n", "")
            body = file.read()
            summary = open('data/BBC News Summary/Summaries/' + topic + "/" + file_name, 'rb')
            item = News(news_source='BBC news', title=title, body=body, body_tldr=summary.read(), date=datetime.datetime.now())
            item.save()


def sync_from_s3():
    # steps fetch data
    # hash summary
    # add non added results
    django.setup()
    s3 = boto3.resource("s3")
    fyp_bucket = s3.Bucket("fyp-news-data-bucket")
    news_titles = set()
    for news_article in News.objects.all():
        news_titles.add(news_article.title)

    for file_name in fyp_bucket.objects.all():
        if file_name.key.find("read:") == -1:
            data = yaml.load(file_name.get()['Body'].read(), Loader=yaml.FullLoader)
            for article in data.keys():
                title = data[article]['title']
                full_text = data[article]['full_text']
                summary = data[article]['summary']
                year = data[article]['date']['year']
                month = data[article]['date']['month']
                day = data[article]['date']['day']
                hour = data[article]['date']['hour']
                minute = data[article]['date']['minute']
                date_time = datetime.datetime(year, month, day, hour, minute)
                if title not in news_titles:
                    item = News(news_source='CNN', title=title, body=full_text, body_tldr=summary,
                                date=date_time)
                    item.save()
            s3.Object('fyp-news-data-bucket', "read:"+file_name.key).copy_from(CopySource='fyp-news-data-bucket/'+file_name.key)
            s3.Object('fyp-news-data-bucket', file_name.key).delete()

