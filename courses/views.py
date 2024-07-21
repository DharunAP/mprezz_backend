from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import CourseDetails, CourseCenter, Enrollment
from .serializer import CourseSerializer
from Authentication.jwtValidation import *
import datetime

def createCourse(data):
    try:
        # data['institution'] = CourseCenter.objects.get(id = data['institution'])
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Course Created Sucessfully'},status=200)
        return Response({'message':'Invalid credentials','error':serializer.errors},status=400)
    except Exception as error:
        return Response({'message':'Error creating a course','error':str(error)},status=500)

@api_view(['POST','GET'])
def ListAllCourses (request) :
    if request.method=='POST':
        return createCourse(request.data)
    try :
        print('all')

        courses = CourseDetails.objects.all()
        print(len(courses),'this is the length..')
        data_list = []

        for course in courses :
            start = course.start_date
            end = course.end_date
            data = dict()
            data['id'] = course.id
            data['course_name'] = course.course_name,
            # data['domain'] = course.domain,
            data['mode'] = course.mode,
            data['start_date'] = start.strftime('%d').lstrip('0') + ' ' + start.strftime('%B')
            data['end_date'] = end.strftime('%d').lstrip('0') + ' ' + end.strftime('%B')
            data['price'] = course.price,
            data['discount'] = course.discount,
            data['institution'] = course.institution.institution_name,
            data['location'] = course.location,
            # data['certification'] = course.certification,
            # data['no.of.seats'] = course.no_of_seats,
            # data['description'] = course.description,
            # data['expectations'] = course.expectations,
            # data['requirements'] = course.requirements

            data_list.append(data)
        return Response({'message' : 'Courses listed Successfully',
                        'Data' : data_list},status=200)

    except Exception as exp :
        print(exp)
        return Response ({'message' : 'Error while listing',
                          'Error' : str(exp)},status=500)

@api_view(['GET'])
def getCourse(request,id):
    try:
        course = CourseDetails.objects.get(id = id)
        start = course.start_date
        end = course.end_date
        data = dict()
        data['id'] = course.id
        data['course_name'] = course.course_name
        data['domain'] = course.domain
        data['mode'] = course.mode
        data['start_date'] = start.strftime('%d').lstrip('0') + ' ' + start.strftime('%B')
        data['end_date'] = end.strftime('%d').lstrip('0') + ' ' + end.strftime('%B')
        data['price'] = course.price
        data['discount'] = course.discount
        data['institution'] = course.institution.institution_name
        data['location'] = course.location
        data['certification'] = course.certification
        data['no_of_seats'] = course.no_of_seats
        data['filled_seats'] = course.filled_seats
        data['description'] = course.description
        data['expectations'] = course.expectations
        data['requirements'] = course.requirements
        return Response({'message':'Course details sent sucessfully','data':data},status=200)
    except Exception as error:
        return Response({'message':'Error '+str(error)},status=500)

@api_view(['POST'])
def enrollCourse(request):
    try:
        validation_response = validate_token(request)  # validating the requested user using authorization headder
        if validation_response is not None:
            return validation_response

        try:
            userDetails = getUserDetails(request)  # getting the details of the requested user
            if userDetails['type']!='Student':  # chekking weather he is allowed inside this endpoint or not
                return Response({'message':'Only Students can enroll for a course'},status=400)
        except Exception as error:
            print(error)
            return Response({'message':'Error authorizing the user try logging in again'})   
        check = Enrollment.objects.filter(
            student_id = userDetails['id'],
            course_id = request.data['course'],
        )
        if check.exists():
            return Response({'message':'Already Enrolled in the course'},status=400)
        Enrollment.objects.create(
            student_id = userDetails['id'],
            course_id = request.data['course'],
        )
        return Response({'message':'Course Enrolled'},status=200)
    except Exception as error:
        return Response({'message':'Error while enrolling','error':str(error)},status=500)

@api_view(['POST'])
def paidForEnrollment(request):
    try:
        instance = Enrollment.objects.get(id = request.data['Enrollment_id'])
        instance.is_amount_paid = True
        # implement code for updating filled seats in CourseDetails model
        instance.save()
        return Response({'message':'sucessfully bought the course'},status=200)
    except Exception as error:
        return Response({'message':'Error in paying the enrollment','error':str(error)},status=500)