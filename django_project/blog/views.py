from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
    )
from django.contrib.auth.models import User
from .models import Category, Post, Review, ClassRoot, ClassPurchaseInfo, ClassOneOnOneInfo, ClassStreamInfo, ClassVideoInfo, TimeForClass
from django.conf import settings
from users.models import Profile, ListOfInstructors
from django.contrib import messages

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# def home(request):
#     context = {
#         'classes': ClassRoot.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

class HomeView(ListView):
    model = ClassRoot
    template_name = 'blog/home.html'
    context_object_name = 'classes'
    ordering = ['-date_posted']
    paginate_by = 5

class PostListView(ListView):
    model = ClassRoot
    template_name = 'blog/home.html'
    context_object_name = 'classes'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = ClassRoot
    template_name = 'blog/user_posts.html'
    context_object_name = 'classes'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return ClassRoot.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['page_user'] = page_user
        return context

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.kwargs.get('username') in list_of_instructor_usernames:
            return True
        return False

    def handle_no_permission(self):
        return redirect('home')

class CategoryPostListView(ListView):
    model = ClassRoot
    template_name = 'blog/category_posts.html'
    context_object_name = 'classes'
    paginate_by = 5

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return ClassRoot.objects.filter(category=category).order_by('-date_posted')

class ClassTypeListView(ListView):
    model = ClassRoot
    template_name = 'blog/class_types.html'
    context_object_name = 'classes'
    paginate_by = 5

    def get_queryset(self):
        class_type = self.kwargs.get('type')
        if class_type == 'one_on_one':
            return ClassRoot.objects.filter(is_one_on_one=True).order_by('-date_posted')
        elif class_type == 'stream':
            return ClassRoot.objects.filter(is_stream=True).order_by('-date_posted')
        elif class_type == 'video':
            return ClassRoot.objects.filter(is_video=True).order_by('-date_posted')
        else:
            return redirect('home')

class PostDetailView(DetailView):
    model = ClassRoot
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_root_object = self.object
        if class_root_object.is_purchase:
            purchase_info = get_object_or_404(ClassPurchaseInfo, classroot=class_root_object)
            charge = str(int(purchase_info.cost * 100))
            dollars_of_charge = charge[:-2]
            cents_of_charge = charge[-2:]
            context['key'] = settings.STRIPE_PUBLISHABLE_KEY
            context['stripe_description'] = str(class_root_object.title)+" by "+str(class_root_object.author.username)
            context['stripe_charge'] = charge
            context['stripe_charge_dollars'] = dollars_of_charge
            context['stripe_charge_cents'] = cents_of_charge
            context['stripe_locale'] = 'auto'
        if class_root_object.is_one_on_one:
            one_on_one_info = get_object_or_404(ClassOneOnOneInfo, classroot=class_root_object)
            time_info = get_object_or_404(TimeForClass, classroot=class_root_object)
            context["class_date"] = str(time_info.date)
            context["class_time"] = str(time_info.time_of_day)
        if class_root_object.is_stream:
            stream_info = get_object_or_404(ClassStreamInfo, classroot=class_root_object)
            time_info = get_object_or_404(TimeForClass, classroot=class_root_object)
            context["class_date"] = str(time_info.date)
            context["class_time"] = str(time_info.time_of_day)
        if class_root_object.is_video:
            video_info = get_object_or_404(ClassVideoInfo, classroot=class_root_object)
            context["video_name"] = video_info.video_name
        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super(DetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'is_purchase', 'type_of_class', 'initial_spots', 'cost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        list_of_instructor_usernames = [d['user_username'] for d in list(ListOfInstructors.objects.values('user_username')) if 'user_username' in d]
        if self.request.user.username in list_of_instructor_usernames:
            return True
        messages.warning(self.request, f'You must be an instructor to create a class, please contact us to make you an instructor')
        return False

    def handle_no_permission(self):
        return redirect('blog-home')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'is_purchase', 'type_of_class', 'initial_spots', 'cost']
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    # def handle_no_permission(self):
    #     return redirect('users:create-profile')
    # this is to redirect after no permission, add message " messages.success(request, 'Form submission successful') "

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

class UserReviewList(ListView):
    model = Review
    template_name = 'blog/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['page_user'] = page_user
        return context

    def get_queryset(self):
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(user_being_reviewed=page_user).order_by('-date_posted')


class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    fields = ['user_rating_out_of_five', 'review_text']
    template_name = 'blog/user_create_review.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_to_review = get_object_or_404(User, username=self.kwargs.get('username'))
        context['user_to_review'] = user_to_review
        return context

    def test_func(self):
        if self.request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return False
        return True

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user_being_reviewed = get_object_or_404(User, username=self.kwargs.get('username'))
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect('profile')


#video calling stuffs

class VideoView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'blog/user_video.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['page_user'] = page_user
        context['user'] = self.request.user
        return context

    def test_func(self):
        if self.request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return False
        return True

    def handle_no_permission(self):
        return redirect('profile')

class TextChatView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'blog/user_chat.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['page_user'] = page_user
        context['user'] = self.request.user
        return context

    def test_func(self):
        if self.request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return False
        return True

    def handle_no_permission(self):
        return redirect('profile')