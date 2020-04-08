from django.contrib import admin
from postoffice.models import Envelope, TextMessage, ImageMessage, PdfMessage, EncryptionType

# Register your models here.

admin.site.register(TextMessage)
admin.site.register(ImageMessage)
admin.site.register(PdfMessage)
admin.site.register(EncryptionType)
admin.site.register(Envelope)
