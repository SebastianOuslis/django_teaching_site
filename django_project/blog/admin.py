from django.contrib import admin
from .models import Category, TypeOfClasses, Post, Review, RatingOptions

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(TypeOfClasses)
admin.site.register(Review)
admin.site.register(RatingOptions)
