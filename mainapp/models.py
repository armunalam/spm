from django.db import models


class School_T(models.Model):
    schoolID = models.CharField(max_length=5, primary_key=True)
    schoolName = models.CharField(max_length=30)
    
class Department_T(models.Model):
    departmentID = models.CharField(max_length=5, primary_key=True)
    departmentName = models.CharField(max_length=30)
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)
    
class Program_T(models.Model):
    programID = models.CharField(max_length=5, primary_key=True)
    programName = models.CharField(max_length=30)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE, default='N/A')
    
class Student_T(models.Model):
    studentID = models.CharField(max_length=7, primary_key=True)
    fname = models.CharField(max_length=30, null=True)
    lname = models.CharField(max_length=30, null=True)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE, default='N/A')
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=30, null=True)
    
class Faculty_T(models.Model):
    facultyID = models.CharField(max_length=4, primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, null=True)
    dateOfBirth = models.DateField(null=True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=30, null=True)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)
    
class Course_T(models.Model):
    courseID = models.CharField(max_length=7, primary_key=True)
    courseName = models.CharField(max_length=30, null=True)
    noOfCredits = models.IntegerField()
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.courseID
    
class PLO_T(models.Model):
    ploNo = models.CharField(max_length=5, primary_key=True)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    details = models.CharField(max_length=50)
    
class CO_T(models.Model):
    coNo = models.IntegerField()
    plo = models.ForeignKey(PLO_T, on_delete=models.CASCADE, default='N/A')
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE, default='N/A')
    
class Section_T(models.Model):
    sectionNo = models.IntegerField()
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty_T, on_delete=models.CASCADE)
    
class Enrollment_T(models.Model):
    enrollmentID = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE, default=0)
    semester = models.CharField(max_length=6)
    year = models.CharField(max_length=4)
    
class Assessment_T(models.Model):
    assessmentNo = models.AutoField(primary_key=True)
    marks = models.FloatField()
    co = models.ForeignKey(CO_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE, default=0)

class Evaluation_T(models.Model):
    evaluationNo = models.AutoField(primary_key=True)
    obtainedMarks = models.FloatField()
    assessment = models.ForeignKey(Assessment_T, on_delete=models.CASCADE, default='N/A')
    enrollment = models.ForeignKey(Enrollment_T, on_delete=models.CASCADE, default=0)
    # student = models.ForeignKey(Student_T, on_delete=models.CASCADE, default='N/A')