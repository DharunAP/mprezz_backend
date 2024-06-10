from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Static.models import CourseDetails, CourseCenter, Enrollment
from .serializer import CourseSerializer

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

        for courses in courses :

            data = dict()
            data['course_name'] = courses.course_name,
            data['domain'] = courses.domain,
            data['mode'] = courses.mode,
            data['start_date'] = courses.start_date,
            data['end_date'] = courses.end_date,
            data['price'] = courses.price,
            data['discount'] = courses.discount,
            data['institution'] = courses.institution,
            data['location'] = courses.location,
            data['certification'] = courses.certification,
            data['no.of.seats'] = courses.no_of_seats,
            data['description'] = courses.description,
            data['expectations'] = courses.expectations,
            data['requirements'] = courses.requirements

            data_list.append(data)
        return Response({'message' : 'Courses listed Successfully',
                        'Data' : data_list},status=200)

    except Exception as exp :
        return Response ({'message' : 'Error while listing',
                          'Error' : str(exp)},status=500)

@api_view(['POST'])
def enrollCourse(request):
    try:
        Enrollment.objects.create(
            student_id = request.data['student'],
            course = request.data['course'],
        )
        return Response({'message':'Course Enrolled'},status=200)
    except Exception as error:
        return Response({'message':'Error while enrolling'},status=500)