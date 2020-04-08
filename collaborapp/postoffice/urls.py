from django.urls import path, include
import postoffice.views

app_name = 'postoffice'

urlpatterns = [
    path('', postoffice.views.home, name='home'),
    path('outbox', postoffice.views.send_envelope, name="outbox"),
    path('inbox', postoffice.views.find_envelope, name="inbox"),
    path('new', postoffice.views.new_item, name="new_item"),
    path('view_contents/<primary_key>', postoffice.views.view_contents, name='view_contents'),
    path('encrypt/<primary_key>', postoffice.views.encrypt, name='encrypt'),
    path('decrypt/<primary_key>', postoffice.views.decrypt, name='decrypt'),
    path('delete-envelope/<primary_key>', postoffice.views.delete_item, name="delete_item"),
    path('edit/<primary_key>', postoffice.views.edit_item, name="edit_item"),
]
