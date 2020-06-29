from django.contrib import admin
from .models import Profile, ListOfInstructors, SignupInstructorList, FollowingList

admin.site.register(Profile)
admin.site.register(ListOfInstructors)
admin.site.register(SignupInstructorList)
admin.site.register(FollowingList)

