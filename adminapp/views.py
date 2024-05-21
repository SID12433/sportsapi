from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet,ViewSet


from app.models import CustomUser
from app.models import *


from app.models import *
from adminapp.serializers import *

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'is_superuser':user. is_superuser,
                'id':user.id,
               'name':user.actual_name,
               'is_student':user.is_student ,
                'is_sponsor':user.is_sponsor,
                'is_college':user.is_college,
                'is_admin':user.is_superuser,
               'profile_pic':user.profile_picture.url if user.profile_picture else None
               
            })
            
            
class EventView(ViewSet):
    permission_classes=[IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=EventSerializer(data=request.data)
        user_id=request.user
        if serializer.is_valid():
            serializer.save(posted_by=user_id)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self,request,*args,**kwargs):
        qs=Event.objects.all()
        serializer=EventSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Event.objects.get(id=id)
        serializer=EventSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance =Event.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Event removed"})
        except Event.DoesNotExist:
            return Response({"msg": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        
        

        