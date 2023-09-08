from django import forms
from .models import Extract, Account

#! Meus formularios aqui


#// Formulario para adicional novos objetos nos meus modelos 

class NewExtract(forms.ModelForm):
    class Meta:
        model = Extract
        fields = ('name', 'value', 'account', 'type', 'date', 'descripition', 'pay')


class NewAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'value', 'descripition', 'type', 'color')