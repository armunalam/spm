# Generated by Django 3.1.4 on 2021-01-22 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20210122_0145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluation_t',
            old_name='enrollmentID',
            new_name='enrollment',
        ),
    ]