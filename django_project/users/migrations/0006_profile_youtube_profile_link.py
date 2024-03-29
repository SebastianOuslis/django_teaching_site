# Generated by Django 3.0.6 on 2020-05-16 02:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200514_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='youtube_profile_link',
            field=models.TextField(default='', validators=[django.core.validators.RegexValidator('/(youtube.com|youtu.be)\\/(watch)?(\\?v=)?(\\S+)?/', message='Please put a valid youtube link')]),
        ),
    ]
