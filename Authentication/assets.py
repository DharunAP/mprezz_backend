from django.core.mail import send_mail
import os
from django.template.loader import render_to_string,get_template

def sendVerificationMail(url, email_id):
    print(url)
    template = get_template('template/verify_mail.html').render({'BASE_URL':os.getenv('BACKEND_URL'),'verifyMail':url})
    send_mail(
        subject="Verify your mail by clicking the below link",  # subject in the sending mail
        from_email=os.getenv('email_host_id'),                  # sender mail
        html_message= template,                                 # html template
        message=os.getenv('BACKEND_URL')+url,                   # message in the mail
        recipient_list=[email_id,]                              # recipient mail id
    )
    print("mail sent")


def sendPasswordMail(url, email_id):
    print(url)
    template = get_template('template/forget_password.html').render({'BASE_URL':os.getenv('BACKEND_URL'),'URL':url})
    send_mail(
        subject="Change your password by clicking the below link",  # subject in the sending mail
        from_email=os.getenv('email_host_id'),                  # sender mail
        html_message= template,                                 # html template
        message=os.getenv('BACKEND_URL')+url,                   # message in the mail
        recipient_list=[email_id,]                              # recipient mail id
    )
    print("mail sent")

def sendRequestMail(email_id):
    template = get_template('template/request_mail.html').render()
    send_mail(
        subject="Request received",  # subject in the sending mail
        from_email=os.getenv('email_host_id'),                  # sender mail
        html_message= template,                                 # html template
        message="Request received",                   # message in the mail
        recipient_list=[email_id,]                              # recipient mail id
    )

def notifyRequest(data):
    template = get_template('template/notify_request.html').render({"name":data['name'],"email":data['email'],'phone':data['phone'],"inst":data['inst'],'web':data['web']})
    send_mail(
        subject=f"{data['inst']} has a new request for you",  # subject in the sending mail
        from_email=os.getenv('email_host_id'),                  # sender mail
        html_message= template,                                 # html template
        message="New Request",                   # message in the mail
        recipient_list=[os.getenv('email_host_id'),]               # recipient mail id
    )