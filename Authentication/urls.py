from django.urls import path
from .views import *

urlpatterns = [
    path('studentSignUp/',SignupStudent,name = 'SignupStudent'),
    path('courseCenterCreation/',CourseCenterCreation)
]