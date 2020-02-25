from django.urls import path, include
import postoffice.views

urlpatterns = [
    path('', postoffice.views.home, name='postoffice_home'),
    path('outbox', postoffice.views.send_envelope, name="postoffice_outbox"),
    path('inbox', postoffice.views.find_envelope, name="postoffice_inbox"),
    path('new', postoffice.views.new_item, name="postoffice_new_item"),
    path('encrypt/<primary_key>', postoffice.views.encrypt, name='postoffice_encrypt'),
    path('decrypt/<primary_key>', postoffice.views.decrypt, name='postoffice_decrypt'),
    path('delete-envelope/<primary_key>', postoffice.views.delete_item, name="postoffice_delete_item"),
]
