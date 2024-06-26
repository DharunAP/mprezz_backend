# Generated by Django 4.2 on 2024-06-08 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Static', '0008_alter_coursedetails_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_amount_paid', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Static.coursedetails')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Static.student')),
            ],
        ),
    ]
