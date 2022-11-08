from .models import Task
from rest_framework import generics
from django.shortcuts import  render
from .serializer import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,get_user_model,logout
from rest_framework import mixins
from .decorators import *
from django.utils.decorators import method_decorator


"""
User registration
"""

class UserRegister(APIView):
    def post(self,request,*args,**kwargs):
        if not request.data.get("email") or not request.data.get("password") or not request.data.get("username") or not request.data.get("full_name"):
            return Response(
                    data={"error": "Something went wrong","required feilds":["email","username","full_name","password"]}, status=status.HTTP_400_BAD_REQUEST
                )
        if len(request.data.get("password")) < 8:
            return Response({"message":"Please enter minimum 8 digit password."},status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(email=request.data.get("email")):
            return Response({"message":"There is already a registered user with that email address"},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=request.data.get("username")):
            return Response({"message":"Username is already taken. Please try again!"},status=status.HTTP_400_BAD_REQUEST)
        dt={
            "full_name":request.data.get("full_name"),
            "username":"_".join(request.data.get("username").lower().split(" ")),
            "email":request.data.get("email"),
            "password":make_password(request.data['password']),
            "role_id":4
        }
        
        try:
            user = User.objects.get(**dt)
        except User.DoesNotExist:
            user = User.objects.create(**dt)        


        data = UserSerializer(user,context={"request":request}).data

        return Response({"data":data,"status":status.HTTP_200_OK,"msg":"Registration done Successful",'url' : self.request.path}, status=status.HTTP_200_OK)


"""
user login
"""
class LoginView(APIView):    
    def post(self, request, *args, **kwargs):
        print(request.data)
        data={}
        if not request.data.get("username") or not request.data.get("password") :
            return Response(
                    data={"error": "Something went wrong","required feilds":["username","password"]}, status=status.HTTP_400_BAD_REQUEST
                )
        if not User.objects.filter(username=request.data.get("username")):
            return Response({"message":"No Account found for entered username!"},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=request.data.get("username"),password=request.data.get("password"))
        if not user:
            return Response({"message":"Invalid login credentials."},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = Token.objects.get(user = user)
            token.delete()
            token = Token.objects.create(user = user)
        except:
            token = Token.objects.create(user = user)
        
        data = UserSerializer(user,context = {"request":request}).data
        data.update({"token":token.key})

        return Response({"data":data,"token":token.key,"status":status.HTTP_200_OK,"msg":"Login Successful",'url' : self.request.path}, status=status.HTTP_200_OK)




class TaskView(generics.ListAPIView,generics.CreateAPIView,generics.GenericAPIView,):
    permission_classes = [IsAuthenticated]
    serializer_class = Taskserializer
    queryset = Task.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @method_decorator(user_is_client)
    def post(self, request):
        if not request.data.get("title") or not request.data.get("description") :
            return Response(
                    data={"error": "Something went wrong","required feilds":["title","description"]}, status=status.HTTP_400_BAD_REQUEST
                )
        task = self.create(request)
        return Response(
            {
                "message": "Task Created Successfully",
            }
        )

    @method_decorator(user_is_client)
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @method_decorator(user_is_manager)
    def put(self, request, id=None, pk=None):
        instance = self.queryset.get(id=id)
        try:
            user = User.objects.get(id=pk)
        except:
            return Response(
            {
                "message": "user not found",
            }
        )
        instance.assigned_to=user
        instance.save()
        return Response(
            {
                "message": f"Task `{instance.title}` assigned to {user.full_name}",
            }
        )

class TaskListView(generics.ListAPIView,generics.GenericAPIView,):
    permission_classes = [IsAuthenticated]
    serializer_class = Taskserializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request)
       
    @method_decorator(user_is_employee)
    def put(self, request, id=None):
        instance = self.queryset.get(id=id)
        if not instance.assigned_to == request.user:
            return Response(
            {
                "message": f"Task `{instance.title}` can not be be completed by you.",
            }
        )
        instance.status=Task.COMPLETE
        instance.save()
        return Response(
            {
                "message": f"Task `{instance.title}` has been marked completed.",
            }
        )

class DeleteTaskView(generics.ListAPIView,generics.GenericAPIView,):
    permission_classes = [IsAuthenticated]
    serializer_class = Taskserializer
    queryset = Task.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    
    @method_decorator(user_is_manager)
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message":"Deleted successfully"})
