from django import forms
from django.forms import ModelForm
from postoffice.models import Envelope, EncryptedStringObject

class EnvelopeReceiver(ModelForm):
    class Meta:
        model = Envelope 
        fields = ('primary_key',)

class NewEnvelope(ModelForm):
    class Meta:
        model = Envelope 
        fields = ('primary_key', 'sender_name', 'recipient_name', )

class NewEncryptedStringObject(ModelForm):
    class Meta:
        model = EncryptedStringObject
        fields = ('message', ) 

class StringLocker(forms.Form):
    user_prompt = forms.CharField(label='Set a passcode reminder')
    symmetric_key = forms.CharField(label='Set a passcode')

class StringUnlocker(forms.Form):
    symmetric_key = forms.CharField(label='Passcode')
