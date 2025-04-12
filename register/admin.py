from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = Account
    list_display = [
        "username",
        "first_name",
        "last_name",
        "balance",
    ]
    fieldsets = [
        ("User Info", {"fields": [
            "username",
            "email",
            "first_name",
            "last_name",
            "currency",
            "balance"
        ]})
    ]

admin.site.register(Account, AccountAdmin)
