from django.urls import path
from .views import *
from core.routes import *

urlpatterns = [
    path('faculty_register/',registerFaculty,name="Register-Faculty"),
    path('institure_request/',createRequest,name="Institute-Request")
]