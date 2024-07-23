from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from payments.client_razorpay import client
from rest_framework.decorators import api_view
from core.models import Payments, Enrollment, CourseDetails
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from django.utils import timezone
from Authentication.jwtValidation import validate_token, getUserDetails

clientOBJ = client()

@csrf_exempt
@api_view(['POST'])
def verify_payment(request):
    if request.method == 'POST':
        try:
            signature = request.headers.get('x-razorpay-signature')

            data = request.body.decode('utf-8')
            jsonData = json.loads(data)

            webhook_secret = os.getenv('WEBHOOK_SECRET')

            response = clientOBJ.utility.verify_webhook_signature(data, signature, webhook_secret)

            if response:
                payment_data = jsonData['payload']['payment']['entity']

                created_at = timezone.datetime.fromtimestamp(payment_data['created_at']).astimezone()

                created = Payments.objects.create(
                    payment_id=payment_data['id'],
                    amount=payment_data['amount'] / 100, 
                    status=payment_data['status'],
                    payment_method=payment_data['method'],
                    email=payment_data.get('email', ''),
                    contact=payment_data.get('contact', ''),
                    order_id=payment_data.get('order_id', ''),
                    created_at=created_at
                )

            if created:
                return Response({'status': 'ok', 'message': 'payment_created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'ok', 'message': 'payment_updated'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failure', 'message': 'payment_failed'}, status=400)

@api_view(["POST"])
def create_order(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        userDetails = getUserDetails(request)  # getting the details of the requested user
        if userDetails['type']!='Student':      # chekking weather he is allowed inside this endpoint or not
            return Response({'message':"ACCESS DENIED"},status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message':'Email not verified'},status=400)
    except Exception as error:
        print(error)
        return Response({'message':'Error authorizing the user try logging in again','error':str(error)},status=500)
    try:
        amount = request.data.get("amount")
        currency = request.data.get("currency")

        order_payload = {
            'amount': int(amount) * 100,  
            'currency': currency,
            'payment_capture': '1'  # Auto capture
        }

        # Create order in Razorpay
        order = clientOBJ.order.create(data=order_payload)

        return Response(order,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"order" : None, "response": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def creteEnrollment(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        userDetails = getUserDetails(request)  # getting the details of the requested user
        if userDetails['type']!='Student':      # chekking weather he is allowed inside this endpoint or not
            return Response({'message':"ACCESS DENIED"},status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message':'Email not verified'},status=400)
    except Exception as error:
        print(error)
        return Response({'message':'Error authorizing the user try logging in again'})
    try:
        payment = Payments.objects.filter(payment_id=request.data['payment_id'])
        if not payment.exists():
            return Response({'message':'Payment does not exists'},status=400)
        course = CourseDetails.objects.filter(id = request.data['id'])
        if not course.exists():
            return Response({'message':'Course does not exists'},status=400)
        Enrollment.objects.create(
            student=userDetails['user'],
            payment=payment,
            course=course
        )
        return Response({'message':'Course Enrolled sucessfully'},status=200)
    except Exception as e:
        return Response({'message':'Error '+str(e)},status=500)