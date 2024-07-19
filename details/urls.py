from django.urls import path
from .views import *
urlpatterns = [
    path('getAllCourseCenters/',getAllCourseCenters,name = 'get-all-cource-centers'),
    path('getAllCourses/',getAllCourses,name='get-all-cources'),
    path('studentEnrolledCourses/',getAllEnrolledCourses,name='get-all-enrolled-courses')
]