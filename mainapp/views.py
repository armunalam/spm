from django.shortcuts import render

def mainpage(request):
    return render(request, 'mainapp/index.html')
    
def login(request):
    return render(request, 'mainapp/login.html')