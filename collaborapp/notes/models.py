from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    """docstring for Note"""
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000)

    def __str__(self):
        return self.title
