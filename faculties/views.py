import pandas as pd
import os
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import FileResponse,HttpResponse
from rest_framework.response import Response
from core.models import Faculty
from .serializer import FacultySerializer, FacultyRequestSerializer
from django.shortcuts import render
from dotenv import load_dotenv
load_dotenv()
@api_view(['POST'])
def registerFaculty(request):
    try:
        ser = FacultySerializer(data=request.data)
        if(ser.is_valid()):
            ser.save()
            df = pd.DataFrame([dict(ser.data)])
            file_path = os.path.join(settings.MEDIA_ROOT, 'faculties.xlsx')
            if os.path.exists(file_path):
                existing_df = pd.read_excel(file_path, engine='openpyxl')
                df = pd.concat([existing_df, df], ignore_index=True)

            df.to_excel(file_path, index=False, engine='openpyxl')

        else:
            return Response({'message':'Invalid Data','error':ser.errors},status=400)
        return Response({'message':'Faculty created sucessfully'},status=200)
    except Exception as error:
        return Response({'message':'Faculty not created.','error':str(error)},status=500)

@api_view(['POST'])
def createRequest(request):
    try:
        ser = FacultyRequestSerializer(data = request.data)
        if ser.is_valid():
            ser.save()
            return Response({'message':'Request saved sucessfully'},status=200)
        return Response({'message':'Invalid Data','error':ser.errors},status=400)
    except Exception as error:
        return Response({'message':'Error creating the request','Error':str(error)},status=500)

def download_excel(request):
    # Define the path to the existing Excel file
    if request.method == 'POST':
        print(request.POST.get('password'),os.environ['PASSWORD'])
        if request.POST.get('password')==os.environ['PASSWORD']:
            file_path = os.path.join(settings.MEDIA_ROOT, 'faculties.xlsx')

            # Check if the file exists
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='faculties.xlsx')
            else:
                # Handle the case where the file doesn't exist
                return HttpResponse("File not found.", status=404)
        return HttpResponse("Invalid Password", status=403)
    return render(request,'template/getData.html')