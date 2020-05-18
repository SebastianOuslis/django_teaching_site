from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import (
    Category, TypeOfClasses, Post, Review, RatingOptions, ClassRoot, TimeForClass, ClassPurchaseInfo, ClassOneOnOneInfo, ClassStreamInfo, ClassVideoInfo
    )

class ClassRootCreate(forms.ModelForm):
    class Meta:
        model = ClassRoot
        fields = ['title', 'content', 'category']

class CreateTimeForClass(forms.ModelForm):
    class Meta:
        model = TimeForClass
        fields = ['time_of_day', 'date']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

class CreatePurchaseInfo(forms.ModelForm):
    class Meta:
        model = ClassPurchaseInfo
        fields = ['cost']

# class CreateOneOnOneInfo(forms.ModelForm):
#     class Meta:
#         model = ClassOneOnOneInfo

class CreateStreamInfo(forms.ModelForm):
    class Meta:
        model = ClassStreamInfo
        fields = ["max_number_of_viewers"]

class CreateVideoInfo(forms.ModelForm):
    class Meta:
        model = ClassVideoInfo
        fields = ["video_name", "video_file"]

