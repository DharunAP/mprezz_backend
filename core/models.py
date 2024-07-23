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
    is_email_verified = models.BooleanField(default=False)
    def __str__(self):
        return str(self.first_name)

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
    is_email_verified = models.BooleanField(default=False)
    def __str__(self):
        return str(self.institution_name)
    
class CourseDetails (models.Model) :
    course_name = models.CharField(max_length=300)
    domain = models.CharField(max_length=200)
    mode = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.CharField(max_length=100)
    discount = models.FloatField()
    institution = models.ForeignKey(CourseCenter,on_delete=models.CASCADE)
    location = models.CharField(max_length=500)
    certification = models.BooleanField(default=False)
    no_of_seats = models.IntegerField()
    filled_seats = models.IntegerField(default = 0)
    description = ArrayField(models.TextField())
    expectations = ArrayField(models.TextField())
    requirements = ArrayField(models.TextField())

    def __str__(self) :
        return str(self.course_name) + ' by ' + str(self.institution)

class Enrollment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetails,on_delete=models.CASCADE)
    is_amount_paid = models.BooleanField(default=False)

from django.db import models
from django.db import models

class Payments(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    payment_method = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    order_id = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.payment_id} - {self.status}"


class AuthToken(models.Model) :
    user_type = models.CharField(max_length=100)
    referenceId = models.IntegerField()
    jwt_token = models.CharField(primary_key=True,max_length=500)
    created_date = models.DateField(auto_now_add=True)