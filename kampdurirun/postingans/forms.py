# forms.py
from django import forms
from .models import Postingans

class EncryptedFileForm(forms.ModelForm):
    class Meta:
        model = Postingans
        fields = ['title', 'encrypted_file']

class KeyForm(forms.Form):
    input_key = forms.CharField()

class PDFFileForm(forms.ModelForm):
    class Meta:
        model = Postingans
        fields = ['title', 'encrypted_file']