from django import forms
from django.forms import ModelForm
from postoffice.models import Letter

class LetterReceiver(ModelForm):
    private_key = forms.CharField(max_length=10, help_text='your key to receive')

    class Meta:
        model = Letter 
        fields = ('private_key',)
