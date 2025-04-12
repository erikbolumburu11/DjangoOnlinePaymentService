import datetime
from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from payapp.forms import TransactionForm, RequestTransactionForm
from payapp.models import Transaction, TransactionRequest
from register.models import Account

import requests

currency = {
    "GBP": "£",
    "EUR": "€",
    "USD": "$",
}


def get_account_from_username(username: str) -> Account:
    return get_object_or_404(Account, username__exact=username)

def process_transaction(t_request: TransactionRequest):
    if t_request.sender == t_request.recipient:
        return HttpResponse("You cannot send yourself money")

    if t_request.sender.balance < t_request.amount:
        return HttpResponse("You do not have enough money to complete this transaction")

    transaction = Transaction(
        sender = t_request.sender,
        recipient = t_request.recipient,
        amount = t_request.amount,
        date_time=datetime.datetime.now()
    )

    t_request.sender.balance -= t_request.amount
    t_request.recipient.balance += t_request.amount

    transaction.save()
    t_request.sender.save()
    t_request.recipient.save()

def get_transaction_history(account: Account):
    sent_transactions = Transaction.objects.filter(sender=account)
    received_transactions = Transaction.objects.filter(recipient=account)
    all_transactions = (sent_transactions | received_transactions).order_by('-date_time')
    return all_transactions

def get_incoming_requests(account: Account):
    return TransactionRequest.objects.filter(sender=account).order_by('-date_time')

def get_outgoing_requests(account: Account):
    return TransactionRequest.objects.filter(recipient=account).order_by('-date_time')

def convert_currency(from_cur_str: str, to_cur_str: str, amount: float) -> float:
    r = requests.get(
        "http://127.0.0.1:7000/conversion/" +
        from_cur_str.lower() + "/" +
        to_cur_str.lower() + "/" +
        amount.__str__() + "/"
    )
    print(
        "http://127.0.0.1:7000/conversion/" +
        from_cur_str.lower() + "/" +
        to_cur_str.lower() + "/" +
        amount.__str__() + "/"
    )

    print(r.json())

    return round(Decimal(r.json()), 2)

def convert_transaction(transaction: Transaction, from_cur_str: str, to_cur_str) -> Transaction:
    transaction.amount = convert_currency(
        from_cur_str,
        to_cur_str,
        transaction.amount
    )

    return transaction

def convert_transactions(transactions: QuerySet[Transaction], from_cur_str, to_cur_str) -> QuerySet[Transaction]:
    for transaction in transactions:
        transaction.amount = convert_transaction(transaction, from_cur_str, to_cur_str).amount

    return transactions

def convert_request(t_request: TransactionRequest, from_cur_str: str, to_cur_str) -> TransactionRequest:
    t_request.amount = convert_currency(
        from_cur_str,
        to_cur_str,
        t_request.amount
    )

    return t_request

def convert_requests(t_requests: QuerySet[TransactionRequest], from_cur_str, to_cur_str) -> QuerySet[TransactionRequest]:
    for t_request in t_requests:
        t_request.amount = convert_request(t_request, from_cur_str, to_cur_str).amount

    return t_requests

# Create your views here.

@login_required
def index(request):
    return HttpResponseRedirect('account/' + request.user.get_username())

@login_required
def make_transaction(request):
    if request.POST:
        form = TransactionForm(request.user.username, request.POST)
        if form.is_valid():
            tr_sender = get_account_from_username(request.user.username)
            tr_recipient = get_account_from_username(form.instance.recipient.username)
            process_transaction(TransactionRequest(
                sender = tr_sender,
                recipient = tr_recipient,
                amount = convert_currency(tr_sender.currency, "gbp", form.instance.amount)
            ))

            return redirect('/')

    context = {
        "form": TransactionForm(request.user.username)
    }
    return render(request, "make_transaction.html", context)

@login_required
def request_transaction(request):
    if request.POST:
        form = RequestTransactionForm(request.user.username, request.POST)
        if form.is_valid():
            form.instance.recipient = get_object_or_404(Account, username__exact=request.user.username)
            form.instance.date_time = datetime.datetime.now()
            form.instance.amount = convert_currency(
                get_account_from_username(request.user.username).currency,
                "gbp",
                form.instance.amount
            )
            form.save()
            return redirect('/')

    context = {
        "form": RequestTransactionForm(request.user.username)
    }
    return render(request, "request_transaction.html", context)


@login_required
def account(request, username):
    if not request.user.is_superuser:
        if request.user.username != username:
            raise Http404("You don't have access to this page!")

    user_account = get_account_from_username(username)

    incoming_requests = get_incoming_requests(user_account)[:5]
    outgoing_requests = get_outgoing_requests(user_account)[:5]
    transactions = get_transaction_history(user_account)[:5]

    context = {
        "account": user_account,
        "balance": convert_currency("gbp", user_account.currency, user_account.balance),
        "currency_symbol": currency[user_account.currency],
        "transactions": convert_transactions(transactions, "gbp", user_account.currency),
        "incoming_requests": convert_requests(incoming_requests, "gbp", user_account.currency),
        "outgoing_requests": convert_requests(outgoing_requests, "gbp", user_account.currency)
    }

    return render(request, "account.html", context)

@login_required
def transaction_history(request, username):
    if not request.user.is_superuser:
        if request.user.username != username:
            raise Http404("You don't have access to this page!")

    transactions = get_transaction_history(get_account_from_username(username))

    user_account = get_account_from_username(username)
    context = {
        "transactions": convert_transactions(transactions, "gbp", user_account.currency),
        "currency_symbol": currency[user_account.currency],
    }

    return render(request, "transaction_history.html", context)

@login_required
def incoming_requests(request, username):
    if not request.user.is_superuser:
        if request.user.username != username:
            raise Http404("You don't have access to this page!")

    requests = get_incoming_requests(get_account_from_username(username))
    user_account = get_account_from_username(username)

    context = {
        "incoming_requests": convert_requests(requests, "gbp", user_account.currency),
        "currency_symbol": currency[user_account.currency]
    }

    return render(request, "incoming_requests.html", context)

@login_required
def transaction_request(request, request_id: int):
    t_request = get_object_or_404(TransactionRequest, pk=request_id)

    if not request.user.is_superuser:
        if  (
                request.user.username != t_request.sender.username and
                request.user.username != t_request.recipient.username
            ):
            raise Http404("You don't have access to this page!")

    if request.POST:
        if request.POST.get("accept"):
            process_transaction(t_request)
            t_request.delete()
            return redirect("/")

        else:
            t_request.delete()
            return redirect("/")

    t_request = get_object_or_404(TransactionRequest, pk=request_id)
    user_account = get_account_from_username(request.user.username)
    context = {
        "transaction_request": convert_request(t_request, "gbp", user_account.currency),
    }

    return render(request, "transaction_request.html", context)

@login_required
def outgoing_requests(request, username):
    if not request.user.is_superuser:
        if request.user.username != username:
            raise Http404("You don't have access to this page!")

    requests = get_outgoing_requests(get_account_from_username(username))
    user_account = get_account_from_username(username)

    context = {
        "outgoing_requests": convert_requests(requests, "gbp", user_account.currency),
        "currency_symbol": currency[user_account.currency]
    }

    return render(request, "outgoing_requests.html", context)
