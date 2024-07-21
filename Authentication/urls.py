from django.urls import path
from .views import *
from core.routes import *

urlpatterns = [
    path('studentSignUp/',SignupStudent,name = 'SignupStudent'),
    path('courseCenterCreation/',CourseCenterCreation,name = 'CourseCenterCreationPage'),
    path('userLogin/',UserLogin,name = 'UserLoginPage'),
    path(VERIFY_MAIL_ROUTE_STUDENT,VerifyStudent,name='verify student mail'),
    path(VERIFY_MAIL_ROUTE_COURSE_CENTER,VerifyCourseCenter,name='verify course center mail'),
    path(CHANGE_PASSWORD,change_password,name='change password')
]