from django.db import models

# Create your models here.

class Letter(models.Model):
    private_key = models.CharField(max_length=10)
    date_sent = models.DateTimeField(auto_now_add=True)
