from django import forms

from allauth.socialaccount.models import SocialAccount

class DonateForm(forms.Form):
    amount = forms.FloatField(label='Amount',required=True, widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    note = forms.CharField(label='Note', max_length=128, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class SettingsForm(forms.Form):
    autopay = forms.BooleanField(label='Autopay', required=False)
