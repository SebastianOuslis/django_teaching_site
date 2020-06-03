from django.urls import path
from .views import CreateClassStepOne, CreateClassStreamNoPay, CreateClassStreamPay, CreateClassOneToOnePay, CreateClassVideoPay, CreateClassVideoNoPay, CreateClassOneToOneNoPay
from django.urls import reverse_lazy

urlpatterns = [
    path('', CreateClassStepOne.as_view(template_name='create_class/create_class_step_one.html'), name='create_class_step_one'),
    path('stream_choose_pay', CreateClassStepOne.as_view(template_name='create_class/stream_choose_pay.html'), name='stream_choose_pay'),
    path('one_on_one_choose_pay', CreateClassStepOne.as_view(template_name='create_class/one_on_one_choose_pay.html'), name='one_on_one_choose_pay'),
    path('video_choose_pay', CreateClassStepOne.as_view(template_name='create_class/video_choose_pay.html'), name='video_choose_pay'),
    path('create_stream_pay', CreateClassStreamPay.as_view(template_name='create_class/create_stream_pay.html'), name='create_stream_pay'),
    path('create_stream_no_pay', CreateClassStreamNoPay.as_view(template_name='create_class/create_stream_no_pay.html'), name='create_stream_no_pay'),
    path('create_one_on_one_pay', CreateClassOneToOnePay.as_view(template_name='create_class/create_one_on_one_pay.html'),
         name='create_one_on_one_pay'),
    path('create_one_on_one_no_pay', CreateClassOneToOneNoPay.as_view(template_name='create_class/create_one_on_one_no_pay.html'),
         name='create_one_on_one_no_pay'),
    path('create_video_pay', CreateClassVideoPay.as_view(template_name='create_class/create_video_pay.html'),
         name='create_video_pay'),
    path('create_video_no_pay', CreateClassVideoNoPay.as_view(template_name='create_class/create_video_no_pay.html'),
         name='create_video_no_pay'),
]
