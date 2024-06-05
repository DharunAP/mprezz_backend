from django.db import models
from django.contrib.postgres.fields import ArrayField

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=25)
    email_id = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.TextField()
    current_role = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    def __str__(self):
        return str(self.firstname)


class CourseCenter(models.Model):
    institution_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    lattitude = models.CharField(max_length=100,default='13.0843')
    longitude = models.CharField(max_length=100,default='80.2705')
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    rating = models.FloatField()
    institution_age = models.IntegerField()
    domain = ArrayField(models.CharField(max_length=100),null=True,blank=True)
    def __str__(self):
        return str(self.institutionName)