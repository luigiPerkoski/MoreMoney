from django import forms
from .models import Extract, Account

#! Meus formularios aqui


#// Formulario para adicional novos objetos nos meus modelos 

class NewExtract(forms.ModelForm):
    class Meta:
        model = Extract
        fields = ('name', 'value', 'account', 'type', 'date', 'descripition', 'pay')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class NewAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'value', 'type', 'descripition')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
            }
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Pesquisar')