from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse

from .decorators import authenticated, unauthenticated, allowedUsers
from .graphQueries import *
    
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


# Dashboard

# Student

# Higher Management

@allowedUsers(allowedRoles=['Student'])
def studentDashboard(request):
    
    chartName = []
    chartLabel = []
    chartDataSet = []
    
    
    
    
    chartN = 'Student-wise PLO'
    chartL = [] # ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    chartD = [] # [2, 10, 5, 3, 20, 30, 45]
    
    student_id = '1625654'
    
    row = getStudentWisePLO(student_id)
    
    for i in row:
        chartL.append(i[1])
        chartD.append(i[0])
    
    chartName.append(chartN)
    chartLabel.append(chartL)
    chartDataSet.append(chartD)
    
    chartN = 'Department-wise PLO'
    chartL = [] # ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    chartD = [] # [2, 10, 5, 3, 20, 30, 45]
    
    row = getDepartmentWisePLO('CSE')
    
    for i in row:
        chartL.append(i[1])
        chartD.append(i[2])
    
    chartName.append(chartN)
    chartLabel.append(chartL)
    chartDataSet.append(chartD)
    
    numberOfGraphs = len(chartName)
    
    # Table
    
    ploTable = getCourseWisePLO(student_id)
    
    # Stacked PLO Chart
    (plo, courses, table) = getCourseWisePLOChart(student_id)
    
    
    return render(request, 'mainapp/dashboard.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'numberOfGraphs': numberOfGraphs,
        'chartName': chartName,
        'chartLabel': chartLabel,
        'chartDataSet': chartDataSet,
        'ploTable': ploTable,
        
        # Stacked PLO Chart
        'plo': plo,
        'courses': courses,
        'table': table,
        'ploWiseChartName': 'Course-wise PLO analysis'
    })

@authenticated
def dashboard(request):
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        
        if group == 'Student':
            return studentDashboard(request)
    
    

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