from django.urls import path
from .views import *

urlpatterns = [
    path('courses/',ListAllCourses,name='course_listing'),
    path('enrollCourse/',enrollCourse,name='enroll_course'),
    path('getCourse/<str:id>',getCourse,name='get-course')
]