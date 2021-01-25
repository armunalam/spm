from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutpage, name='logoutpage'),
    path('dataentry', views.dataentry, name='dataentry'),
    path('report', views.studentReport, name='report'),
    path('mapping', views.mapping, name='mapping'),
    path('assessment', views.assessment, name='assessment'),
    path('evaluation', views.evaluation, name='evaluation'),
    path('facultystudentreport', views.facultystudentreport, name='facultystudentreport'),
    path('facultystudentreportresult', views.facultystudentreportresult, name='facultystudentreportresult'),
    path('coursereport', views.courseReport, name='coursereport'),
    path('coursereportresult', views.courseReportResult, name='coursereportresult'),
]