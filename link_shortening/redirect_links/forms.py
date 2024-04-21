from django import forms
from .models import Companies

class CompaniesForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название кампании', widget= forms.TextInput ( attrs = {'class': 'input', 'placeholder':'Моя кампания'}))
    link = forms.CharField(max_length=500, label='Ссылка', widget= forms.TextInput( attrs = {'class': 'input', 'placeholder': 'https://mycompany.ru'}))
