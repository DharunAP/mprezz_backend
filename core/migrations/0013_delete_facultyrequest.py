# Generated by Django 4.2 on 2024-08-27 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_faculty_email_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FacultyRequest',
        ),
    ]