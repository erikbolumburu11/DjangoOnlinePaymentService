from django.db import models
from django.views.generic import ListView

from register.models import Account


# Create your models here.
class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sender_account")
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="recipient_account")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField()

class TransactionRequest(models.Model):
    sender= models.ForeignKey(Account, on_delete=models.CASCADE, related_name="request_from")
    recipient= models.ForeignKey(Account, on_delete=models.CASCADE, related_name="request_to")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField()