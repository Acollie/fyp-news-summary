from django.db import models

class News(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    news_source = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=200)
    body_tldr = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    date = models.DateField()

