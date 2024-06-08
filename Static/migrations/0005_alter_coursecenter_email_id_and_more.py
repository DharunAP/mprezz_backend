# Generated by Django 5.0.6 on 2024-06-05 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Static', '0004_remove_coursecenter_phonenumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecenter',
            name='email_id',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='coursecenter',
            name='institution_age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='coursecenter',
            name='institution_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coursecenter',
            name='owner_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coursecenter',
            name='password',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='coursecenter',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='student',
            name='current_role',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='email_id',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]