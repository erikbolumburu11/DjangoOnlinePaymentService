from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from register.forms import AccountRegisterForm
from register.models import Account


def register(request):
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            form.instance.balance = 750
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = AccountRegisterForm()
    return render(request, 'register.html', {'form': form})