from django.shortcuts import render, redirect
from postoffice.forms import EnvelopeReceiver, StringLocker, StringUnlocker, NewEncryptedStringObject, NewEnvelope
from postoffice.models import Envelope, EncryptionType, EncryptedStringObject
from postoffice import utilities
# Create your views here.

def home(request):
    return render(request, 'postoffice/home.html')

def lookup_envelope(primary_key):
    envelope_object_list = Envelope.objects.filter(primary_key=primary_key)
    if envelope_object_list:
        print(envelope_object_list)
        return envelope_object_list[0]
    else:
        return False

def delete_item(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    envelope_object.delete()
    return redirect('postoffice_home')

def new_item(request):
    if request.method == "POST":
        envelope_form = NewEnvelope(request.POST)
        message_form = NewEncryptedStringObject(request.POST)
        if message_form.is_valid() and envelope_form.is_valid():
            #for now, only letting fernet_string encryption be an option
            encryption_type = EncryptionType.objects.filter(name="fernet_string")[0]
            print(encryption_type)
            envelope = envelope_form.save(commit=False)
            message = message_form.save(commit=False)
            message.encryption_type = encryption_type
            print(message.encryption_type)
            message.save()
            envelope.encrypted_string_object = message
            envelope.save()
            return redirect('postoffice_encrypt', envelope.primary_key)
    data = {'envelope_form': envelope_form, 'message_form': message_form}
    return render(request, 'postoffice/outbox.html', data)

def send_envelope(request):
    envelope_form = NewEnvelope()
    message_form = NewEncryptedStringObject()
    data = {"envelope_form": envelope_form, "message_form": message_form}
    return render(request, 'postoffice/outbox.html', data)

def find_envelope(request, primary_key=None):
    if not primary_key:
        envelope_object = lookup_envelope(request.GET.get("primary_key", False))
        data = {'envelope': envelope_object}
    form = EnvelopeReceiver()
    data['form'] = form
    return render(request, 'postoffice/inbox.html', data)

#todo research sending symmetric key in cleartext
def encrypt(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    if envelope_object:
        if request.method == "POST":
            form = StringLocker(request.POST)
            symmetric_key = form["symmetric_key"].value()
            user_prompt = form["user_prompt"].value()
            envelope_object.user_prompt = user_prompt
            encrypted_message = utilities.encrypt_string(symmetric_key, envelope_object.encrypted_string_object.message)
            envelope_object.encrypted_string_object.encrypted_message = encrypted_message
            envelope_object.encrypted_string_object.message = None
            envelope_object.is_encrypted = True
            envelope_object.encrypted_string_object.save()
            envelope_object.save()
    form = StringUnlocker() if envelope_object.is_encrypted else StringLocker()
    return render(request, 'postoffice/encrypt.html', {'form': form, 'envelope': envelope_object})

#todo research sending symmetric key in cleartext
def decrypt(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    if envelope_object:
        if request.method == "POST":
            form = StringLocker(request.POST)
            symmetric_key = form["symmetric_key"].value()
            envelope_object.user_prompt = None
            message = utilities.decrypt_string(symmetric_key, envelope_object.encrypted_string_object.encrypted_message)
            envelope_object.encrypted_string_object.encrypted_message = None
            envelope_object.encrypted_string_object.message = message 
            envelope_object.is_encrypted = False 
            envelope_object.encrypted_string_object.save()
            envelope_object.save()
    form = StringUnlocker() if envelope_object.is_encrypted else StringLocker()
    return render(request, 'postoffice/encrypt.html', {'form': form, 'envelope': envelope_object})

