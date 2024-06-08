from django.urls import path
from .views import *

urlpatterns = [
    path('list-all-courses/',ListAllCourses,name='course_listing')
]