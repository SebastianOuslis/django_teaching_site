from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateFormInstructor, ProfileUpdateFormStudent, SignupInstructorForm
from django.views.generic import ListView, UpdateView, TemplateView
from payments.models import Purchases
from django.contrib.auth.models import User
from .models import Profile, ListOfInstructors, SignupInstructorList
from django.urls import reverse_lazy
from django.template import RequestContext

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
        return self.request.user.profile

    def post(self, request, **kwargs):
        p_form = ProfileUpdateFormInstructor(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
        else:
            messages.warning(request, f'Please try again')
            return redirect('profile')

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
        return self.request.user.profile

    def post(self, request, **kwargs):
        p_form = ProfileUpdateFormStudent(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return super(ProfileUpdateViewStudent, self).post(request, **kwargs)
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

class UserSalesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Purchases
    template_name = 'users/user_sales.html'
    context_object_name = 'sales'
    paginate_by = 5

    def get_queryset(self):
        return Purchases.objects.filter(user_bought_from=self.request.user).order_by('-date_bought')

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        return False

    def handle_no_permission(self):
        return redirect('profile')

class UserPurchasesListView(LoginRequiredMixin, ListView):
    model = Purchases
    template_name = 'users/user_purchases.html'
    context_object_name = 'purchases'
    paginate_by = 5

    def get_queryset(self):
        return Purchases.objects.filter(user_bought_by=self.request.user).order_by('-date_bought')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        list_of_instructor_usernames = [d['user_username'] for d in
                                        list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            context["is_instructor"] = True
        else:
            context["is_instructor"] = False
        return context

class InstructorSignupPage(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        signup_instructor_form = SignupInstructorForm(request.POST)
        if signup_instructor_form.is_valid():
            signup_object = SignupInstructorList(user_requesting=self.request.user, request_info=signup_instructor_form.cleaned_data.get('request_info'))
            signup_object.save()
            messages.success(self.request,
                             f'You have been added to the instructor signup list, we will get in contact with you after we have reviewed your application, you may be emailed for more information')
            return redirect('home')
        else:
            print("failed")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        signup_instructor_form = SignupInstructorForm()
        context['signup_instructor_form'] = signup_instructor_form
        return context

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            messages.warning(self.request,
                             f'You are already an instructor')
            return False
        list_of_signup_usernames = [d['user_username'] for d in
                                        list(SignupInstructorList.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_signup_usernames:
            messages.warning(self.request,
                             f'You are already on the signup list')
            return False
        return True

    def handle_no_permission(self):
        return redirect('profile')


def handler404(request, *args, **kwargs):
    return render(request, 'users/404.html', locals())

def handler500(request, *args, **kwargs):
    return render(request, 'users/500.html', locals())

def handler403(request, *args, **kwargs):
    return render(request, 'users/403.html', locals())

def handler400(request, *args, **kwargs):
    return render(request, 'users/400.html', locals())




