from django.urls import path
from .views import *

urlpatterns = [
    path('studentSignUp/',SignupStudent,name = 'SignupStudent'),
    path('courseCenterCreation/',CourseCenterCreation,name = 'CourseCenterCreationPage'),
    path('userLogin/',UserLogin,name = 'UserLoginPage')
]