from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms
from django.forms.models import ModelChoiceField

from register.models import Account
from .models import Transaction, TransactionRequest

class TransactionForm(ModelForm):
    def __init__(self, username,*args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Account.objects.exclude(username__exact=username)

    class Meta:
        model = Transaction
        fields =['recipient', 'amount']

    field_order = ['recipient', 'amount']

class RequestTransactionForm(ModelForm):
    sender = forms.ModelChoiceField(queryset=None, label="From")
    def __init__(self, username,*args, **kwargs):
        super(RequestTransactionForm, self).__init__(*args, **kwargs)
        self.fields['sender'].queryset = Account.objects.exclude(username__exact=username)
    class Meta:
        model = TransactionRequest
        fields =['sender', 'amount']

    field_order = ['sender', 'amount']