from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutpage, name='logoutpage'),
    path('dataentry', views.dataentry, name='dataentry'),
    path('result', views.result, name='result'),
    path('mapping', views.mapping, name='mapping'),
    path('assessment', views.assessment, name='assessment'),
    path('evaluation', views.evaluation, name='evaluation'),
]