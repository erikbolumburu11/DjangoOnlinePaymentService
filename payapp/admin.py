from django.contrib import admin

from payapp.models import Transaction, TransactionRequest
from register.models import Account


# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = [
        "sender",
        "recipient",
        "amount",
        "date_time"
    ]

    pass

admin.site.register(Transaction, TransactionAdmin)

class TransactionRequestAdmin(admin.ModelAdmin):
    model = TransactionRequest
    list_display = [
        "sender",
        "recipient",
        "amount",
        "date_time"
    ]

    pass

admin.site.register(TransactionRequest, TransactionRequestAdmin)
