from django.urls import path
from .views import (
    PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CategoryPostListView, ReviewCreateView, UserReviewList, VideoView, TextChatView, ClassTypeListView, ClassVideoView
    )
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('category/<str:category>', CategoryPostListView.as_view(), name='post-category'),
    path('classType/<str:type>', ClassTypeListView.as_view(), name='class-type'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('classvideo/<int:pk>/', ClassVideoView.as_view(), name='class-video'),
    path('review/create/<str:username>', ReviewCreateView.as_view(success_url=reverse_lazy('blog-home')), name='create-review'),
    path('review/<str:username>', UserReviewList.as_view(), name='user-review'),
    path('video/<str:username>', VideoView.as_view(), name='video-call'),
    path('chat/<str:username>', TextChatView.as_view(), name='text-chat'),
    path('about/', views.about, name='blog-about'),

]
