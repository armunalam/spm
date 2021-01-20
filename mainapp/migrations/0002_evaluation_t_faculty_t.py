# Generated by Django 3.1.4 on 2021-01-20 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation_T',
            fields=[
                ('evaluationNo', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('obtainedMarks', models.FloatField()),
                ('associatedCO', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_T',
            fields=[
                ('facultyID', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1)),
                ('dateOfBirth', models.DateField()),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=30)),
                ('departmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.department_t')),
            ],
        ),
    ]
