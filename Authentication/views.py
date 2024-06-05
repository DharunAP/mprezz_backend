from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Static.models import Student,CourseCenter
from .Serializers import StudentSerializer,CourseCenterSerializer

@api_view(['POST'])
def SignupStudent(request):
    try:
        if Student.objects.filter(email=request.data['email']).exists():
            return Response({"message":"EMAIL_ALREADY_EXISTS"},status=400)
        serializer = StudentSerializer(data=request.data)
        valid=serializer.is_valid()
        if valid:
            # instance = Student.objects.create(email_id=request.data['email_id'],password=make_password(request.data['password']))
            # instance.save()
            serializer.save()
            return Response({"message":"Student created"},status=200)
        print(serializer.errors)
        return Response({"message":"Invalid Serializer"},status=400)
    except Exception as e:
        print(e)
        return Response({"message":"Error "+str(e)},status=500)

@api_view(['POST'])
def CourseCenterCreation(request):
    try:
        if CourseCenter.objects.filter(email=request.data['email']).exists():
            return Response({"message":"EMAIL_ALREADY_EXISTS"},status=400)
        serializer = CourseCenterSerializer(data=request.data)
        valid=serializer.is_valid()
        if valid:
            # instance = Student.objects.create(email_id=request.data['email_id'],password=make_password(request.data['password']))
            # instance.save()
            serializer.save()
            return Response({"message":"CourseCenter created"},status=200)
        print(serializer.errors)
        return Response({"message":"Invalid Serializer"},status=400)
    except Exception as e:
        print(e)
        return Response({"message":"Error "+str(e)},status=500)
    
# @api_view(['POST'])
# def UserLogin (request) :
#     try :
#         print('hello')

#     except Exception as ex:
#         print(ex ,' the exception')
#         return Response({'message' : 'Some error occurre'},status=500)
    

@api_view(['POST'])
def UserLogin(request):
    print("Request has Entered into User Login Page")

    try:
        print(request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user_role = request.data.get('user_role')  # 'Student' or 'CourseProvider'
        user = None
        if user_role == 'CourseProvider':
                 # Request entered where the user exist
            user = CourseCenter.objects.filter(email_id=email).first()

        elif user_role == 'Student':
            user = Student.objects.filter(email_id=email).first()
            
        else:
            return Response({'message' : "User Entered Invalid Role"},status = 500)
        print(user)

        if not user:
                    # Request entered were user not exist
            if user_role == 'Student':
                return Response({'message' : 'Current Student Not Found' }, status = 500)
            
            else :
                return Response({'message' : 'Current CourseCenter Not Found'},status = 500)
            
        # if check_password(password, user.password):
        if (password == user.password):
            # token = str(get_or_create_jwt(user,user_role,email))
            token = 'ippo summa da'
            print(token, " tata printed ")
            return Response({
                'message': 'Logged in Successfully',  # Using 'message' key
                'token' : token,
                'data' : {
                    'name' : user.first_name + user.last_name,
                    # 'user_id' : encryptData(user.id),  # encoding the user id
                     
                    'email' : email,
                    'role' : user_role
                }
            }, status= 200)
        
        else:
            print("Invalid password")            
            return Response({'message' : 'Invalid Password'}, status = 400)
            
    except Exception as ex:
        print(ex)
        return  Response({'message' : 'Error in Login'}, status = 500)

