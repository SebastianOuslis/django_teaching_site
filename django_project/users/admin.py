from django.contrib import admin
from .models import Profile, ListOfInstructors, SignupInstructorList

admin.site.register(Profile)
admin.site.register(ListOfInstructors)
admin.site.register(SignupInstructorList)

