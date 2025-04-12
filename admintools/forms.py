from django import forms

from register.models import Account


class RegisterAdminForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.exclude(is_superuser=True))
