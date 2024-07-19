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