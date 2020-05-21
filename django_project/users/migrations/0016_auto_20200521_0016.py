# Generated by Django 3.0.6 on 2020-05-21 04:16

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20200520_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default_logo.PNG', upload_to=users.models.user_directory_path),
        ),
    ]
