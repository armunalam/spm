from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse

from .decorators import authenticated, unauthenticated#, allowedUsers
    
@unauthenticated
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('<h1>Unsuccessful</h1>')
        
    else:
        return render(request, 'mainapp/login.html')
    
def logoutpage(request):
    logout(request)
    return redirect('loginpage')

@authenticated
def dashboard(request):
    return render(request, 'mainapp/dashboard.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
    })

@authenticated
def dataentry(request):
    return render(request, 'mainapp/dataentry.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
    })

@authenticated
def result(request):
    return render(request, 'mainapp/result.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
    })