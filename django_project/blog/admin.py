from django.contrib import admin
from .models import (
    Category, TypeOfClasses, Post, Review, RatingOptions, ClassRoot, TimeForClass, ClassPurchaseInfo, ClassOneOnOneInfo, ClassStreamInfo, ClassVideoInfo
    )

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(TypeOfClasses)
admin.site.register(Review)
admin.site.register(RatingOptions)
admin.site.register(ClassRoot)
admin.site.register(TimeForClass)
admin.site.register(ClassPurchaseInfo)
admin.site.register(ClassOneOnOneInfo)
admin.site.register(ClassStreamInfo)
admin.site.register(ClassVideoInfo)
