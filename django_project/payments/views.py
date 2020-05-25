from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic    import TemplateView
from .models import Purchases, StripeInteractions
from blog.models import Post, ClassPurchaseInfo, ClassRoot
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    charge = '500'
    dollars_of_charge = charge[:-2]
    cents_of_charge = charge[-2:]
    context = {
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_description': 'A Django Charge',
        'stripe_charge': charge,
        'stripe_charge_dollars': dollars_of_charge,
        'stripe_charge_cents': cents_of_charge,
        'stripe_locale': 'auto'
    }
    return render(request, 'payments/home.html', context)

class ChargeClass(LoginRequiredMixin, TemplateView):
    template_name = 'payments/charge.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        print(self.kwargs.get('username'))
        page_user = get_object_or_404(User, username=self.kwargs.get('username'))
        class_object = get_object_or_404(ClassRoot, id=self.kwargs.get('pk'))
        purchase_info = get_object_or_404(ClassPurchaseInfo, classroot=class_object)
        context['page_user'] = page_user
        context['user'] = self.request.user
        context['post_purchased'] = class_object
        context['stripe_description'] = class_object.title
        context['stripe_charge'] = str(int(purchase_info.cost*100))
        context['stripe_charge_dollars'] = context['stripe_charge'][:-2]
        context['stripe_charge_cents'] = context['stripe_charge'][-2:]
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(self, *args, **kwargs)
        stripe_charge = stripe.Charge.create(
            amount=int(context['stripe_charge']),
            currency='usd',
            description=context['stripe_description'],
            source=request.POST['stripeToken']
        )
        stripe_interaction = StripeInteractions(bought_by_username=context['user'].username, bought_from_username=context['page_user'].username, stripe_data=str(stripe_charge), post_bought_from_title=context['post_purchased'].title)
        stripe_interaction.save()
        if stripe_charge["paid"] == True:
            purchase = Purchases(user_bought_by=context['user'], user_bought_from=context['page_user'], price_in_cents=stripe_charge['amount'], post_bought_from=context['post_purchased'], currency=stripe_charge['currency'])
            purchase.save()
            return render(request, 'payments/charge.html', context)
        else:
            return render(request, 'payments/charge_failure.html', context)