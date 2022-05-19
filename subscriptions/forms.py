#form data for posting a new article
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *


class submitform(forms.ModelForm):
    #form for a particular user
    class Meta:
        model = formforsubmit
        fields = ['headline', 'summary', 'article', 'schedule', 'prev_img']
        widgets = {
            'article': CKEditorWidget(),
            'schedule': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'type': 'datetime-local'}
            )
        }

#form for sending a mail to the user
class sendmailform(forms.ModelForm):
    class Meta:
        model = sendmail
        fields = ['message']
        widgets = {
            'message': CKEditorWidget(),
        }
        