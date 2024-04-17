from django import forms
from .models import Companies

class CompaniesForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название кампании')
    link = forms.CharField(max_length=500, label='Ссылка')
