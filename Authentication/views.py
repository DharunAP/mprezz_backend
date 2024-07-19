from rest_framework.response import Response
from rest_framework.decorators import api_view
from Static.models import Student,CourseCenter
from .Serializers import StudentSerializer,CourseCenterSerializer
from .jwtValidation import *

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
            return Response({"message":"Student created","token":str(jwt_token)},status=200)
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
            jwt_token = get_or_create_jwt(instance, 'CourseProvider', instance.email_id)
            return Response({"message":"CourseCenter created",'token':str(jwt_token)},status=200)
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