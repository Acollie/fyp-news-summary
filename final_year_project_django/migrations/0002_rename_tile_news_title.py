# Generated by Django 3.2.12 on 2022-02-14 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final_year_project_django', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='tile',
            new_name='title',
        ),
    ]