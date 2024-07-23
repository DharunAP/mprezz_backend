from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import Student,CourseCenter,CourseDetails, Enrollment
from Authentication.jwtValidation import *

@api_view(['GET'])
def getAllCourseCenters(request):
    try:
        courceCenters = CourseCenter.objects.all()
        data = []
        for value in courceCenters:
            index = dict()
            index['id'] = value.id
            index['institution_name'] = value.institution_name
            index['owner_name'] = value.owner_name
            index['address'] = value.location
            index['location'] = [value.lattitude, value.longitude]
            index['email'] = value.email_id
            index['phone_number'] = value.phone_number
            index['age'] = value.institution_age
            index['domain'] = value.domain
            index['rating'] = value.rating
            data.append(index)
        return Response({'message':'success','data':data},status=200)
    except Exception as e:
        return Response({'message':str(e)},status=500)

@api_view(['GET'])
def getAllCourses(request):
    try:
        try:
            courses = CourseDetails.objects.filter(institution_id=request.data['courseCenter'])
        except:
            courses = CourseDetails.objects.all()
        data = []
        for value in data:
            index = dict()
            index['cource_name'] = value.cource_name
            index['institution'] = value.institution
            index['price'] = value.price
            index['total_seats'] = value.no_of_seats
            index['certification'] = value.certification
            index['location'] = value.location
            index['filled_seats'] = value.filled_seats
            data.append(index)
        return Response({'message':'successfull','data':data},status=200)
    except Exception as e:
        return Response({'message':'Error '+str(e)},status=500)

@api_view(['POST'])
def getAllEnrolledStudents(request,id):
    try:
        return
    except Exception as e:
        return

@api_view(['GET'])
def getAllEnrolledCourses(request):
    try:
        validation_response = validate_token(request)  # validating the requested user using authorization headder
        if validation_response is not None:
            return validation_response

        try:
            userDetails = getUserDetails(request)  # getting the details of the requested user
            if userDetails['type']!='Student':  # chekking weather he is allowed inside this endpoint or not
                return Response({'message':'ACCESS_DENIED'},status=400)
        except Exception as error:
            print(error)
            return Response({'message':'Error authorizing the user try logging in again'})   
        courses = Enrollment.objects.filter(student_id = userDetails['id'])
        data = []
        for value in courses:
            index = dict()
            index['cource_name'] = value.cource_name
            index['institution'] = value.institution
            index['price'] = value.price
            index['total_seats'] = value.no_of_seats
            index['certification'] = value.certification
            index['location'] = value.location
            index['filled_seats'] = value.filled_seats
            data.append(index)
            
        return Response({'message':'success','data':data},status=200)
    except Exception as e:
        return Response({'message':'Error '+str(e)},status=500)