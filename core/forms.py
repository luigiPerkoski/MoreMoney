from django import forms
from .models import Extract, Account

#! Meus formularios aqui


#// Formulario para adicional novos objetos nos meus modelos 

class NewExtract(forms.ModelForm):
    
    class Meta:
        model = Extract
        fields = ('name', 'value', 'account', 'type', 'date', 'pay')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'value': forms.TextInput(attrs={'type': 'text'}),
        }

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

        
    

class NewAccount(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'value', 'type')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'value': forms.TextInput(attrs={'type': 'text'}),
            }
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)