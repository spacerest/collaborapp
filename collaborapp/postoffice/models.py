from django.db import models

class EncryptionType(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name 

class Envelope(models.Model):
    primary_key = models.CharField(max_length=40, primary_key=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    sender_name = models.CharField(max_length=40)
    recipient_name = models.CharField(max_length=40)
    user_prompt = models.TextField(max_length=500, null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)
    def __str__(self):
        return "From: " + self.sender_name + ", To: " + self.recipient_name + ", " + self.date_sent.ctime()

class EncryptedStringObject(models.Model):
    encryption_type = models.ForeignKey(EncryptionType, on_delete=models.CASCADE)
    message = models.TextField(max_length=40000, null = True, blank = True)
    encrypted_message = models.BinaryField(max_length=50000, null=True, blank=True)
    envelope = models.ForeignKey(Envelope, related_name='encrypted_objects', on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message or self.date_created.ctime()
