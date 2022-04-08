import boto3
import yaml
from final_year_project_django.models import News
import datetime


def data_sync():
    s3 = boto3.resource("s3")
    fyp_bucket = s3.Bucket("fyp-news-data-bucket")
    news_titles = set()
    for news_article in News.objects.all():
        news_titles.add(news_article.title)

    for file_name in fyp_bucket.objects.all():
        # print(file_name.key.find("read:"))
        if file_name.key.find("read:") == -1:
            data = yaml.load(file_name.get()['Body'].read(), Loader=yaml.FullLoader)
            for article in data.keys():
                title = data[article]['title']
                full_text = data[article]['full_text']
                summary = data[article]['summary']
                if title not in news_titles:
                    item = News(news_source='CNN', title=title, body=full_text, body_tldr=summary,
                                date=datetime.datetime.now())
                    item.save()
        s3.Object('fyp-news-data-bucket', "read:"+file_name.key).copy_from(CopySource='fyp-news-data-bucket/'+file_name.key)
        s3.Object('fyp-news-data-bucket', file_name).delete()


if __name__ == '__main__':
    data_sync()