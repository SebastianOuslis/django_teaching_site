# Generated by Django 3.0.6 on 2020-06-29 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0020_auto_20200617_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_being_followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_being_followed', to=settings.AUTH_USER_MODEL)),
                ('user_doing_following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_doing_following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
