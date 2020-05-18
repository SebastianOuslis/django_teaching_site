from django.urls import path
from .views import ChargeClass, home

urlpatterns = [
    path('charge/<str:username>/<int:pk>', ChargeClass.as_view(), name='payments-charge'),
]