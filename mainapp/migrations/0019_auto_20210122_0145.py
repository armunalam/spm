# Generated by Django 3.1.4 on 2021-01-22 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_auto_20210122_0128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation_t',
            name='student',
        ),
        migrations.AddField(
            model_name='evaluation_t',
            name='enrollmentID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='mainapp.enrollment_t'),
        ),
    ]