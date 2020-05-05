from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

class Purchases(models.Model):
    user_bought_by = models.ForeignKey(User, related_name='Purchases_bought_by', null=True, default=None, on_delete=models.SET_DEFAULT)
    user_bought_from = models.ForeignKey(User, related_name='Purchases_sold_by', null=True, default=None, on_delete=models.SET_DEFAULT)
    price_in_cents = models.IntegerField()
    dollars_string = models.TextField(default='0')
    cents_string = models.TextField(default='00')
    date_bought = models.DateTimeField(default=timezone.now)
    post_bought_from = models.ForeignKey(Post, related_name='Item_bought', null=True, default=None, on_delete=models.SET_DEFAULT)
    currency = models.CharField(max_length=5)

    def save(self, *args, **kwargs):
        if self.price_in_cents > 99:
            self.dollars_string = str(self.price_in_cents)[:-2]
            self.cents_string = str(self.price_in_cents)[-2:]
        else:
            self.dollars_string = '0'
            self.cents_string = str(self.price_in_cents+100)[-2:]
        super(Purchases, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_bought_by.username + " bought something for " + str(self.price_in_cents/100) + "$ from " + self.user_bought_from.username

class StripeInteractions(models.Model):
    bought_by_username = models.TextField()
    bought_from_username = models.TextField()
    stripe_data = models.TextField()
    date_bought = models.DateTimeField(default=timezone.now)
    post_bought_from_title = models.TextField()