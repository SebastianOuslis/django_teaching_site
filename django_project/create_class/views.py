from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
    )
from django.contrib.auth.models import User
from blog.models import (
    Category, TypeOfClasses, Post, Review, RatingOptions, ClassRoot, TimeForClass, ClassPurchaseInfo, ClassOneOnOneInfo, ClassStreamInfo, ClassVideoInfo
    )
from django.conf import settings
from .forms import ClassRootCreate, CreateTimeForClass, CreatePurchaseInfo, CreateStreamInfo, CreateVideoInfo
from users.models import Profile, ListOfInstructors
from django.contrib import messages


class CreateClassStepOne(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        messages.warning(self.request, f'You must be an instructor to create a class, please contact us to make you an instructor')
        return False

    def handle_no_permission(self):
        return redirect('home')


class CreateClassStreamNoPay(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    # def post(self, request, **kwargs):
    #     p_form = ProfileUpdateFormStudent(request.POST, instance=request.user.profile)
    #     if p_form.is_valid():
    #         p_form.save()
    #         messages.success(request, f'Your Profile has been updated!')
    #         return redirect('profile_student')
    #     else:
    #         messages.warning(request, f'Please try again')
    #         return redirect('profile_student')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_create_form = ClassRootCreate(prefix='class_form')
        class_stream_form = CreateStreamInfo(prefix='stream_form')
        time_form = CreateTimeForClass(prefix='time_form')
        context['class_create_form'] = class_create_form
        context['stream_create_form'] = class_stream_form
        context['time_form'] = time_form
        return context

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in
                                        list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        messages.warning(self.request,
                         f'You must be an instructor to create a class, please contact us to make you an instructor')
        return False

    def handle_no_permission(self):
        return redirect('home')


class CreateClassStreamPay(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def post(self, request, **kwargs):
        return render(request, "create_class/create_stream_pay.html")


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_create_form = ClassRootCreate(prefix='class_form')
        class_stream_form = CreateStreamInfo(prefix='stream_form')
        purchase_form = CreatePurchaseInfo(prefix='purchase_form')
        time_form = CreateTimeForClass(prefix='time_form')
        context['class_create_form'] = class_create_form
        context['stream_create_form'] = class_stream_form
        context['time_form'] = time_form
        context['purchase_form'] = purchase_form
        return context

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        messages.warning(self.request, f'You must be an instructor to create a class, please contact us to make you an instructor')
        return False

    def handle_no_permission(self):
        return redirect('home')


class CreateClassOneToOnePay(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def post(self, request, **kwargs):
        return render(request, "create_class/create_one_on_one_pay.html", )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_create_form = ClassRootCreate(prefix='class_form')
        purchase_form = CreatePurchaseInfo(prefix='purchase_form')
        time_form = CreateTimeForClass(prefix='time_form')
        context['class_create_form'] = class_create_form
        context['time_form'] = time_form
        context['purchase_form'] = purchase_form
        return context

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        messages.warning(self.request, f'You must be an instructor to create a class, please contact us to make you an instructor')
        return False

    def handle_no_permission(self):
        return redirect('home')

class CreateClassVideoPay(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_create_form = ClassRootCreate(prefix='class_form')
        purchase_form = CreatePurchaseInfo(prefix='purchase_form')
        video_form = CreateVideoInfo(prefix='video_form')
        context['class_create_form'] = class_create_form
        context['video_form'] = video_form
        context['purchase_form'] = purchase_form
        return context

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        messages.warning(self.request, f'You must be an instructor to create a class, please contact us to make you an instructor')
        return False

    def handle_no_permission(self):
        return redirect('home')