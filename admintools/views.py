from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from admintools.forms import RegisterAdminForm
from payapp.models import Transaction
from register.models import Account


# Create your views here.
@login_required
def index(request):
    if not request.user.is_superuser:
        raise Http404("You don't have access to admin tools!")

    return render(request, 'admin_tools.html')

@login_required
def view_all_users(request):
    if not request.user.is_superuser:
        raise Http404("You don't have access to admin tools!")

    context = {
        "users": Account.objects.all()
    }

    return render(request, 'view_all_users.html', context)

@login_required
def view_all_transactions(request):
    if not request.user.is_superuser:
        raise Http404("You don't have access to admin tools!")

    context = {
        "transactions": Transaction.objects.all()
    }

    return render(request, 'view_all_transactions.html', context)

@login_required
def register_new_admin(request):
    if not request.user.is_superuser:
        raise Http404("You don't have access to admin tools!")

    if request.POST:
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            form.cleaned_data['account'].is_superuser = True
            form.cleaned_data['account'].save()
            return redirect("/")

    context = {
        "form": RegisterAdminForm
    }

    return render(request, 'register_new_admin.html', context)