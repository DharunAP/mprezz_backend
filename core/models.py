from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

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
    rating = models.FloatField(default=0)
    institution_age = models.IntegerField()
    domain = ArrayField(models.CharField(max_length=100),null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    def __str__(self):
        return str(self.institution_name)


class AccountDetails(models.Model):
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    account_number = models.CharField(max_length=16)
    ifsc_code = models.CharField(max_length=11)
    beneficiary_name = models.CharField(max_length=100)
    linked_acount_id = models.CharField(max_length=100, default=None)
    product_config_id = models.CharField(max_length=100, default=None)
    CourseCenter = models.OneToOneField(CourseCenter,on_delete=models.CASCADE)

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

class Payments(models.Model):
    payment_id = models.CharField(max_length=100, unique=True, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    payment_method = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    order_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)  # Ensure timezone-aware datetime

    def __str__(self):
        return f"{self.payment_id} - {self.status}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetails,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payments,on_delete=models.CASCADE)

class AuthToken(models.Model) :
    user_type = models.CharField(max_length=100)
    referenceId = models.IntegerField()
    jwt_token = models.CharField(primary_key=True,max_length=500)
    created_date = models.DateField(auto_now_add=True)

class Faculty(models.Model):
    first_name =  models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_id = models.EmailField()
    qualification = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    institution = models.CharField(max_length=150)
    place = models.CharField(max_length=100)
    experience = models.IntegerField()
    linkedIn_profile = models.TextField(null=True, blank=True)

    address = models.TextField()
    pin_code = models.CharField(max_length=6)
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    cv_link = models.TextField()

class FacultyRequest(models.Model):
    institute_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    website_link = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField()

    # Details of Single Point of contact
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6,choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')])
    phone_number = models.CharField(max_length=13)
    email_id = models.EmailField