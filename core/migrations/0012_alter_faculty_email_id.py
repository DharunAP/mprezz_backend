# Generated by Django 4.2 on 2024-08-27 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_faculty_facultyrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='email_id',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
