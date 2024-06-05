from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Static.models import Student,CourseCenter
from .Serializers import StudentSerializer,CourseCenterSerializer

@api_view(['POST'])
def SignupStudent(request):
    try:
        if Student.objects.filter(email=request.data['email']).exists():
            return Response({"message":"EMAIL_ALREADY_EXISTS"},status=400)
        serializer = StudentSerializer(data=request.data)
        valid=serializer.is_valid()
        if valid:
            # instance = Student.objects.create(email_id=request.data['email_id'],password=make_password(request.data['password']))
            # instance.save()
            serializer.save()
            return Response({"message":"Student created"},status=200)
        print(serializer.errors)
        return Response({"message":"Invalid Serializer"},status=400)
    except Exception as e:
        print(e)
        return Response({"message":"Error "+str(e)},status=500)

@api_view(['POST'])
def CourseCenterCreation(request):
    try:
        if CourseCenter.objects.filter(email=request.data['email']).exists():
            return Response({"message":"EMAIL_ALREADY_EXISTS"},status=400)
        serializer = CourseCenterSerializer(data=request.data)
        valid=serializer.is_valid()
        if valid:
            # instance = Student.objects.create(email_id=request.data['email_id'],password=make_password(request.data['password']))
            # instance.save()
            serializer.save()
            return Response({"message":"CourseCenter created"},status=200)
        print(serializer.errors)
        return Response({"message":"Invalid Serializer"},status=400)
    except Exception as e:
        print(e)
        return Response({"message":"Error "+str(e)},status=500)