from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, SignupInstructorList

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateFormInstructor(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'instagram_handle', 'youtube_channel', 'short_description', 'description', 'image', 'youtube_profile_link']
        widgets = {
            'instagram_handle': forms.Textarea(attrs={'rows':1, 'cols':8}),
            'youtube_channel': forms.Textarea(attrs={'rows':1, 'cols':8}),
            'youtube_profile_link': forms.Textarea(attrs={'rows': 1, 'cols': 8}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateFormInstructor, self).__init__(*args, **kwargs)
        self.fields['instagram_handle'].required = False
        self.fields['youtube_channel'].required = False
        self.fields['youtube_profile_link'].required = False

class ProfileUpdateFormStudent(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'image']


class SignupInstructorForm(forms.ModelForm):
    class Meta:
        model = SignupInstructorList
        fields = ['request_info', 'contact_email']

