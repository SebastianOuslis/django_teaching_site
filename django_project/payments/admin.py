from django.contrib import admin
from .models import Purchases, StripeInteractions

admin.site.register(Purchases)
admin.site.register(StripeInteractions)
