from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account/<str:username>", views.account ,name="account"),
    path("make_transaction", views.make_transaction, name="make_transaction"),
    path("request_transaction", views.request_transaction, name="request_transaction"),
    path("transaction_history/<str:username>", views.transaction_history, name="transaction_history"),
    path("incoming_requests/<str:username>", views.incoming_requests, name="incoming_requests"),
    path("transaction_request/<int:request_id>", views.transaction_request, name="transaction_request"),
    path("outgoing_requests/<str:username>", views.outgoing_requests, name="outgoing_requests"),
]