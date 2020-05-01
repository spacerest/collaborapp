from django.shortcuts import render, redirect
from postoffice.forms import EnvelopeReceiver, StringLocker, StringUnlocker, NewTextMessage, NewEnvelope, NewImageMessage, NewPdfMessage
from postoffice.models import Envelope, EncryptionType, TextMessage, ImageMessage, PdfMessage
from postoffice import utilities
# Create your views here.

def home(request):
    return render(request, 'postoffice/home.html')

def lookup_envelope(primary_key):
    envelope_object_list = Envelope.objects.filter(primary_key=primary_key)
    if envelope_object_list:
        return envelope_object_list[0]
    else:
        return False

def delete_item(request, primary_key):
    envelope_object = lookup_envelope(primary_key) 

    #only make envelope object deletable if it's not currently encrypted
    if not envelope_object.is_encrypted:
        envelope_object.delete()
    return redirect('postoffice:home')

def new_item(request):
    try:
        if request.method == "POST":
            envelope_form = NewEnvelope(request.POST)
            message_form = NewTextMessage(request.POST)
            image_form = NewImageMessage(request.POST, request.FILES)
            pdf_form = NewPdfMessage(request.POST, request.FILES)
            print(pdf_form)
            print(pdf_form.is_valid())
            if message_form.is_valid() and envelope_form.is_valid():
                #todo: for now, only letting fernet_string encryption be an option
                encryption_type = EncryptionType.objects.filter(name="fernet_string")[0]
                envelope = envelope_form.save(commit=False)
                envelope.save()
                message = message_form.save(commit=False)
                message.envelope = envelope 
                message.encryption_type = encryption_type
                message.save()
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.envelope = envelope 
                    image.encryption_type = encryption_type
                    image.save()
                if pdf_form.is_valid():
                    pdf = pdf_form.save(commit=False)
                    pdf.envelope = envelope 
                    pdf.encryption_type = encryption_type
                    pdf.save()

                return redirect('postoffice:encrypt', envelope.primary_key)
        data = {'envelope_form': envelope_form, 'message_form': message_form, 'image_form': image_form, 'pdf_form': pdf_form}
        return render(request, 'postoffice/outbox.html', data)
    except Exception as e:
        print(e)

def send_envelope(request):
    envelope_form = NewEnvelope()
    message_form = NewTextMessage()
    image_form = NewImageMessage()
    pdf_form = NewPdfMessage()
    data = {"envelope_form": envelope_form, "message_form": message_form, "image_form": image_form, "pdf_form": pdf_form}
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
    try:
        data = {}
        data['envelope'] = lookup_envelope(primary_key) 
        data['form'] = StringUnlocker()
        if data['envelope']:
            data['text_contents'] = data['envelope'].text_messages.all()
            data['image_contents'] = data['envelope'].image_messages.all()
            data['pdf_contents'] = data['envelope'].pdf_messages.all()
            print(data)
        form = StringUnlocker()
        return render(request, 'postoffice/view_contents.html', data)
    except Exception as e:
        print(data)
        print(e)

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
    return redirect('postoffice:view_contents', primary_key)

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
        contents = envelope_object.text_messages.all()
    form = StringUnlocker() if envelope_object.is_encrypted else StringLocker()
    return render(request, 'postoffice/edit_item.html', {'form': form, 'envelope': envelope_object, 'contents': contents})

#todo research sending symmetric key in cleartext
def decrypt(request, primary_key):
    data = {}
    data['envelope'] = lookup_envelope(primary_key) 
    if data['envelope']:
        if request.method == "POST":
            form = StringUnlocker(request.POST)
            symmetric_key = form["symmetric_key"].value()
            try:
                encrypted_contents = decrypt_envelope_and_contents(data['envelope'], symmetric_key)
            except Exception as e:
                data['error_msg'] = repr(e) + str(e)
                data['form'] = form
                data['envelope'] = lookup_envelope(primary_key)
                data['contents'] = data['envelope'].text_messages.all()
                return render(request, 'postoffice/view_contents.html', data)
            else:
                encrypted_contents.user_prompt = None
                encrypted_contents.is_encrypted = False 
                encrypted_contents.save()
    return redirect('postoffice:view_contents', primary_key)

def encrypt_envelope_and_contents(envelope, symmetric_key):
    try:
        #todo if you want more than one object in an envelope, update this:
        object_in_envelope = envelope.text_messages.first()
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
        object_in_envelope = envelope.text_messages.first()
        message = utilities.decrypt_string(symmetric_key, object_in_envelope.encrypted_message)
        object_in_envelope.encrypted_message = None
        object_in_envelope.message = message 
    except Exception:
        raise
    finally:
        object_in_envelope.save()
    return envelope 


