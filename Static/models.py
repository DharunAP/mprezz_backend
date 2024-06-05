from django.db import models
from django.contrib.postgres.fields import ArrayField

class Student(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    dateOfBirth = models.DateField()
    gender = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    PhoneNumber = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.TextField()
    currentRole = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    def __str__(self):
        return str(self.firstname)


class CourseCenter(models.Model):
    institutionName = models.CharField(max_length=100)
    ownerName = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    lattitude = models.CharField(max_length=100,default='13.0843')
    longitude = models.CharField(max_length=100,default='80.2705')
    email = models.EmailField()
    PhoneNumber = models.CharField(max_length=15)
    rating = models.FloatField()
    institutionAge = models.IntegerField()
    domain = ArrayField(models.CharField(max_length=100),null=True,blank=True)
    # def __str__(self):
    #     return institutionName