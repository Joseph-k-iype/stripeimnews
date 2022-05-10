from django.contrib import admin

# Register your models here.
from subscriptions.models import StripeCustomer, formforsubmit, sendmail

class formadmin(admin.ModelAdmin):
    search_fields = ['user', 'headline']
    list_display = ['user', 'headline']
    list_filter = ['user', 'headline']


admin.site.register(StripeCustomer)
admin.site.register(formforsubmit, formadmin)
admin.site.register(sendmail)

