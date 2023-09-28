from django import forms
from .models import Extract, Account

#! Meus formularios aqui


#// Formulario para adicional novos objetos nos meus modelos 

class NewExtract(forms.ModelForm):
    
    class Meta:
        model = Extract
        fields = ('name', 'value', 'account', 'type', 'date', 'pay', 'descripition')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'value': forms.TextInput(attrs={'type': 'text'}),
            'descripition':forms.Textarea(attrs={'required': False})
        }

class NewAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'value', 'type', 'descripition')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'value': forms.TextInput(attrs={'type': 'text'}),
            'descripition':forms.Textarea(attrs={'required': False})
            }
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class CadastroForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, help_text='Máximo de 30 caracteres')
    email = forms.EmailField(max_length=254, required=True, help_text='Informe um endereço de email válido')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='A senha não deve ser muito comum')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


