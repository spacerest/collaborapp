from django import forms
from django.forms import ModelForm
from postoffice.models import Envelope, TextMessage, ImageMessage, PdfMessage

class EnvelopeReceiver(ModelForm):
    class Meta:
        model = Envelope 
        fields = ('primary_key',)

class NewEnvelope(ModelForm):
    class Meta:
        model = Envelope 
        fields = ('primary_key', 'sender_name', 'recipient_name', )

class NewTextMessage(ModelForm):
    class Meta:
        model = TextMessage
        fields = ('message', ) 

class NewImageMessage(ModelForm):
    class Meta:
        model = ImageMessage
        fields = ('image', ) 

class NewPdfMessage(ModelForm):
    class Meta:
        model = PdfMessage
        fields = ('pdf_file', ) 



class StringLocker(forms.Form):
    user_prompt = forms.CharField(label='Set a passcode reminder')
    symmetric_key = forms.CharField(label='Set a passcode')

class StringUnlocker(forms.Form):
    symmetric_key = forms.CharField(label='Passcode')
