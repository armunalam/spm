# Generated by Django 3.1.4 on 2021-01-20 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_enrollment_t_section_t'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment_T',
            fields=[
                ('assessmentNo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('marksObtained', models.FloatField()),
                ('associatedCO', models.CharField(max_length=5)),
                ('enrollmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.enrollment_t')),
                ('evaluationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.evaluation_t')),
            ],
        ),
    ]
