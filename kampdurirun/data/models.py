# data/models.py

from django.db import models
from user.models import User
from cryptography.fernet import Fernet
from .utils import generate_key_pair

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_panjang = models.CharField(max_length=60)
    berat_badan = models.IntegerField()
    tinggi_badan = models.IntegerField()
    public_key = models.BinaryField(null=True, blank=True)  # Store the encryption key as bytes
    private_key = models.BinaryField(null=True, blank=True)  # Store the encryption key as bytes

    def __str__(self):
        return f"{self.user.username}'s Data"

    def save(self, *args, **kwargs):
        # Generate a new key if not provided
        if not (self.public_key and self.private_key):
            self.private_key, self.public_key  = generate_key_pair()

        super().save(*args, **kwargs)
