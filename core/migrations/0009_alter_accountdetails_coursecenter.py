# Generated by Django 4.2 on 2024-08-19 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_accountdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetails',
            name='CourseCenter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.coursecenter'),
        ),
    ]