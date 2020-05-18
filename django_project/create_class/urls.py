from django.urls import path
from .views import CreateClassStepOne, CreateClassStreamNoPay, CreateClassStreamPay, CreateClassOneToOnePay, CreateClassVideoPay
from django.urls import reverse_lazy

urlpatterns = [
    path('', CreateClassStepOne.as_view(template_name='create_class/create_class_step_one.html'), name='create_class_step_one'),
    path('stream_choose_pay', CreateClassStepOne.as_view(template_name='create_class/stream_choose_pay.html'), name='stream_choose_pay'),
    path('create_stream_pay', CreateClassStreamPay.as_view(template_name='create_class/create_stream_pay.html'), name='create_stream_pay'),
    path('create_stream_no_pay', CreateClassStreamNoPay.as_view(template_name='create_class/create_stream_no_pay.html'), name='create_stream_no_pay'),
    path('create_one_on_one', CreateClassOneToOnePay.as_view(template_name='create_class/create_one_on_one_pay.html'),
         name='create_one_on_one'),
    path('create_video', CreateClassVideoPay.as_view(template_name='create_class/create_video_pay.html'),
         name='create_video'),
]
