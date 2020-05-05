from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic    import TemplateView
from .models import Purchases, StripeInteractions
from blog.models import Post
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
        page_post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        context['page_user'] = page_user
        context['user'] = self.request.user
        context['post_purchased'] = page_post
        context['stripe_description'] = page_post.title
        context['stripe_charge'] = str(int(page_post.cost*100))
        context['stripe_charge_dollars'] = context['stripe_charge'][:-2]
        context['stripe_charge_cents'] = context['stripe_charge'][-2:]
        return context

    def post(self, request, *args, **kwards):
        context = self.get_context_data(self, *args, **kwards)
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