from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from users.models import Profile

class Category(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class TypeOfClasses(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class RatingOptions(models.Model):
    number = models.IntegerField(default=1)

    def __str__(self):
        return str(self.number)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_profile = models.ForeignKey(Profile, null=True, default=None, on_delete=models.SET_DEFAULT)
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.SET_DEFAULT)
    is_purchase = models.BooleanField(default=False)
    type_of_class = models.ForeignKey(TypeOfClasses, null=True, default=None, on_delete=models.SET_DEFAULT)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, validators=[MinValueValidator(0.51)])
    initial_spots = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    spots_available = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def save(self, *args, **kwargs):
        self.spots_available = self.initial_spots
        self.author_profile = Profile.objects.filter(user=self.author).first()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Review(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    review_text = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name='author_of_review', on_delete=models.CASCADE)
    user_being_reviewed = models.ForeignKey(User, related_name='user_being_reviewed', on_delete=models.CASCADE)
    user_rating_out_of_five = models.ForeignKey(RatingOptions, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.author.username)+" rated "+str(self.user_being_reviewed.username) + " " + str(self.user_rating_out_of_five.number) + " out of 5"