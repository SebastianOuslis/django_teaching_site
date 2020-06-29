from django.urls import path
from .views import (
    PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CategoryPostListView, ReviewCreateView, UserReviewList, VideoView_payed, VideoView_free, TextChatView, ClassTypeListView, ClassVideoView, PostSalesView, OneOnOneVideoAgora, FollowingListView
    )
from .views import (
    set_video_call_start, set_video_call_end, validate_video_call, add_following
    )
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('following/', FollowingListView.as_view(), name='following'),
    path('category/<str:category>', CategoryPostListView.as_view(), name='post-category'),
    path('classType/<str:type>', ClassTypeListView.as_view(), name='class-type'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/sales/<int:pk>/', PostSalesView.as_view(), name='post-sales'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('classvideo/<int:pk>/', ClassVideoView.as_view(), name='class-video'),
    path('review/create/<str:username>', ReviewCreateView.as_view(success_url=reverse_lazy('blog-home')), name='create-review'),
    path('review/<str:username>', UserReviewList.as_view(), name='user-review'),
    path('video/<str:classTitle>/<str:username>', VideoView_payed.as_view(), name='video-call'),
    path('agora_video/', OneOnOneVideoAgora.as_view(), name='agora-video' ),
    path('open_video/<str:classTitle>', VideoView_free.as_view(), name='open-video-call'),
    path('chat/<str:username>', TextChatView.as_view(), name='text-chat'),
    path('about/', views.about, name='blog-about'),
    path('ajax/start_call/', set_video_call_start, name='start_call'),
    path('ajax/end_call/', set_video_call_end, name='end_call'),
    path('ajax/check_call/', validate_video_call, name='check_call'),
    path('ajax/add_following/', add_following, name='add_following'),

]
