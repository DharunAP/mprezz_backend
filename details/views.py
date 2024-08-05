from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import Student,CourseCenter,CourseDetails, Enrollment
from core.chiper import encryptData, decryptData
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

@api_view(['GET'])
def getAllEnrolledStudents(request,id):
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
        course = CourseDetails.objects.get(id = id)
        enrollments = Enrollment.objects.filter(course=course)
        stud_list=[]
        for en in enrollments:
            value=dict()
            if en.course.institution==userDetails['user']:
                student = en.student
                value['name'] = student.first_name + " " + student.last_name
                value['id'] = encryptData(student.id)
                value['phone_number'] = student.phone_number
                value['email_id'] = student.email_id
                value['organization'] = student.organization
                stud_list.append(value)
        
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
        return Response({'message':'students details sent sucessfully.','data':data,'students_list':stud_list},status=200)
    except Exception as e:
        print(str(e))
        return Response({'message':'Error sending details.','Error':str(e)},status=500)

@api_view(['GET'])
def studentProfile(request):
    try:
        print(request)
        id = request.GET.get('id')
        try:
            student = Student.objects.get(id=decryptData(id))
        except:
            return Response({'message':'Student does not exists'},status=404)
        data = dict()
        data['name']= student.first_name +' '+ student.last_name
        data['gender']= student.gender
        data['dob']= student.dateOfBirth
        # data['email_id']= student.email_id
        # data['phone_number']= student.phone_number
        data['city']= student.city
        data['organization']= student.organization
        data['domain']= student.domain
        return Response({'message':'Details sent sucessfully','data':data},status=200)
    except Exception as e:
        print(str(e))
        return Response({'message':'Error retriving profile details','error':str(e)},status=500)

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
            value = value.course
            start = value.start_date
            end = value.end_date
            index = dict()
            index['course_name'] = value.course_name
            index['institution'] = str(value.institution)
            index['mode'] = value.mode
            index['location'] = value.location
            index['start_date'] = start.strftime('%d').lstrip('0') + ' ' + start.strftime('%B')
            index['end_date'] = end.strftime('%d').lstrip('0') + ' ' + end.strftime('%B')
            print(index)
            data.append(index)
            
        return Response({'message':'success','data':data},status=200)
    except Exception as e:
        return Response({'message':'Error '+str(e)},status=500)