# Generated by Django 4.2 on 2024-07-23 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_enrollment_is_amount_paid_enrollment_payment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]
