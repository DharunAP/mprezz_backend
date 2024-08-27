import pandas as pd
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Faculty
from .serializer import FacultySerializer

@api_view(['POST'])
def registerFaculty(request):
    try:
        ser = FacultySerializer(data=request['data'])
        if(ser.is_valid()):
            ser.save()
        else:
            return Response({'message':'Invalid Data','error':ser.errors},status=400)
        return Response({'message':'Faculty created sucessfully'},status=200)
    except Exception as error:
        return Response({'message':'Faculty not created.','error':str(error)},status=500)