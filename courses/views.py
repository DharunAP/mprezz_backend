from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import CourseDetails, CourseCenter, Enrollment
from core.chiper import encryptData, decryptData
from .serializer import CourseSerializer
from Authentication.jwtValidation import *
from Authentication.jwtValidation import validate_token,getUserDetails
import datetime

def createCourse(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        userDetails = getUserDetails(request)  # getting the details of the requested user
        if userDetails['type']!='CourseProvider':      # chekking weather he is allowed inside this endpoint or not
            return Response({'message':"ACCESS DENIED"},status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message':'Email not verified'},status=400)
    except Exception as error:
        print(error)
        return Response({'message':'Error authorizing the user try logging in again'})
    try:
        data = request.data
        data['institution'] = userDetails['id']
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Course Created Sucessfully'},status=200)
        print(serializer.errors)
        return Response({'message':'Invalid credentials','error':serializer.errors},status=400)
    except Exception as error:
        return Response({'message':'Error creating a course','error':str(error)},status=500)

@api_view(['POST','GET'])
def ListAllCourses (request) :
    if request.method=='POST':
        return createCourse(request)
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

@api_view(['GET','POST'])
def GetMyCourse(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        userDetails = getUserDetails(request)  # getting the details of the requested user
        # if userDetails['type']!='Student':      # chekking weather he is allowed inside this endpoint or not
            # return Response({'message':"ACCESS DENIED"},status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message':'Email not verified'},status=400)
    except Exception as error:
        print(error)
        return Response({'message':'Error authorizing the user try logging in again'})

    # Authentication over
    try:
        if userDetails['type']=='CourseProvider':
            courses = CourseDetails.objects.filter(institution=userDetails['user'])
        elif userDetails['type']=='Student':
            courses=[]
            enrollments = Enrollment.objects.filter(student=userDetails['user'])
            for enrollment in enrollments:
                course = CourseDetails.objects.get(id=enrollment.course_id)
                courses.append(course)
        data_list = []

        for course in courses :
            start = course.start_date
            end = course.end_date
            data = dict()
            data['id'] = course.id
            data['course_name'] = course.course_name
            data['mode'] = course.mode
            data['start_date'] = start.strftime('%d').lstrip('0') + ' ' + start.strftime('%B')
            data['end_date'] = end.strftime('%d').lstrip('0') + ' ' + end.strftime('%B')
            data['price'] = course.price
            data['discount'] = course.discount
            data['institution'] = course.institution.institution_name
            data['location'] = course.location

            data_list.append(data)
        return Response({'message':'courses sent sucessfully','data':data_list},status=200)
    except Exception as e:
        return Response({'message':'Error '+str(e)},status=500)

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
            if not userDetails['user'].is_email_verified:
                return Response({'message':'Email not verified'},status=400)
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