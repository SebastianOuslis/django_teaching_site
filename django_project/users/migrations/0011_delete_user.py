# Generated by Django 3.0.6 on 2020-05-16 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
