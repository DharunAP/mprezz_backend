# Generated by Django 5.0.6 on 2024-06-04 15:44

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Static', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institutionName', models.CharField(max_length=100)),
                ('ownerName', models.CharField(verbose_name=builtins.max)),
                ('location', models.CharField()),
                ('email', models.EmailField(max_length=254)),
                ('PhoneNumber', models.CharField(max_length=15)),
                ('rating', models.FloatField()),
                ('institutionAge', models.IntegerField()),
                ('domain', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateField()),
                ('gender', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('PhoneNumber', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('currentRole', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
                ('organization', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Students',
        ),
    ]
