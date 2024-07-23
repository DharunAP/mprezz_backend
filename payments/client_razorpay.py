from razorpay import Client
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def client():
    api_key = os.getenv('RAZORPAY_API_KEY')
    api_secret = os.getenv('RAZORPAY_API_SECRET')
    try:
        client = Client(auth=(api_key,api_secret))
        client.set_app_details({"title": "Django", "version": "3.0.0"})
        print("Client initialized")
        return client
    except Exception as e:
        print(e)
        return None