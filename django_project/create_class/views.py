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

#https://stackoverflow.com/questions/569468/django-multiple-models-in-one-template-using-forms

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
    def post(self, request, *args, **kwargs):
        class_root_form = ClassRootCreate(request.POST, prefix='class_form')
        stream_form = CreateStreamInfo(request.POST, prefix='stream_form')
        time_form = CreateTimeForClass(request.POST, prefix='time_form')
        if class_root_form.is_valid() and stream_form.is_valid() and time_form.is_valid():
            class_root_object = ClassRoot(title=class_root_form.cleaned_data.get('title'), content=class_root_form.cleaned_data.get('content'), author=self.request.user, author_profile=self.request.user.profile,
                                            category=class_root_form.cleaned_data.get('category'), is_purchase=False , is_one_on_one=False , is_stream=True , is_video=False)
            class_root_object.save()
            time_object = TimeForClass(classroot=class_root_object,
                                       time_of_day=time_form.cleaned_data.get('time_of_day'),
                                       date=time_form.cleaned_data.get('date'))
            time_object.save()
            stream_object = ClassStreamInfo(classroot=class_root_object, max_number_of_viewers=stream_form.cleaned_data.get('max_number_of_viewers'), stream_time=time_object)
            stream_object.save()
            messages.success(self.request,
                             f'You have made a free stream')
            return redirect('home')
        else:
            print("failed")

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
    def post(self, request, *args, **kwargs):
        class_root_form = ClassRootCreate(request.POST, prefix='class_form')
        stream_form = CreateStreamInfo(request.POST, prefix='stream_form')
        purchase_form = CreatePurchaseInfo(request.POST, prefix='purchase_form')
        time_form = CreateTimeForClass(request.POST, prefix='time_form')
        if class_root_form.is_valid() and stream_form.is_valid() and time_form.is_valid() and purchase_form.is_valid():
            class_root_object = ClassRoot(title=class_root_form.cleaned_data.get('title'), content=class_root_form.cleaned_data.get('content'), author=self.request.user, author_profile=self.request.user.profile,
                                            category=class_root_form.cleaned_data.get('category'), is_purchase=True, is_one_on_one=False , is_stream=True , is_video=False)
            class_root_object.save()
            purchase_object = ClassPurchaseInfo(classroot=class_root_object, cost=purchase_form.cleaned_data.get('cost'))
            purchase_object.save()
            time_object = TimeForClass(classroot=class_root_object,
                                       time_of_day=time_form.cleaned_data.get('time_of_day'),
                                       date=time_form.cleaned_data.get('date'))
            time_object.save()
            stream_object = ClassStreamInfo(classroot=class_root_object, max_number_of_viewers=stream_form.cleaned_data.get('max_number_of_viewers'), stream_time=time_object)
            stream_object.save()
            messages.success(self.request,
                             f'You have made a free stream')
            return redirect('home')
        else:
            print("failed")

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
    def post(self, request, *args, **kwargs):
        class_root_form = ClassRootCreate(request.POST, prefix='class_form')
        purchase_form = CreatePurchaseInfo(request.POST, prefix='purchase_form')
        time_form = CreateTimeForClass(request.POST, prefix='time_form')
        if class_root_form.is_valid() and time_form.is_valid() and purchase_form.is_valid():
            class_root_object = ClassRoot(title=class_root_form.cleaned_data.get('title'), content=class_root_form.cleaned_data.get('content'), author=self.request.user, author_profile=self.request.user.profile,
                                            category=class_root_form.cleaned_data.get('category'), is_purchase=True, is_one_on_one=True, is_stream=False, is_video=False)
            class_root_object.save()
            purchase_object = ClassPurchaseInfo(classroot=class_root_object, cost=purchase_form.cleaned_data.get('cost'))
            purchase_object.save()
            time_object = TimeForClass(classroot=class_root_object,
                                       time_of_day=time_form.cleaned_data.get('time_of_day'),
                                       date=time_form.cleaned_data.get('date'))
            time_object.save()
            messages.success(self.request,
                             f'You have made a free stream')
            return redirect('home')
        else:
            print("failed")

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
    def post(self, request, *args, **kwargs):
        class_root_form = ClassRootCreate(request.POST, prefix='class_form')
        purchase_form = CreatePurchaseInfo(request.POST, prefix='purchase_form')
        video_form = CreateVideoInfo(request.POST, request.FILES, prefix='video_form')
        if class_root_form.is_valid() and video_form.is_valid() and purchase_form.is_valid():
            class_root_object = ClassRoot(title=class_root_form.cleaned_data.get('title'), content=class_root_form.cleaned_data.get('content'), author=self.request.user, author_profile=self.request.user.profile,
                                            category=class_root_form.cleaned_data.get('category'), is_purchase=True, is_one_on_one=False, is_stream=False, is_video=True)
            class_root_object.save()
            purchase_object = ClassPurchaseInfo(classroot=class_root_object, cost=purchase_form.cleaned_data.get('cost'))
            purchase_object.save()
            video_object = ClassVideoInfo(classroot=class_root_object, video_name=video_form.cleaned_data.get('video_name'), video_file=video_form.cleaned_data.get('video_file'))
            video_object.save()
            messages.success(self.request,
                             f'You have made a free stream')
            return redirect('home')
        else:
            print("failed")

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