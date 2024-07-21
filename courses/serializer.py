from rest_framework import serializers
from core.models import CourseDetails
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetails
        fields = '__all__'