import boto3
import yaml
from final_year_project_django.models import News
import datetime

# The purpose of this function is to sync the local database with the online database.

def data_sync():
    # This gets an instance of the s3 bucket
    s3 = boto3.resource("s3")
    fyp_bucket = s3.Bucket("fyp-news-data-bucket")

    # This makes a list of all of the titles of the news articles and puts them into a set
    news_titles = set()
    for news_article in News.objects.all():
        news_titles.add(news_article.title)
    # This loops over the contents of the bucket
    for file_name in fyp_bucket.objects.all():
        # This skips if the file has already been read.
        if file_name.key.find("read:") == -1:
            # This then loads the contains of the file yaml which is then understood as a nested dictionary
            data = yaml.load(file_name.get()['Body'].read(), Loader=yaml.FullLoader)
            # The program then loops over the articles in the yaml file

            for article in data.keys():
                title = data[article]['title']
                full_text = data[article]['full_text']
                summary = data[article]['summary']
                # This is because the same article an appear in multiple news files so to avoid duplication
                # as the program will only add the articles if the event has not already been seen.
                if title not in news_titles:
                    # This then saves the file into database
                    item = News(news_source='CNN', title=title, body=full_text, body_tldr=summary,
                                date=datetime.datetime.now())
                    item.save()
        # Renaming the files which have now been read.
        s3.Object('fyp-news-data-bucket', "read:"+file_name.key).copy_from(CopySource='fyp-news-data-bucket/'+file_name.key)
        s3.Object('fyp-news-data-bucket', file_name).delete()


if __name__ == '__main__':
    data_sync()