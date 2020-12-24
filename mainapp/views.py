from django.shortcuts import render

# Create your views here.
def mainpage(request):
    return render(request, 'mainapp/index.html')
    
def login(request):
    return render(request, 'mainapp/login.html')