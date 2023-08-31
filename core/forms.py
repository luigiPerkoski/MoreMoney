from django import forms
from .models import Extract

class NewExtract(forms.ModelForm):
    class Meta:
        model = Extract
        fields = ('name', 'value', 'account', 'type', 'date', 'descripition', 'pay')
