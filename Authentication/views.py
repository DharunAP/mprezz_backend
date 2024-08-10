from rest_framework.response import Response
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from core.models import Student,CourseCenter
from .Serializers import StudentSerializer,CourseCenterSerializer
from .jwtValidation import *
from .assets import sendVerificationMail, sendPasswordMail
from core.chiper import encryptData,decryptData
from core.routes import VERIFY_MAIL_ROUTE_COURSE_CENTER,VERIFY_MAIL_ROUTE_STUDENT
from .jwtValidation import validate_token, getUserDetails

@api_view(['POST'])
def SignupStudent(request):
    try:
        if Student.objects.filter(email_id=request.data['email_id']).exists():
            return Response({"message":"EMAIL_ALREADY_EXISTS"},status=400)
        serializer = StudentSerializer(data=request.data)
        valid=serializer.is_valid()
        if valid:
            # instance = Student.objects.create(email_id=request.data['email_id'],password=make_password(request.data['password']))
            # instance.save()
            serializer.save()
            instance = Student.objects.get(email_id=request.data['email_id'])
            jwt_token = get_or_create_jwt(instance, 'Student', instance.email_id)
            encryptedID = encryptData(instance.id)
            sendVerificationMail(VERIFY_MAIL_ROUTE_STUDENT+"?id="+encryptedID,request.data['email_id']) # sending the verification mail
            return Response({"message":"Student created","token":str(jwt_token),"id":encryptedID},status=200)
        print(serializer.errors)
        return Response({"message":"Invalid Serializer"},status=400)
    except Exception as e:
        print(e)
        return Response({"message":"Error "+str(e)},status=500)

@api_view(['GET'])
def VerifyStudent(request):
    try:
        id = decryptData(request.GET.get('id'))
        student = Student.objects.get(id = id)
        student.is_email_verified = True
        student.save()
        return redirect('https://mprezz.com/login/')
    except Exception as e:
        print(str(e))
        return Response({'error':str(e),'message':'Error verifying student mail'},status=500)

@api_view(['GET'])
def VerifyCourseCenter(request):
    try:
        id = decryptData(request.GET.get('id'))
        course_center = CourseCenter.objects.get(id = id)
        course_center.is_email_verified = True
        course_center.save()
        return redirect('https://mprezz.com/login/')
    except Exception as e:
        print(str(e))
        return Response({'error':str(e),'message':'Error verifying Course center mail'},status=500)

@api_view(['POST'])
def CourseCenterCreation(request):
    try:
        if CourseCenter.objects.filter(email_id=request.data['email_id']).exists():
            return Response({"message":"EMAIL_ALREADY_EXISTS"},status=400)
        serializer = CourseCenterSerializer(data=request.data)
        valid=serializer.is_valid()
        if valid:
            # instance = Student.objects.create(email_id=request.data['email_id'],password=make_password(request.data['password']))
            # instance.save()
            serializer.save()
            instance = CourseCenter.objects.get(email_id=request.data['email_id'])
            jwt_token = get_or_create_jwt(instance, 'CourseProvider', instance.email_id)
            encryptedID = encryptData(instance.id)
            sendVerificationMail(VERIFY_MAIL_ROUTE_COURSE_CENTER+"?id="+encryptedID,request.data['email_id']) # sending the verification mail
            return Response({"message":"CourseCenter created",'token':str(jwt_token),'id':encryptedID},status=200)
        print(serializer.errors)
        return Response({"message":"Invalid Serializer"},status=400)
    except Exception as e:
        print(e)
        return Response({"message":"Error "+str(e)},status=500)  

@api_view(['POST'])
def UserLogin(request):
    print("Request has Entered into User Login Page")

    try:
        print(request.data)
        email = request.data.get('email_id')
        password = request.data.get('password')
        user_role = request.data.get('user_role')  # 'Student' or 'CourseProvider'
        print(user_role)
        user = None
        if user_role == 'CourseProvider':
            print("user is a coursepro")
                 # Request entered where the user exist
            user = CourseCenter.objects.filter(email_id=email).first()
            if user:
                print("user exist")
                if user.password == password:
                    print("pass is crt")
                    token = str(get_or_create_jwt(user,user_role,email))
                    print(token, " tata printed ")
                    return Response({
                        'message': 'Logged in Successfully',  # Using 'message' key
                        'token' : token,
                        'id':encryptData(user.id),
                        'data' : {
                            'name' : user.institution_name,
                            # 'user_id' : encryptData(user.id),  # encoding the user id
                            'email' : email,
                            'role' : user_role
                        }
                    }, status= 200)

                else:
                    print("pass wrong")
                    return Response({'message' : "courseprovider password was wrong"},status = 400)    

            else :
                print('coursepro not found')
                return Response({'message' : 'Current CourseCenter Not Found'},status = 500)

    
        elif user_role == 'Student':
            user = Student.objects.filter(email_id=email).first()
            if user:
                if user.password == password:
                    token = str(get_or_create_jwt(user,user_role,email))
                    print(token, " tata printed ")
                    return Response({
                        'message': 'Logged in Successfully',  # Using 'message' key
                        'token' : token,
                        'id':encryptData(user.id),
                        'data' : {
                            # 'name' : user.first_name + user.last_name,
                            # 'user_id' : encryptData(user.id),  # encoding the user id
                            # 'user_id':user.id,
                            # 'email' : email,
                            'role' : user_role

                        }
                    }, status= 200)

                else:
                    return Response({'message' : "student password was wrong"},status = 400)    

            else :
                return Response({'message' : 'Current Student Not Found'},status = 500)

            
        else:
            return Response({'message' : "User Entered Invalid Role"},status = 500)
            
    except Exception as ex:
        print(ex)
        return  Response({'message' : 'Error in Login'}, status = 500)


@api_view(['GET'])
def resend_verification_mail(request):
    validation_response = validate_token(request)
    if validation_response is not None:
        return validation_response
    try:
        userDetails = getUserDetails(request)  # getting the details of the requested user
        # if userDetails['type']!='Student':      # chekking weather he is allowed inside this endpoint or not
            # return Response({'message':"ACCESS DENIED"},status=400)
        print(userDetails)
        if userDetails['user'].is_email_verified:
            return Response({'message':'Email already verified'},status=400)
    except Exception as error:
        print(error)
        return Response({'message':'Error authorizing the user try logging in again'})
    try:
        sendVerificationMail(VERIFY_MAIL_ROUTE_STUDENT+"?id="+encryptData(userDetails['user'].id),userDetails['user'].email_id) # sending the verification mail
        return Response({'message':'Email send sucessfully.'},status=200)
    except Exception as e:
        return Response({'message':'Error resending the verification mail','Error':str(e)},status=500)


@api_view(['POST'])
def forget_password_student(request):
    try:
        student = Student.objects.filter(email_id=request.data['email_id'])
        if not student.exists():
            return Response({'message':'User not found'},status=404)
        student=student[0]
        sendPasswordMail('change_password/student/'+encryptData(student.id),student.email_id)
        return Response({'message':'Mail sent for changing password'},status=200)
    except Exception as e:
        print(str(e))
        return Response({'error':str(e),'message':'Error sending password changing mail'},status=500)

@api_view(['POST'])
def forget_password_course_center(request):
    try:
        course_center = CourseCenter.objects.filter(email_id=request.data['email_id'])
        if not course_center.exists():
            return Response({'message':'User not found'},status=404)
        course_center = course_center[0]
        sendPasswordMail('change_password/course_center/'+encryptData(course_center.id),course_center.email_id)
        return Response({'message':'Mail sent for changing password'},status=200)
    except Exception as e:
        print(str(e))
        return Response({'error':str(e),'message':'Error sending password changing mail'},status=500)

def change_password(request,role,id):
    user_id = decryptData(id)
    if role=='student':
        user = Student.objects.get(id = user_id)
        name = user.first_name+" "+user.last_name
    else:
        user = CourseCenter.objects.get(id = user_id)
        name = user.institution_name
    if request.method=='POST':
        if(request.POST.get('Password')==request.POST.get('Confirm_Passsword')):
            print('same')
            user.password = request.POST.get('Password')
            user.save()
            return redirect('https://mprezz.com/login')
        return render(request,'template/password.html',{"error":"Passwords does not match",'name':name})
    return render(request,'template/password.html',{"error":None,"name":name})