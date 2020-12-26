from django.shortcuts import render

def dashboard(request):
    return render(request, 'mainapp/dashboard.html')
    
def login(request):
    return render(request, 'mainapp/login.html')
    
def dataentry(request):
    return render(request, 'mainapp/dataentry.html')
    
def result(request):
    return render(request, 'mainapp/result.html')