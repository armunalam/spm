# Reset the git everytime you run this script

import pandas as pd
from mainapp.models import Student_T, Faculty_T, School_T, Department_T, Program_T, Course_T, Evaluation_T, Assessment_T, CO_T, PLO_T, Enrollment_T, Section_T


# Reading data from CSV

data = pd.read_csv('Sheet.csv')

datalist = data.values.tolist()
for i in datalist[2:]:
    i[0] = str(int(i[0]))
    i[2] = int(i[2])
    for j in range(4,8):
        i[j] = int(i[j])
fullmarks = datalist[1][4:]
for i in range(len(fullmarks)):
    fullmarks[i] = int(fullmarks[i])
datalist = datalist[2:][:]


# School

school = School_T(schoolID='SETS', schoolName='School of Engineering')
school.save()


# Department

dept = Department_T(departmentID='CSE', departmentName='Computer Science and Engineering', school_id='SETS')
dept.save()


# Program

prog = Program_T(programID='BSc', programName='Bachelor of Science', department_id='CSE')
prog.save()


# Faculty

faculty = Faculty_T(facultyID='1234', fname='Mahady', lname='Hasan', department_id='CSE', gender='h')
faculty.save()


# Course

for i in datalist:
    course = Course_T(courseID=i[1], program_id='BSc', noOfCredits=3)
    course.save()


# Sections
sections = []
for i in datalist:
    if i[2] not in sections:
        sections.append(i[2])

for i in sections:
    section = Section_T(sectionNo=i, course_id='CSE303', faculty_id='1234')
    section.save()


# Student

student = Student_T(studentID='1820750', fname='Mayabee', lname='Tahsin', department_id='CSE', program_id='BSc')
student.save()

for i in datalist:
    student = Student_T(studentID=i[0], department_id='CSE', program_id='BSc')
    student.save()


# Enrollment

for i in datalist:
    courseID = 'CSE303'
    sectionNo = i[2]
    section_id = Section_T.objects.raw('''
        SELECT *
        FROM mainapp_section_t
        WHERE course_id = '{}' AND sectionNo = {};
    '''.format(courseID, sectionNo))
    enrollment = Enrollment_T(student_id=i[0], section_id=section_id[0].id, semester='Summer', year='2019')
    enrollment.save()
    
# PLO

plo1 = PLO_T(ploNo='PLO01', details='Knowledge', program_id='BSc')
plo2 = PLO_T(ploNo='PLO02', details='Requirement Analysis', program_id='BSc')
plo3 = PLO_T(ploNo='PLO03', details='Problem Analysis', program_id='BSc')
plo4 = PLO_T(ploNo='PLO04', details='Design', program_id='BSc')
plo5 = PLO_T(ploNo='PLO05', details='Problem Solving', program_id='BSc')
plo6 = PLO_T(ploNo='PLO06', details='Implementation', program_id='BSc')
plo7 = PLO_T(ploNo='PLO07', details='Experiment and Analysis', program_id='BSc')
plo8 = PLO_T(ploNo='PLO08', details='Community Engagement and Engineering', program_id='BSc')
plo9 = PLO_T(ploNo='PLO09', details='Teamwork', program_id='BSc')
plo10 = PLO_T(ploNo='PLO10', details='Communication', program_id='BSc')
plo11 = PLO_T(ploNo='PLO11', details='Self-directed', program_id='BSc')
plo12 = PLO_T(ploNo='PLO12', details='Process Management', program_id='BSc')

plo1.save()
plo2.save()
plo3.save()
plo4.save()
plo5.save()
plo6.save()
plo7.save()
plo8.save()
plo9.save()
plo10.save()
plo11.save()
plo12.save()
    

# CO

co = []
co.append(CO_T(coNo=1, course_id='CSE303', plo_id='PLO02'))
co.append(CO_T(coNo=2, course_id='CSE303', plo_id='PLO03'))
co.append(CO_T(coNo=3, course_id='CSE303', plo_id='PLO04'))
co.append(CO_T(coNo=4, course_id='CSE303', plo_id='PLO06'))

co[0].save()
co[1].save()
co[2].save()
co[3].save()


# Assessment

for i in range(1, len(sections) + 1):
    courseID = 'CSE303'
    sectionNo = i
    section_id = Section_T.objects.raw('''
        SELECT *
        FROM mainapp_section_t
        WHERE course_id = '{}' AND sectionNo = {};
    '''.format(courseID, sectionNo))
    for j in range(1, len(co) + 1):
        assessment = Assessment_T(section_id=section_id[0].id, co_id=j, marks=fullmarks[j - 1])
        assessment.save()
        

# Evaluation

for i in datalist:
    courseID = i[1]
    sectionNo = i[2]
    section_id = Section_T.objects.raw('''
        SELECT *
        FROM mainapp_section_t
        WHERE course_id = '{}' AND sectionNo = {};
    '''.format(courseID, sectionNo))
    
    for j in range(1, len(co) + 1):
        assessment_id = Assessment_T.objects.raw('''
            SELECT *
            FROM mainapp_assessment_t
            WHERE section_id = {} AND co_id IN (
                SELECT id
                FROM mainapp_co_t
                WHERE course_id = '{}' AND coNo = {}
            )
        '''.format(section_id[0].id, courseID, j))
        enrollment_id = Enrollment_T.objects.raw('''
            SELECT *
            FROM mainapp_enrollment_t
            WHERE student_id = '{}' AND section_id = {}
        '''.format(i[0], section_id[0].id))
        # evaluation = Evaluation_T(enrollment_id=enrollment_id[0].enrollmentID, assessment_id=assessment_id, obtainedMarks=i[j + 4])
        # evaluation = Evaluation_T(student_id=i[0], assessment_id=assessment_id[0].assessmentNo, obtainedMarks=i[j + 3])
        # try:
        evaluation = Evaluation_T(enrollment_id=enrollment_id[0].enrollmentID, assessment_id=assessment_id[0].assessmentNo, obtainedMarks=i[j + 3])
        evaluation.save()
        # except:
        #     continue