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
