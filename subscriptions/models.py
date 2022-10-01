
from datetime import datetime
from email.policy import default
import json
from select import select
from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from hitcount.views import HitCountDetailView
from hitcount.models import HitCountMixin, HitCount
#from phonenumber_field.modelfields import PhoneNumberField




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
    #phoneNum = PhoneNumberField()
    published = models.BooleanField(default=False)
    prev_img = models.ImageField(upload_to = "uploads/")
    def __str__(self):
        return self.headline
    class Meta:
        verbose_name = 'Article'

class PostCountHitDetailView(HitCountDetailView):
    model = formforsubmit        # your model goes here
    count_hit = True   

#send a mail to the user when the article is published

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = RichTextField(blank=True,null=True)
    fromAdmin = models.BooleanField(default=True)
    seenByAdmin = models.BooleanField(default=True)
    seenByUser = models.BooleanField(default=True)
    timeSent = models.DateTimeField(default=datetime.now())
    class Meta:
        verbose_name = 'Mail'

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seenByUser = models.BooleanField(default=False)
    seenByAdmin = models.BooleanField(default=False)
    def __str__(self):
        return(self.user.email)

#class to get ip address of the user and store it in the database
class IpAddress(models.Model):
    #use django hitcount
    ip = models.CharField(max_length=255)
    def __str__(self):
        return self.ip


        
class responsefromuser(models.Model):
    #use user and article as foreign keys to get the response from the user
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    article = models.ForeignKey(formforsubmit, on_delete = models.CASCADE)
    response = RichTextField(blank=True,null=True)

    def __str__(self):
        return self.response
    class Meta:
        verbose_name = 'Response'
        


class task(models.Model):
    #assign one task for multiple users
    #select multiple users from the admin panel and assign them a task

    user = models.ManyToManyField(User)
    task = models.CharField(max_length = 255)
    task_description = models.CharField(max_length = 255)
    taskstatus = models.BooleanField(default=False)
    task_date = models.DateTimeField()
    
    def __str__(self):
        return self.task

    def __str__(self):
        return self.task
    class Meta:
        verbose_name = 'Task'

class tasksubmissions(models.Model):
    # view all the responses from the users for a particular task
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.ForeignKey(task, on_delete = models.CASCADE)
    response = RichTextField(blank=True,null=True)
    proof = models.ImageField(upload_to='proofs/',blank=True,null=True)

    completed_on = models.DateTimeField(default=datetime.now())
    

    def __str__(self):
        return self.response
    class Meta:
        verbose_name = 'Task Response'
        