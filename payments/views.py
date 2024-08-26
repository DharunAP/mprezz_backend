from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from payments.client_razorpay import client
from rest_framework.decorators import api_view
from core.models import Payments, Enrollment, CourseDetails, AccountDetails, CourseCenter
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from django.utils import timezone
from Authentication.jwtValidation import validate_token, getUserDetails
import requests
from requests.auth import HTTPBasicAuth
import json
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

            response = clientOBJ.utility.verify_webhook_signature(
                data, signature, webhook_secret)

            if response:
                payment_data = jsonData['payload']['payment']['entity']

                created_at = timezone.datetime.fromtimestamp(
                    payment_data['created_at']).astimezone()

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
        # getting the details of the requested user
        userDetails = getUserDetails(request)
        # chekking weather he is allowed inside this endpoint or not
        if userDetails['type'] != 'Student':
            print('not a stud')
            return Response({'message': "ACCESS DENIED"}, status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message': 'Email not verified'}, status=400)
    except Exception as error:
        print(error)
        return Response({'message': 'Error authorizing the user try logging in again', 'error': str(error)}, status=500)

    try:
        amount = request.data.get("amount")
        currency = request.data.get("currency")
        transfer_currency = request.data.get("transfer_currency")
        transfer_percentage = 10
        course_center_id = request.data.get("course_center_id")

        
        course_center = CourseCenter.objects.get(id=course_center_id)
        account_details = AccountDetails.objects.get(CourseCenter=course_center)

        order_payload = {
            'amount': int(amount) * 100,
            'currency': currency,
            'payment_capture': '1',  # Auto capture
            'transfers': [{
                "account": account_details['linked_acount_id'],
                "amount": (int(amount) * 100) * (transfer_percentage//100),
                "currency": transfer_currency, 
                "on_hold": 0
        }],
        }

        # Create order in Razorpay
        order = clientOBJ.order.create(data=order_payload)

        return Response(order, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"order": None, "response": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def creteEnrollment(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        # getting the details of the requested user
        userDetails = getUserDetails(request)
        # chekking weather he is allowed inside this endpoint or not
        if userDetails['type'] != 'Student':
            return Response({'message': "ACCESS DENIED"}, status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message': 'Email not verified'}, status=400)
    except Exception as error:
        print(error)
        return Response({'message': 'Error authorizing the user try logging in again'})
    try:
        payment = Payments.objects.filter(
            payment_id=request.data['payment_id'])
        if not payment.exists():
            return Response({'message': 'Payment does not exists'}, status=400)
        payment = payment[0]
        course = CourseDetails.objects.filter(id=request.data['course_id'])
        if not course.exists():
            return Response({'message': 'Course does not exists'}, status=400)
        course = course[0]
        print(course)
        Enrollment.objects.create(
            student=userDetails['user'],
            payment=payment,
            course=course
        )
        return Response({'message': 'Course Enrolled sucessfully'}, status=200)
    except Exception as e:
        print(str(e))
        return Response({'message': 'Error '+str(e)}, status=500)


@api_view(["POST"])
def createLinkedAccount(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        userDetails = getUserDetails(request)  # getting the details of the requested user
        if userDetails['type']!='Coursecenter':      # chekking weather he is allowed inside this endpoint or not
            print('Not a course center')
            return Response({'message':"ACCESS DENIED"},status=400)
        print(userDetails)
        if not userDetails['user'].is_email_verified:
            return Response({'message':'Email not verified'},status=400)
    except Exception as error:
        print(error)
        return Response({'message':'Error authorizing the user try logging in again','error':str(error)},status=500)

    try:
        authObject = HTTPBasicAuth(
            os.getenv('RAZORPAY_API_KEY'), os.getenv('RAZORPAY_API_SECRET'))
        headers = {"Content-type": "application/json"}

        account_url = 'https://api.razorpay.com/v2/accounts/'
        stake_holder_api_url = f"https://api.razorpay.com/v2/accounts/"

        data = json.loads(request.body)

        linked_account_payload = {
            "email": data.get("email"),
            "phone": data.get("phone"),
            "type": "route",
            "legal_business_name": data.get("business_name"),
            "business_type": "partnership",
            "contact_name": data.get("beneficiary_name"),
            "profile": {
                "category": data.get("profile").get("category"),
                "subcategory": data.get("profile").get("subcategory"),
                "addresses": {
                    "registered": {
                        "street1": data.get("address").get("street1"),
                        "street2": data.get("address").get("street2"),
                        "city": data.get("address").get("city"),
                        "state": data.get("address").get("state"),
                        "postal_code": data.get("address").get("postal_code"),
                        "country": data.get("address").get("country")
                    }
                }
            },
            "legal_info": {
                "pan": data.get("legal_info").get("pan")
            },
        }


        # # creates a linked account for the course center
        response = requests.post(
            account_url, json=linked_account_payload, auth=authObject, headers=headers)

        linked_account = response.json()

        # linked_account_id = "acc_Op2Zs0s4bcFHkV"

        linked_account_id = linked_account['id']

        # # creates a stakeholder object for the course center
        stake_holder_payload = {
            "name": data.get("beneficiary_name"),
            "email": data.get("email"),
            "addresses": {
                "residential": {
                    "street": data.get("address").get("street1"),
                    "city": data.get("address").get("city"),
                    "state": data.get("address").get("state"),
                    "postal_code": data.get("address").get("postal_code"),
                    "country": data.get("address").get("country")
                }
            },
        }
        response = requests.post(stake_holder_api_url + f"{linked_account_id}/stakeholders", json=stake_holder_payload, auth=authObject, headers=headers)


        # create product configuration
        product_config_data = {
            "product_name": "route",
            "tnc_accepted": bool(data.get("tnc_accepted"))
        }
        response = requests.post(account_url + f"{linked_account_id}/products", auth=authObject, headers=headers, json=product_config_data)

        product_config_id = response.json()['id']


        # update product cofiguration
        update_product_data = {
            "settlements": {
                "account_number": data.get("settlements").get("account_number"),
                "ifsc_code": data.get("settlements").get("ifsc_code"),
                "beneficiary_name": data.get("beneficiary_name")
            },
            "tnc_accepted": bool(data.get("tnc_accepted"))
        }
        response = requests.patch(
            account_url + f"{linked_account_id}/products/{product_config_id}/", headers=headers, json=update_product_data, auth=authObject)

        product_details = response.json()

        # stores it in the database
        AccountDetails.objects.create(
            CourseCenter= userDetails['user'],
            business_name=data.get("legal_business_name"),
            business_type=data.get("business_type"),
            account_number=data.get("settlements").get("account_number"),
            ifsc_code=data.get("settlements").get("ifsc_code"),
            beneficiary_name=data.get("beneficiary_name"),
            linked_acount_id=product_details['account_id'],
            product_config_id=product_details['id'],
       )

        return Response({"message": f"Payment route initialized for Linked account {linked_account_id}!"}, status=status.HTTP_200_OK)

    except Exception as e:
        print(str(e))
        return Response({'message': 'Error '+str(e)},status=500)
    

