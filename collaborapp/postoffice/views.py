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

    #only make envelope object deletable if it's not currently encrypted
    if not envelope_object.is_encrypted:
        envelope_object.delete()
    return redirect('postoffice_home')

def new_item(request):
    if request.method == "POST":
        envelope_form = NewEnvelope(request.POST)
        message_form = NewEncryptedStringObject(request.POST)
        if message_form.is_valid() and envelope_form.is_valid():
            #todo: for now, only letting fernet_string encryption be an option
            encryption_type = EncryptionType.objects.filter(name="fernet_string")[0]
            envelope = envelope_form.save(commit=False)
            envelope.save()
            message = message_form.save(commit=False)
            message.envelope = envelope 
            message.encryption_type = encryption_type
            message.save()
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
def view_contents(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    if envelope_object:
        contents = envelope_object.encrypted_objects.all()
    form = StringUnlocker()
    return render(request, 'postoffice/view_contents.html', {'form': form, 'envelope': envelope_object, 'contents': contents})

#todo research sending symmetric key in cleartext
def encrypt(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    if envelope_object:
        if request.method == "POST":
            form = StringLocker(request.POST)
            symmetric_key = form["symmetric_key"].value()
            user_prompt = form["user_prompt"].value()
            try:
                envelope_object = encrypt_envelope_and_contents(envelope_object, symmetric_key)
            except Exception:
                raise 
            else:
                envelope_object.user_prompt = user_prompt
                envelope_object.is_encrypted = True
                envelope_object.save()
    return redirect('postoffice_view_contents', primary_key)

def edit_item(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    if envelope_object:
        if request.method == "POST":
            form = StringLocker(request.POST)
            symmetric_key = form["symmetric_key"].value()
            user_prompt = form["user_prompt"].value()
            try:
                envelope_object = encrypt_envelope_and_contents(envelope_object, symmetric_key)
            except Exception:
                raise 
            else:
                envelope_object.user_prompt = user_prompt
                envelope_object.is_encrypted = True
                envelope_object.save()
        contents = envelope_object.encrypted_objects.all()
    form = StringUnlocker() if envelope_object.is_encrypted else StringLocker()
    return render(request, 'postoffice/edit_item.html', {'form': form, 'envelope': envelope_object, 'contents': contents})

#todo research sending symmetric key in cleartext
def decrypt(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 
    if envelope_object:
        if request.method == "POST":
            if not envelope_object.is_encrypted:
                return encrypt(request, primary_key)

            form = StringLocker(request.POST)
            symmetric_key = form["symmetric_key"].value()
            try:
                envelope_object = decrypt_envelope_and_contents(envelope_object, symmetric_key)
            except Exception as e:
                data['error_msg'] = repr(e) + str(e)
                #raise e
            else:
                envelope_object.user_prompt = None
                envelope_object.is_encrypted = False 
                envelope_object.save()
    return redirect('postoffice_view_contents', primary_key)

def encrypt_envelope_and_contents(envelope, symmetric_key):
    try:
        #todo if you want more than one object in an envelope, update this:
        object_in_envelope = envelope.encrypted_objects.first()
        encrypted_message = utilities.encrypt_string(symmetric_key, object_in_envelope.message)
        object_in_envelope.encrypted_message = encrypted_message
        object_in_envelope.message = None
    except Exception:
        raise
    finally:
        object_in_envelope.save()
    return envelope 

def decrypt_envelope_and_contents(envelope, symmetric_key):
    try:
        #todo if you want more than one object in an envelope, update this:
        object_in_envelope = envelope.encrypted_objects.first()
        print("this should be an obj in an envelope:")
        print(object_in_envelope)
        message = utilities.decrypt_string(symmetric_key, object_in_envelope.encrypted_message)
        object_in_envelope.encrypted_message = None
        object_in_envelope.message = message 
    except Exception:
        raise
    finally:
        object_in_envelope.save()
    return envelope 


