from django.contrib import admin
from postoffice.models import Envelope, EncryptedStringObject, EncryptionType

# Register your models here.

admin.site.register(EncryptedStringObject)
admin.site.register(EncryptionType)
admin.site.register(Envelope)
