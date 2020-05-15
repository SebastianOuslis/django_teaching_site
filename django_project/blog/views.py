from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
    )
from django.contrib.auth.models import User
from .models import Category, Post, Review
from django.conf import settings
from users.models import Profile

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['page_user'] = page_user
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return Post.objects.filter(category=category).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        post_object = self.object
        if post_object.is_purchase:
            charge = str(int(post_object.cost * 100))
            dollars_of_charge = charge[:-2]
            cents_of_charge = charge[-2:]
            context['key'] = settings.STRIPE_PUBLISHABLE_KEY
            context['stripe_description'] = 'A Django Charge'
            context['stripe_charge'] = charge
            context['stripe_charge_dollars'] = dollars_of_charge
            context['stripe_charge_cents'] = cents_of_charge
            context['stripe_locale'] = 'auto'
        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super(DetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'is_purchase', 'type_of_class', 'initial_spots', 'cost']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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