from rest_framework.serializers import ModelSerializer
from core.models import Faculty,FacultyRequest

class FacultySerializer(ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class FacultyRequestSerializer(ModelSerializer):
    class Meta:
        model = FacultyRequest
        fields = '__all__'