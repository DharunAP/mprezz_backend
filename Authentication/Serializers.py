from rest_framework import serializers
from Static.models import Student,CourseCenter

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CourseCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCenter
        fields = '__all__'