# Generated by Django 3.0.6 on 2020-05-16 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200515_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='youtube_short_link',
            field=models.TextField(default=''),
        ),
    ]
