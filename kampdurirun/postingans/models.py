# postingans/models.py
from django.db import models
from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from user.models import User  # Assuming your user model is in the 'user' app
from .utils import encrypt_file, decrypt_file
import os

class Postingans(models.Model):
    title = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to='uploads/encrypted_files/')
    encryption_key = models.BinaryField(null=True, blank=True)  # Store the encryption key as bytes
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postingans')
    file_format = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        # Generate an encryption key
        key = Fernet.generate_key()

        # Read the uploaded file data
        uploaded_file_data = self.encrypted_file.read()

        # Apply your custom encryption process to the uploaded file data
        encrypted_data = encrypt_file(uploaded_file_data, key)

        # Create a ContentFile with the encrypted data
        encrypted_content = ContentFile(encrypted_data)

        # Save the encrypted data to the file field
        self.encrypted_file.save(self.encrypted_file.name, encrypted_content, save=False)

        # Save the encryption key as bytes
        self.encryption_key = key

        # Extract file format from the file name or use the file extension directly
        file_name, file_extension = os.path.splitext(os.path.basename(self.encrypted_file.name))
        self.file_format = file_extension[1:]

        super(Postingans, self).save(*args, **kwargs)