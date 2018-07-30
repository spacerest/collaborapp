from django.db import models

# Create your models here.

class Notes(object):
    """docstring for Notes"""
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000)
