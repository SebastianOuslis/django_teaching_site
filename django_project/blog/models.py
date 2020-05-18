from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from users.models import Profile
import datetime
from django.utils.translation import gettext as _

# values for choices
TIME_VALUES_COLON_SPLIT = ['00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30',
                           '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30',
                           '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
                           '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
                           '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']
TIME_STRINGS = ['12:00 AM', '12:30 AM', '01:00 AM', '01:30 AM', '02:00 AM', '02:30 AM', '03:00 AM', '03:30 AM',
                '04:00 AM', '04:30 AM', '05:00 AM', '05:30 AM', '06:00 AM', '06:30 AM', '07:00 AM', '07:30 AM',
                '08:00 AM', '08:30 AM', '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
                '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM',
                '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM', '07:30 PM',
                '08:00 PM', '08:30 PM', '09:00 PM', '09:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM']

TIME_CHOICES = ( (TIME_VALUES_COLON_SPLIT[i],TIME_STRINGS[i]) for i in range(0,48) )

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

class ClassRoot(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_profile = models.ForeignKey(Profile, null=True, default=None, on_delete=models.SET_DEFAULT)
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.SET_DEFAULT)
    is_purchase = models.BooleanField(default=False)
    is_one_on_one = models.BooleanField(default=False)
    is_stream = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.spots_available = self.initial_spots
        self.author_profile = Profile.objects.filter(user=self.author).first()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('class-detail', kwargs={'pk': self.pk})


class TimeForClass(models.Model):

    # for forms that need date
    # date_field = forms.DateField(
    #     widget=forms.TextInput(
    #         attrs={'type': 'date'}
    #     )
    # )
    # def clean_date(self):
    #         date = self.cleaned_data['date']
    #         if date <= datetime.date.today():
    #             raise forms.ValidationError("The date cannot be in the past or today!")
    #         return date

    def validate_date(date):
        if date < timezone.now().date():
            raise ValidationError("Date cannot be in the past")

    classroot = models.ForeignKey(ClassRoot, on_delete=models.CASCADE)
    time_of_day = models.CharField(max_length=6, choices=TIME_CHOICES)
    date = models.DateField(_("Date"), default=datetime.date.today, validators=[validate_date])

class ClassPurchaseInfo(models.Model):
    classroot = models.ForeignKey(ClassRoot, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, validators=[MinValueValidator(3.01)])
    # add currency

    def __str__(self):
        return self.classroot.title + " costs " + str(self.cost) + "$"


class ClassOneOnOneInfo(models.Model):
    classroot = models.ForeignKey(ClassRoot, on_delete=models.CASCADE)
    class_time = models.ForeignKey(TimeForClass, null=True, default=None, on_delete=models.SET_DEFAULT)


class ClassStreamInfo(models.Model):
    classroot = models.ForeignKey(ClassRoot, on_delete=models.CASCADE)
    max_number_of_viewers = models.PositiveIntegerField(default=20, validators=[MinValueValidator(5), MaxValueValidator(30)])
    stream_time = models.ForeignKey(TimeForClass, null=True, default=None, on_delete=models.SET_DEFAULT)


class ClassVideoInfo(models.Model):
    classroot = models.ForeignKey(ClassRoot, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=40, default="Class Video")
    video_file = models.FileField(upload_to='videos/', null=True, verbose_name="")
    # video file
    # https://stackoverflow.com/questions/3116637/django-db-images-video


class Review(models.Model):
    date_posted = models.DateTimeField(default=timezone.now)
    review_text = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name='author_of_review', on_delete=models.CASCADE)
    user_being_reviewed = models.ForeignKey(User, related_name='user_being_reviewed', on_delete=models.CASCADE)
    user_rating_out_of_five = models.ForeignKey(RatingOptions, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.author.username)+" rated "+str(self.user_being_reviewed.username) + " " + str(self.user_rating_out_of_five.number) + " out of 5"