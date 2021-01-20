from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutpage, name='logoutpage'),
    path('dataentry', views.dataentry, name='dataentry'),
    path('result', views.result, name='result'),
]