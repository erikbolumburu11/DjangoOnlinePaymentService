from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm, UserCreationForm
from django import forms

from .models import Account

class AccountCreationForm(AdminUserCreationForm):
    class Meta:
        model = Account
        fields = ("email", "first_name", "last_name", "balance")

class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ("email", "first_name", "last_name", "balance")

class AccountRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=20, label='Password')
    password2 = forms.CharField(max_length=20, label ='Confirm Password')
    currency = forms.ChoiceField(choices={
        "GBP": "£",
        "EUR": "€",
        "USD": "$",
    })

    class Meta:
        model = Account
        fields = {'username', 'email', 'first_name', 'last_name', 'currency', 'password1', 'password2'}

    field_order = ['username', 'email','first_name', 'last_name', 'currency','password1', 'password2']