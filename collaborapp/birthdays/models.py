from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Gift(models.Model):
    recipient_age = models.IntegerField(default=0)
    recipient = models.ForeignKey(User, related_name="present_recipient", on_delete=models.SET_NULL, blank=True, null=True)
    gifter = models.ForeignKey(User, related_name="present_gifter", on_delete=models.SET_NULL, blank=True, null=True)
    
