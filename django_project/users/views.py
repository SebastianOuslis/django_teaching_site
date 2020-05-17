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
    #
    # def post(self, request, **kwargs):
    #     messages.success(request, f'Your Profile has been updated!')
    #     return super(ProfileUpdateViewInstructor, self).post(request, **kwargs)

    def test_func(self):
        list_of_instructors = ListOfInstructors.objects.all()
        print(list_of_instructors)
        if self.request.user in list_of_instructors:
            return True
        return redirect("profile_student")

class ProfileUpdateViewStudent(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateFormStudent
    success_url = reverse_lazy('profile_student')

    def get_object(self):
        return self.request.user
    #
    # def post(self, request, **kwargs):
    #     messages.success(request, f'Your Profile has been updated!')
    #     return super(ProfileUpdateViewStudent, self).post(request, **kwargs)

    def test_func(self):
        list_of_instructors = ListOfInstructors.objects.all()
        print(list_of_instructors)
        if self.request.user in list_of_instructors:
            return redirect("profile")
        return True

class UserSalesListView(ListView):
    model = Purchases
    template_name = 'users/user_sales.html'
    context_object_name = 'sales'
    paginate_by = 5

    def get_queryset(self):
        return Purchases.objects.filter(user_bought_from=self.request.user).order_by('-date_bought')




