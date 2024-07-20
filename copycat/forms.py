from django import forms
from .models import Uploadmp4

class Mp4form(forms.ModelForm):
    class Meta:
        model = Uploadmp4
        fields = ('files',)
