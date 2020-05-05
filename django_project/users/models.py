from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default='Alex')
    last_name = models.CharField(max_length=20, default='Green')
    instagram_handle = models.TextField(default='')
    youtube_channel = models.TextField(default='')
    image = models.ImageField(default='default.PNG', upload_to='profile_pics')
    short_description = models.CharField(max_length=100, default='Add a short description of yourself')
    description = models.TextField(default='Add a description of your Skills and what you can offer as classes')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
