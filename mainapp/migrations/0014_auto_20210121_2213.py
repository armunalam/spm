# Generated by Django 3.1.4 on 2021-01-21 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20210121_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment_t',
            name='enrollmentID',
        ),
        migrations.RemoveField(
            model_name='evaluation_t',
            name='studentID',
        ),
        migrations.AddField(
            model_name='evaluation_t',
            name='enrollmentID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='mainapp.enrollment_t'),
        ),
    ]
