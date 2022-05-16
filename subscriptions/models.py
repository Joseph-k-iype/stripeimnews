
import json
from msvcrt import getch
from pyexpat import model
from select import select
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from hitcount.views import HitCountDetailView


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class formforsubmit(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    headline = models.CharField(max_length = 255)
    summary = models.CharField(max_length = 500)
    article = RichTextField(blank=True,null=True)
    schedule = models.DateTimeField()

    def __str__(self):
        return self.headline
    class Meta:
        verbose_name = 'Article'

class PostCountHitDetailView(HitCountDetailView):
    model = formforsubmit        # your model goes here
    count_hit = True   

#send a mail to the user when the article is published

class sendmail(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = RichTextField(blank=True,null=True)
    fromAdmin = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Mail'

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view = models.BooleanField(default=False) # True if message is not seen by admin
    def __str__(self):
        return(self.user.email)

        
class responsefromuser(models.Model):
    #use user and article as foreign keys to get the response from the user
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    article = models.ForeignKey(formforsubmit, on_delete = models.CASCADE)
    response = RichTextField(blank=True,null=True)

    def __str__(self):
        return self.response
    class Meta:
        verbose_name = 'Response'
        