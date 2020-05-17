from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateFormInstructor, ProfileUpdateFormStudent
from django.views.generic import ListView, UpdateView
from payments.models import Purchases
from django.contrib.auth.models import User
from .models import Profile, ListOfInstructors
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, you can now login')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if p_form.is_valid():
#             p_form.save()
#             messages.success(request, f'Your Profile has been updated!')
#             return redirect('profile')
#     else:
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'p_form': p_form
#     }
#     return render(request, 'users/profile.html', context)


class ProfileUpdateViewInstructor(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateFormInstructor
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def post(self, request, **kwargs):
        p_form = ProfileUpdateFormInstructor(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
        else:
            messages.warning(request, f'Please try again')
            return redirect('profile')


        messages.success(request, f'Your Profile has been updated!')
        return super(ProfileUpdateViewInstructor, self).post(request, **kwargs)

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        return False

    def handle_no_permission(self):
        return redirect('profile_student')

class ProfileUpdateViewStudent(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateFormStudent
    success_url = reverse_lazy('profile_student')

    def get_object(self):
        return self.request.user

    def post(self, request, **kwargs):
        p_form = ProfileUpdateFormStudent(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile_student')
        else:
            messages.warning(request, f'Please try again')
            return redirect('profile_student')

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return False
        return True

    def handle_no_permission(self):
        return redirect('profile')

class UserSalesListView(ListView):
    model = Purchases
    template_name = 'users/user_sales.html'
    context_object_name = 'sales'
    paginate_by = 5

    def get_queryset(self):
        return Purchases.objects.filter(user_bought_from=self.request.user).order_by('-date_bought')




