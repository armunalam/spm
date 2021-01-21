from django.db import models


class School_T(models.Model):
    schoolID = models.CharField(max_length=5, primary_key=True)
    schoolName = models.CharField(max_length=30)
    
class Department_T(models.Model):
    departmentID = models.CharField(max_length=5, primary_key=True)
    departmentName = models.CharField(max_length=30)
    schoolID = models.ForeignKey(School_T, on_delete=models.CASCADE)
    
class Student_T(models.Model):
    studentID = models.CharField(max_length=7, primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    program = models.CharField(max_length=30)
    departmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=1)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    
class Faculty_T(models.Model):
    facultyID = models.CharField(max_length=4, primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    dateOfBirth = models.DateField()
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    departmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE)
    
class Program_T(models.Model):
    programID = models.CharField(max_length=5, primary_key=True)
    programName = models.CharField(max_length=30)
    departmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE, default='N/A')

    
class Course_T(models.Model):
    courseID = models.CharField(max_length=7, primary_key=True)
    courseName = models.CharField(max_length=30)
    noOfCredits = models.IntegerField()
    programID = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    
class PLO_T(models.Model):
    ploNo = models.CharField(max_length=5, primary_key=True)
    programID = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    details = models.CharField(max_length=30)
    
class CO_T(models.Model):
    coNo = models.IntegerField(primary_key=True)
    ploNo = models.ForeignKey(PLO_T, on_delete=models.CASCADE)
    details = models.CharField(max_length=30)
    courseID = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    
class Section_T(models.Model):
    sectionID = models.IntegerField(primary_key=True)
    courseID = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    facultyID = models.ForeignKey(Faculty_T, on_delete=models.CASCADE)
    
class Enrollment_T(models.Model):
    enrollmentID = models.CharField(max_length=10, primary_key=True)
    studentID = models.ForeignKey(Student_T, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    semester = models.CharField(max_length=2)
    year = models.CharField(max_length=4)
    
class Assessment_T(models.Model):
    assessmentNo = models.CharField(max_length=30, primary_key=True)
    marks = models.FloatField()
    coNo = models.ForeignKey(CO_T, on_delete=models.CASCADE, default=0)
    enrollmentID = models.ForeignKey(Enrollment_T, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section_T, on_delete=models.CASCADE, default=0)

class Evaluation_T(models.Model):
    evaluationNo = models.CharField(max_length=30, primary_key=True)
    obtainedMarks = models.FloatField()
    assessmentNo = models.ForeignKey(Assessment_T, on_delete=models.CASCADE, default='N/A')
    studentID = models.ForeignKey(Student_T, on_delete=models.CASCADE, default='N/A')