from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

class Purchases(models.Model):
    user_bought_by = models.ForeignKey(User, related_name='Purchases_bought_by', null=True, default=None, on_delete=models.SET_DEFAULT)
    user_bought_from = models.ForeignKey(User, related_name='Purchases_sold_by', null=True, default=None, on_delete=models.SET_DEFAULT)
    user_bought_by_username = models.TextField(default='someone')
    user_bought_from_username = models.TextField(default='someone')
    price_in_cents = models.IntegerField()
    dollars_string = models.TextField(default='0')
    cents_string = models.TextField(default='00')
    date_bought = models.DateTimeField(default=timezone.now)
    post_bought_from = models.ForeignKey(Post, related_name='Item_bought', null=True, default=None, on_delete=models.SET_DEFAULT)
    post_bought_from_title = models.TextField(default='class title')
    currency = models.CharField(max_length=5)

    def save(self, *args, **kwargs):
        if self.price_in_cents > 99:
            self.dollars_string = str(self.price_in_cents)[:-2]
            self.cents_string = str(self.price_in_cents)[-2:]
        else:
            self.dollars_string = '0'
            self.cents_string = str(self.price_in_cents+100)[-2:]
        if self.user_bought_by is not None:
            self.user_bought_by_username = self.user_bought_by.username
        if self.user_bought_from is not None:
            self.user_bought_from_username = self.user_bought_from.username
        if self.post_bought_from is not None:
            self.post_bought_from_title = self.post_bought_from.title
        super(Purchases, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_bought_by_username + " bought something for " + str(self.dollars_string) + "." + str(self.cents_string) + self.currency + " from " + self.user_bought_from_username

class StripeInteractions(models.Model):
    bought_by_username = models.TextField()
    bought_from_username = models.TextField()
    stripe_data = models.TextField()
    date_bought = models.DateTimeField(default=timezone.now)
    post_bought_from_title = models.TextField()