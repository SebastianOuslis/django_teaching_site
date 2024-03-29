# Generated by Django 3.0.6 on 2020-05-16 02:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_youtube_profile_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='youtube_profile_link',
            field=models.TextField(default='', validators=[django.core.validators.RegexValidator('(https?://)?(www\\.)?((youtube\\.(com))/watch\\?v=([-\\w]+)|youtu\\.be/([-\\w]+))', message='Please put a valid youtube link')]),
        ),
    ]
