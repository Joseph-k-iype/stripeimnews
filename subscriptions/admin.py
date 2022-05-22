from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from subscriptions.models import  Conversation, StripeCustomer, formforsubmit, sendmail, IpAddress, tasksforoperations

class formadmin(admin.ModelAdmin):
    search_fields = ['user', 'headline']
    list_display = ['user', 'headline']
    list_filter = ['user', 'headline']


admin.site.register(StripeCustomer)
admin.site.register(formforsubmit, formadmin)
admin.site.register(Conversation)
admin.site.register(IpAddress)
admin.site.register(sendmail)


admin.site.register(tasksforoperations)