# forms.py
from django import forms
from .models import Postingans

class EncryptedFileForm(forms.ModelForm):
    class Meta:
        model = Postingans
        fields = ['title', 'encrypted_file']

class KeyForm(forms.Form):
    input_key = forms.CharField(label='Enter Encryption Key', widget=forms.TextInput(attrs={'type': 'password'}))