from django.urls import path
from .views import *

urlpatterns = [
    path('create_order/', create_order),
    path('verify/payment/', verify_payment),
    path('createEnrollment/',creteEnrollment)
]