from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator
import re

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print(instance)
    return 'profile_pics/user_{0}/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40, default='First Last')
    instagram_handle = models.TextField(default='')
    youtube_channel = models.TextField(default='')
    image = models.ImageField(default='profile_pics/default_logo.PNG', upload_to=user_directory_path)
    short_description = models.CharField(max_length=100, default='Add a short description of yourself')
    description = models.TextField(default='Add a description of your Skills and what you can offer as classes')
    youtube_profile_link = models.TextField(default='')
    youtube_short_link = models.TextField(default='')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        youtube_profile_string = self.youtube_profile_link
        if "youtube" in youtube_profile_string or "youtu" in youtube_profile_string:
            if "=" in youtube_profile_string:
                key_for_vid = re.split("=", youtube_profile_string)[1]
                self.youtube_short_link = key_for_vid
        super().save(*args, **kwargs)

        # img = Image.open(self.image.path)
        #
        # if img.height > 300 or img.width > 300:
        #     output_size = (300,300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

class ListOfInstructors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_username = models.TextField(default='')

    def save(self, *args, **kwargs):
        self.user_username = self.user.username
        super().save(*args, **kwargs)
