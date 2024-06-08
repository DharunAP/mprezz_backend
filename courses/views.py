from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Static.models import CourseDetails

@api_view(['GET'])
def ListAllCourses (request) :
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
