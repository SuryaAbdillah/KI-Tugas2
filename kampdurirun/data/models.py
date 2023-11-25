# data/models.py

from django.db import models
from user.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_panjang = models.CharField(max_length=60)
    berat_badan = models.IntegerField()
    tinggi_badan = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Data"
