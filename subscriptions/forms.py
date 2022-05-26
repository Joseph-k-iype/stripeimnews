#form data for posting a new article
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

class submitform(forms.ModelForm):
    #form for a particular user
    headline = forms.CharField(
            widget=forms.widgets.Textarea(
                attrs={'style': 'height:10px',
                    'class':'form-control mb-5'
                }
            )
        )
    summary = forms.CharField(
            widget=forms.widgets.Textarea(
                attrs={'style': 'height:10px',
                    'class':'form-control mb-5'
                }
            )
        )
    article = forms.CharField(
        widget=forms.widgets.Textarea(
                attrs={
                    'class':'form-control area_1'
                }
            )

    )
    schedule = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(
            format='%Y-%m-%d %H:%M:%S',
            attrs={'type': 'datetime-local',
                'class':'form-control date'
            }
        )
    )
  
    class Meta:
        model = formforsubmit
        fields = ['headline', 'summary', 'article', 'schedule']
        

        widgets = {
            'article': CKEditorWidget(),
            'schedule': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'type': 'datetime-local',
                'class':'form-control time'
                },
                
            ),
            
            
        }

#form for sending a mail to the user
class sendmailform(forms.ModelForm):
    class Meta:
        model = sendmail
        fields = ['message']
        widgets = {
            'message': CKEditorWidget(),
        }
        