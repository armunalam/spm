# Generated by Django 3.1.4 on 2021-01-21 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20210121_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_t',
            name='fname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student_t',
            name='lname',
            field=models.CharField(max_length=30, null=True),
        ),
    ]