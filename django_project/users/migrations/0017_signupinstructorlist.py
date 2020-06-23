# Generated by Django 3.0.6 on 2020-06-17 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_auto_20200521_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupInstructorList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_username', models.TextField(default='')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_info', models.CharField(default='What are you looking to teach?', max_length=150)),
                ('user_requesting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]