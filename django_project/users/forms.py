from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

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

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'instagram_handle', 'youtube_channel', 'short_description', 'description', 'image']
        widgets = {
            'instagram_handle': forms.Textarea(attrs={'rows':1, 'cols':8}),
            'youtube_channel': forms.Textarea(attrs={'rows':1, 'cols':8}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['instagram_handle'].required = False
        self.fields['youtube_channel'].required = False
