# postingans/models.py
from django.db import models
from .utils import sign_pdf
from django.core.files.base import ContentFile
from user.models import User
import os
from django.db import models
from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from user.models import User  # Assuming your user model is in the 'user' app
from .utils import encrypt_file, decrypt_file
import os

class Postingans(models.Model):
    title = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to='uploads/encrypted_files/')
    encryption_key = models.BinaryField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postingans')
    file_format = models.CharField(max_length=10, blank=True)
    digital_signature = models.BinaryField(null=True, blank=True)

    def save(self, *args, **kwargs):
        key = Fernet.generate_key()
        uploaded_file_data = self.encrypted_file.read()

        # Sign the PDF and store the digital signature
        signature = sign_pdf(uploaded_file_data, self.user.private_key)
        self.digital_signature = signature

        encrypted_data = encrypt_file(uploaded_file_data, key)
        encrypted_content = ContentFile(encrypted_data)
        self.encrypted_file.save(self.encrypted_file.name, encrypted_content, save=False)
        self.encryption_key = key

        file_name, file_extension = os.path.splitext(os.path.basename(self.encrypted_file.name))
        self.file_format = file_extension[1:]

        super(Postingans, self).save(*args, **kwargs)
