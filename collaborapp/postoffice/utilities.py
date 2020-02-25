from __keys import django_secret_key
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
import base64

def encrypt_string(key, message):
    key = key.encode()
    salt = django_secret_key.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                 length=32,
                 salt=salt,
                 iterations=100000,
                 backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(key))

    f = Fernet(key)

    message_encoded = message.encode()
    message_encrypted = f.encrypt(message_encoded)
    return message_encrypted

def decrypt_string(key, encrypted_message):
    key = key.encode()
    salt = django_secret_key.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                 length=32,
                 salt=salt,
                 iterations=100000,
                 backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(key))

    f = Fernet(key)

    message_decrypted = f.decrypt(encrypted_message)
    message_decoded = message_decrypted.decode()
    return message_decoded

