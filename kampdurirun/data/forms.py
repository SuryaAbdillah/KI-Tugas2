from django import forms
from .models import UserData

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['nama_panjang', 'berat_badan', 'tinggi_badan']
