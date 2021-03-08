from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse

from .decorators import authenticated, unauthenticated, allowedUsers
from .graphQueries import *

from mainapp.models import Course_T, CO_T, Assessment_T, Section_T, Enrollment_T, Evaluation_T
    
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


# Dashboards

# Student Dashboard
@allowedUsers(allowedRoles=['Student'])
def studentDashboard(request):
    chartName = []
    chartLabel = []
    chartDataSet = []
    
    chartN = 'Student-wise PLO'
    chartL = []
    chartD = []
    
    student_id = request.user.username
    print(str(student_id))
    
    row = getStudentWisePLO(student_id)
    
    for i in row:
        chartL.append(i[1])
        chartD.append(i[0])
    
    chartName.append(chartN)
    chartLabel.append(chartL)
    chartDataSet.append(chartD)
    
    chartN = 'Department-wise PLO'
    chartL = []
    chartD = []
    
    row = getDepartmentWisePLO('CSE')
    
    for i in row:
        chartL.append(i[1])
        chartD.append(i[2])
    
    chartName.append(chartN)
    chartLabel.append(chartL)
    chartDataSet.append(chartD)
    
    numberOfGraphs = len(chartName)
    
    # Stacked PLO Chart
    (plo, courses, table) = getCourseWisePLOChart(student_id)
    
    # getStudentProgressView
    (semester, semesterActual, semesterAttempted) = getStudentProgressView(student_id, 2019)
    
    # Heading
    a = getNoOfPLOAchieved(student_id)
    b = getNoOfPLOAttempted(student_id)
    c = getMinLowestPLO(student_id)
    d = ploSuccessRate(student_id)
    
    return render(request, 'mainapp/studentdashboard.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'numberOfGraphs': numberOfGraphs,
        'chartName': chartName,
        'chartLabel': chartLabel,
        'chartDataSet': chartDataSet,
        
        # Stacked PLO Chart
        'plo': plo,
        'courses': courses,
        'table': table,
        'ploWiseChartName': 'Course-wise PLO analysis',
        
        # getStudentProgressView
        'semester': semester,
        'semesterActual': semesterActual,
        'semesterAttempted': semesterAttempted,
        'studentProgressView': 'Student Progress View (Semester-wise)',
        
        # Heading
        'a': a,
        'b': b,
        'c': c,
        'd': d,
    })

# Faculty Dashboard
@allowedUsers(allowedRoles=['Faculty'])
def facultyDashboard(request):
    faculty_id = request.user.username
    chartName = []
    chartLabel = []
    chartDataSet = []
    
    chartN = 'Department-wise PLO'
    chartL = []
    chartD = []
    
    row = getDepartmentWisePLO('CSE')
    
    for i in row:
        chartL.append(i[1])
        chartD.append(i[2])
    
    chartName.append(chartN)
    chartLabel.append(chartL)
    chartDataSet.append(chartD)
    
    numberOfGraphs = len(chartName)
    
    # getCourseProgressView
    (semester2, semesterActualCourse, semesterAttemptedCourse) = getCourseProgressView('CSE303', '2019')
    
    # Heading
    a = getNumOfCoursesHead(faculty_id)
    b = getNumOfSections(faculty_id)
    c = getAverageSuccessRate(faculty_id)
    d = getNumOfPLOsTaught(faculty_id)
    
    return render(request, 'mainapp/facultydashboard.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'numberOfGraphs': numberOfGraphs,
        'chartName': chartName,
        'chartLabel': chartLabel,
        'chartDataSet': chartDataSet,
        
        # getCourseProgressView
        'semester2': semester2,
        'semesterActualCourse': semesterActualCourse,
        'semesterAttemptedCourse': semesterAttemptedCourse,
        'courseProgressView': 'Course Progress View',
        
        # Heading
        'a': a,
        'b': b,
        'c': c,
        'd': d,
    })

# Higher Management Dashboard
@allowedUsers(allowedRoles=['Higher Management'])
def hmDashboard(request):
    dept_id = 'CSE'
    
    chartName = []
    chartLabel = []
    chartDataSet = []
    
    chartN = 'Department-wise PLO'
    chartL = []
    chartD = []
    
    row = getDepartmentWisePLO('CSE')
    
    for i in row:
        chartL.append(i[1])
        chartD.append(i[2])
    
    chartName.append(chartN)
    chartLabel.append(chartL)
    chartDataSet.append(chartD)
    
    numberOfGraphs = len(chartName)
    
    # getSemesterWiseProgress
    (plo1, semesterActualOverall, semesterAttemptedOverall) = getSemesterWiseStudentProgress('2', 2019)
    
    # getSemesterWiseProgress
    (plo2, programActualOverall, programAttemptedOverall) = getProgramAchievement('BSc')
    
    a = getNumOfStudents(dept_id)
    b = getNumOfFaculties(dept_id)
    c = getNumOfCourses()
    d = getAverageAchievedPLO()
    
    return render(request, 'mainapp/hmdashboard.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        
        'numberOfGraphs': numberOfGraphs,
        'chartName': chartName,
        'chartLabel': chartLabel,
        'chartDataSet': chartDataSet,
        
        # getSemesterWiseProgress
        'plo1': plo1,
        'semesterActualOverall': semesterActualOverall,
        'semesterAttemptedOverall': semesterAttemptedOverall,
        'semesterProgressView': 'Semester Progress View',
        
        # getSemesterWiseProgress
        'plo2': plo2,
        'programActualOverall': programActualOverall,
        'programAttemptedOverall': programAttemptedOverall,
        'programProgressView': 'Program Progress View',
        
        # Heading
        'a': a,
        'b': b,
        'c': c,
        'd': d,
    })    

@authenticated
def dashboard(request):
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        
        if group == 'Student':
            return studentDashboard(request)
        if group == 'Faculty':
            return facultyDashboard(request)
        if group == 'Higher Management':
            return hmDashboard(request)
    
# Overall Report
@allowedUsers(allowedRoles=['Student'])
def studentReport(request):
    student_id = request.user.username
    ploTable = getCourseWisePLO(student_id)
    
    return render(request, 'mainapp/studentreport.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'ploTable': ploTable,
    })

@allowedUsers(allowedRoles=['Faculty'])
def dataentry(request):
    temp = Course_T.objects.filter()
    courses = []
    for i in range(len(temp)):
        courses.append(str(temp[i]))
    
    return render(request, 'mainapp/dataentry.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'courses': courses,
    })
    
@allowedUsers(allowedRoles=['Faculty'])
def mapping(request):
    if request.method == 'POST':
        course_id = request.POST.get('course-id')
        coMaps = request.POST.getlist('coMaps')
        
        course = Course_T(course_id, program_id='BSc', noOfCredits=3)
        course.save()
        
        for i in range(len(coMaps)):
            co = CO_T(coNo=i + 1, course_id=course_id, plo_id=coMaps[i])
            co.save()
    
        
    return redirect('dataentry')
        
@allowedUsers(allowedRoles=['Faculty'])
def assessment(request):
    if request.method == 'POST':
        faculty_id = request.user.username
        course_id = request.POST.get('course-id')
        sectionNo = request.POST.get('section')
        coMarks = request.POST.getlist('coMarks')
        
        section_id = None
        try:
            section_id = Section_T.objects.raw('''
                SELECT *
                FROM mainapp_section_t
                WHERE course_id = '{}' AND sectionNo = {};
            '''.format(course_id, sectionNo))
            section_id = section_id[0].id
        except:
            section_id = None
        
        if section_id is None:
            section = Section_T(sectionNo=sectionNo, course_id=course_id, faculty_id=faculty_id)
            section.save()
            section_id = section.id
            
        for j in range(1, len(coMarks) + 1):
            co_id = CO_T.objects.raw('''
                SELECT *
                FROM mainapp_co_t
                WHERE course_id = '{}' AND coNo = {}
            '''.format(course_id, j))
            assessment = Assessment_T(section_id=section_id, co_id=co_id[0].id, marks=coMarks[j - 1])
            assessment.save()
            
        return redirect('dataentry')
    
@allowedUsers(allowedRoles=['Faculty'])
def evaluation(request):
    if request.method == 'POST':
        course_id = request.POST.get('course-id')
        section = request.POST.get('section')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        
        student_id = request.POST.getlist('student_id')
        coMarks = []
        for i in range(len(student_id)):
            coMarks.append(request.POST.getlist(f'coMarks{i}'))
        
        section_id = None
        try:
            section_id = Section_T.objects.raw('''
                SELECT *
                FROM mainapp_section_t
                WHERE course_id = '{}' AND sectionNo = {};
            '''.format(course_id, section))
            section_id = section_id[0].id
        except:
            section_id = None
        assessment_list = []
        coLength = 0
        try:
            coLength = len(coMarks[0]) + 1
        except:
            coLength = 0
        for j in range(1, coLength):
            assessment_id = None
            try:
                assessment_id = Assessment_T.objects.raw('''
                    SELECT *
                    FROM mainapp_assessment_t
                    WHERE section_id = {} AND co_id IN (
                        SELECT id
                        FROM mainapp_co_t
                        WHERE course_id = '{}' AND coNo = {}
                    )
                '''.format(section_id, course_id, j))
                assessment_list.append(assessment_id[0].assessmentNo)
            except:
                assessment_id = None
                assessment_list.append(assessment_id)
        
        for i in range(len(student_id)):
            enrollment_id = None
            try:
                enrollment_id = Enrollment_T.objects.raw('''
                    SELECT *
                    FROM mainapp_enrollment_t
                    WHERE student_id = '{}' AND section_id = {}
                '''.format(student_id[i], section_id))
                enrollment_id = enrollment_id[0].enrollmentID
            except:
                enrollment_id = None
                
            if enrollment_id is None:
                enrollment = Enrollment_T(student_id=student_id[i], section_id=section_id, semester=semester, year=year)
                enrollment.save()
                enrollment_id = enrollment.enrollmentID
            
            for j in range(len(assessment_list)):
                evaluation = Evaluation_T(enrollment_id=enrollment_id, assessment_id=assessment_list[j], obtainedMarks=coMarks[i][j])
                evaluation.save()
                
        return redirect('dataentry')

@allowedUsers(allowedRoles=['Faculty', 'Higher Management'])
def facultystudentreportresult(request):
    if request.method == 'POST':
        student_id = request.POST.get('student-id')
        print(student_id)
        ploTable = getCourseWisePLO(student_id)
        
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        scripttag = 'false'
        if group == 'Higher Management':
            scripttag = 'false'
        
        searchtag = 'false'
        
        return render(request, 'mainapp/facultystudentreport.html', {
            'userfullname': f'{request.user.first_name} {request.user.last_name}',
            'usertype': request.user.groups.all()[0].name,
            'ploTable': ploTable,
            'scripttag': scripttag,
            'searchtag': searchtag,
        })

@allowedUsers(allowedRoles=['Faculty', 'Higher Management'])
def facultystudentreport(request):
    searchtag = 'true'
        
    if request.user.groups.exists():
            group = request.user.groups.all()[0].name
    
    scripttag = 'false'
    if group == 'Higher Management':
        scripttag = 'true'
    
    return render(request, 'mainapp/facultystudentreport.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'scripttag': scripttag,
        'searchtag': searchtag,
    })
    
@allowedUsers(allowedRoles=['Faculty', 'Higher Management'])
def courseReportResult(request):
    if request.method == 'POST':
        course_id = request.POST.get('course-id')
        (verdictRow, verdictTotal) = getVerdictTable(course_id)
        
        searchtag = 'false'
        
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        scripttag = 'false'
        if group == 'Higher Management':
            scripttag = 'true'
        
        return render(request, 'mainapp/coursereport.html', {
            'userfullname': f'{request.user.first_name} {request.user.last_name}',
            'usertype': request.user.groups.all()[0].name,
            
            # getVerdictTable
            'verdictRow': verdictRow,
            'verdictTotal': verdictTotal,
            'scripttag': scripttag,
            'searchtag': searchtag,
        })
    
@allowedUsers(allowedRoles=['Faculty', 'Higher Management'])
def courseReport(request):
    searchtag = 'true'
    
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    
    scripttag = 'false'
    if group == 'Higher Management':
        scripttag = 'true'
    
    return render(request, 'mainapp/coursereport.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
        'scripttag': scripttag,
        'searchtag': searchtag,
    })

@authenticated
def result(request):
    return render(request, 'mainapp/result.html', {
        'userfullname': f'{request.user.first_name} {request.user.last_name}',
        'usertype': request.user.groups.all()[0].name,
    })
