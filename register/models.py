from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

currency = {
    "GBP": "£",
    "EUR": "€",
    "USD": "$",
}

class Account(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(choices=currency)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'balance']

    def __str__(self):
        return self.username
