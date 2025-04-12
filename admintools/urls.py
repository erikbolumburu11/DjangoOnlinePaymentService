from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_users", views.view_all_users, name="all_users"),
    path("all_transactions", views.view_all_transactions, name="all_transactions"),
    path("register_admin", views.register_new_admin, name="register_admin"),
]
