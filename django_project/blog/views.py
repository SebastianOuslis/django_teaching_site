from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
    )
from django.contrib.auth.models import User
from .models import Category, Post, Review, ClassRoot, ClassPurchaseInfo, ClassOneOnOneInfo, ClassStreamInfo, ClassVideoInfo, TimeForClass
from django.conf import settings
from users.models import Profile, ListOfInstructors
from payments.models import Purchases
from django.contrib import messages
from create_class.forms import ClassRootCreate, CreateTimeForClass, CreatePurchaseInfo, CreateStreamInfo, CreateVideoInfo
from django.http import HttpResponseRedirect
from django.http import JsonResponse

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# def home(request):
#     context = {
#         'classes': ClassRoot.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

class HomeView(ListView):
    model = ClassRoot
    template_name = 'blog/newhome.html'

class PostListView(ListView):
    model = ClassRoot
    template_name = 'blog/classes_list.html'
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
        if self.request.user.is_authenticated:
            list_of_titles = [d.post_bought_from_title for d in
                                            list(Purchases.objects.filter(user_bought_by=self.request.user)) if
                                            'post_bought_from_title' in d]
            if self.request.user == class_root_object.author or class_root_object.title in list_of_titles:
                context['purchased_or_is_author'] = True
            else:
                context['purchased_or_is_author'] = False
        else:
            context['purchased_or_is_author'] = False
        context['user_who_purchased'] = self.object.author
        if class_root_object.is_purchase:
            purchase_info = get_object_or_404(ClassPurchaseInfo, classroot=class_root_object)
            if len(list(Purchases.objects.filter(post_bought_from=class_root_object))) > 0:
                context['has_not_been_purchased'] = False
                context['user_who_purchased'] = (list(Purchases.objects.filter(post_bought_from=class_root_object))[0]).user_bought_by
            else:
                context['has_not_been_purchased'] = True
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

class PostSalesView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClassRoot
    template_name = 'blog/post_sales.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_root_object = self.object
        context['list_of_buyers'] = [{'date_bought': d.date_bought, 'user_bought_by_full_name': d.user_bought_by.profile.full_name, 'user_bought_by_email': d.user_bought_by.email} for d in
                              list(Purchases.objects.filter(post_bought_from=class_root_object))]
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

    def handle_no_permission(self):
        return redirect('home')

    def test_func(self):
        class_object = get_object_or_404(ClassRoot, pk=self.kwargs.get('pk'))
        if class_object.is_purchase == False:
            return False
        if self.request.user == class_object.author:
            return True
        return False

# not used anymore
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

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'blog/post_update.html'

    def post(self, request, *args, **kwargs):
        class_root_object = get_object_or_404(ClassRoot, id=self.kwargs.get('pk'))
        class_root_form = ClassRootCreate(request.POST, prefix='class_form', instance=class_root_object)
        forms = []
        forms.append(class_root_form)
        if class_root_object.is_purchase:
            forms.append(CreatePurchaseInfo(request.POST, prefix='purchase_form', instance=get_object_or_404(ClassPurchaseInfo, classroot=class_root_object)))
        if class_root_object.is_one_on_one:
            forms.append(CreateTimeForClass(request.POST, prefix='time_form', instance=get_object_or_404(TimeForClass, classroot=class_root_object)))
        if class_root_object.is_stream:
            forms.append(CreateStreamInfo(request.POST, prefix='stream_form', instance=get_object_or_404(ClassStreamInfo, classroot=class_root_object)))
            forms.append(CreateTimeForClass(request.POST, prefix='time_form', instance=get_object_or_404(TimeForClass, classroot=class_root_object)))
        if class_root_object.is_video:
            video_info = get_object_or_404(ClassVideoInfo, classroot=class_root_object)
            forms.append(CreateVideoInfo(request.POST, prefix='video_form', instance=get_object_or_404(ClassVideoInfo, classroot=class_root_object)))
        success_flag = True
        for form in forms:
            if not form.is_valid() and success_flag:
                messages.warning(self.request,
                                 f'You failed to update the class with the following errors: {form.errors}')
                return HttpResponseRedirect(self.request.path_info)
                success_flag = False
        if success_flag:
            for form in forms:
                form.save()
            messages.success(self.request,
                             f'You have updated the class')
            return redirect('home')
        else:
            print("failed")
            return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_root_object = get_object_or_404(ClassRoot, id=self.kwargs.get('pk'))
        forms = []
        forms.append(ClassRootCreate(None, prefix='class_form', instance=class_root_object))
        if class_root_object.is_purchase:
            purchase_info = get_object_or_404(ClassPurchaseInfo, classroot=class_root_object)
            forms.append(CreatePurchaseInfo(None, prefix='purchase_form', instance=purchase_info))
        if class_root_object.is_one_on_one:
            time_info = get_object_or_404(TimeForClass, classroot=class_root_object)
            forms.append(CreateTimeForClass(None, prefix='time_form', instance=time_info))
        if class_root_object.is_stream:
            stream_info = get_object_or_404(ClassStreamInfo, classroot=class_root_object)
            time_info = get_object_or_404(TimeForClass, classroot=class_root_object)
            forms.append(CreateStreamInfo(None, prefix='stream_form', instance=stream_info))
            forms.append(CreateTimeForClass(None, prefix='time_form', instance=time_info))
        if class_root_object.is_video:
            video_info = get_object_or_404(ClassVideoInfo, classroot=class_root_object)
            forms.append(CreateVideoInfo(None, prefix='video_form', instance=video_info))
        context["forms"] = forms
        return context

    def test_func(self):
        class_root_object = get_object_or_404(ClassRoot, id=self.kwargs.get('pk'))
        if self.request.user == get_object_or_404(User, username=class_root_object.author.username):
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect('home')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClassRoot
    success_url = '/blog'

    def test_func(self):
        class_object = self.get_object()
        if self.request.user == class_object.author:
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


class ClassVideoView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClassRoot
    template_name = 'blog/watch_video_class.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        class_root_object = class_object = get_object_or_404(ClassRoot, id=self.kwargs.get('pk'))
        context['class_root_object'] = class_root_object
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
            context["video_file"] = video_info.video_file
        return context

    def get_object(self):
        return get_object_or_404(ClassRoot, id=self.kwargs['pk'])

    def test_func(self):
        class_object = get_object_or_404(ClassRoot, id=self.kwargs.get('pk'))
        if class_object.is_video:
            if not class_object.is_purchase:
                return True
            if self.request.user == get_object_or_404(User, username=class_object.author.username):
                return True
            list_of_titles = [d.post_bought_from_title for d in
                                            list(Purchases.objects.filter(user_bought_by=self.request.user)) if
                                            'post_bought_from_title' in d]
            if class_object.title in list_of_titles:
                return True
            else:
                messages.warning(self.request,
                                 f'Please pay for the class and you can view this video')
                return False
        else:
            return False

    def handle_no_permission(self):
        return redirect('home')


#video calling stuffs

class VideoView_payed(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'blog/user_video.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['page_user'] = page_user
        context['user'] = self.request.user
        context['class_object'] = get_object_or_404(ClassRoot, title=self.kwargs.get('classTitle'))
        context['title'] = self.kwargs.get('classTitle')
        return context

    def test_func(self):
        if self.request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return False
        return True

    def handle_no_permission(self):
        return redirect('profile')

class VideoView_free(LoginRequiredMixin, TemplateView):
    template_name = 'blog/open_video_call.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_object'] = get_object_or_404(ClassRoot, title=self.kwargs.get('classTitle'))
        context['title'] = self.kwargs.get('classTitle')
        context['page_user'] = context['class_object'].author
        context['user'] = self.request.user
        return context

    def handle_no_permission(self):
        return redirect('home')

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


class OneOnOneVideoAgora(LoginRequiredMixin, TemplateView):
    template_name = 'blog/agora_video_chat.html'


### ajaxs
def set_video_call_start(request):
    pk_for_classroot = request.GET.get('pk', None)
    ClassOneOnOneInfo.objects.filter(classroot=get_object_or_404(ClassRoot, id=pk_for_classroot)).update(started=True)
    messages.success(request,
                     f'You have started the video class')
    data = {
        'pk_for_class': pk_for_classroot
    }
    return JsonResponse(data)


def set_video_call_end(request):
    pk_for_classroot = request.GET.get('pk', None)
    ClassOneOnOneInfo.objects.filter(classroot=get_object_or_404(ClassRoot, id=pk_for_classroot)).update(started=False)
    messages.success(request,
                     f'You have ended the video class')
    data = {
        'pk_for_class': pk_for_classroot
    }
    return JsonResponse(data)


def validate_video_call(request):
    pk_for_classroot = request.GET.get('pk', None)
    data = {
        'is_started': ClassOneOnOneInfo.objects.filter(classroot=get_object_or_404(ClassRoot, id=pk_for_classroot), started=True).exists()
    }
    if not data['is_started']:
        messages.success(request, f'The One on One class has not started yet, or the instructor has ended the class. If something went wrong, please contact admin@nxtklass.com')
    return JsonResponse(data)