from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from payments.client_razorpay import client
from rest_framework.decorators import api_view
from core.models import Payments
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import datetime
from django.utils import timezone

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

