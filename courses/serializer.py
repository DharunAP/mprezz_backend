from rest_framework import serializers
from Static.models import CourseDetails
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetails
        fields = '__all__'