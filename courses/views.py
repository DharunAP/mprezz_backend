from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Static.models import CourseDetails

api_view(['GET'])
def ListAllCourses (request) :
    print('all')

    courses = CourseDetails.objects.all()

