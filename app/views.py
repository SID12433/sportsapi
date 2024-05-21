from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from .  models import CustomUser
from . import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, status
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'username': user.username,
            'email': user.email,
            'id':user.id,
            'college':user.is_college,
            'student':user.is_student,
            'sponsor':user.is_sponsor
            
      })


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

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
               'profile_pic':user.profile_picture.url if user.profile_picture else None

 

            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#college---------------------------

class StudentsAPI(generics.ListCreateAPIView):
    serializer_class=serializers.AddStudentsSerializer
    queryset=models.StudentDetails.objects.all()
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(college=user)
    def get_queryset(self):
       user=self.request.user
       query=models.StudentDetails.objects.filter(college=user)
       return query
    
class Events(generics.ListAPIView):
    serializer_class=serializers.AddEventserializer
    queryset=models.Event.objects.all()
    permission_classes=[IsAuthenticated]
    # def get_queryset(self):
    #     user=self.request.user
    #     return models.Event.objects.all()

# class UpdateEvents(generics.RetrieveUpdateAPIView):
#     serializer_class=serializers.AddEventserializer
#     queryset=models.Event.objects.all()
#     permission_classes=[IsAuthenticated]
   
class Posts(generics.ListCreateAPIView):
    serializer_class=serializers.AddPostSerializer
    queryset=models.Post.objects.all()
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(college=user)

    def get_queryset(self):
        user=self.request.user
        qury=models.Post.objects.filter(college=user)
        return qury

class Myrequest(generics.ListAPIView):
    serializer_class=serializers.PostRequestSerializer
    queryset=models.Request.objects.all()
    permission_classes=[IsAuthenticated]
    lookup_url_kwarg = 'post_id' 

    def get_queryset(self):
        post_id=self.kwargs.get('post_id')
        queryset=models.Request.objects.filter(post=post_id)
        return queryset

class requestUpdate(generics.RetrieveUpdateAPIView):
    serializer_class=serializers.PostRequestSerializer
    queryset=models.Request.objects.all()
    permission_classes=[IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        pending = self.request.data.get('pending', False)
        accept = self.request.data.get('accept', False)
        decline = self.request.data.get('decline', False)
        if pending:
            accept = False
            decline = False
        elif accept:
            pending = False
            decline = False
        elif decline:
            pending = False
            accept = False
        serializer.save(pending=pending, accept=accept, decline=decline)
 
class Listeventsexc(generics.ListAPIView):
    serializer_class=serializers.AddEventserializer
    queryset=models.Post.objects.all()
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        queryset=models.Event.objects.exclude(posted_by=user)
        return queryset
class UpdatePost(generics.RetrieveUpdateAPIView):
    serializer_class=serializers.AddPostSerializer
    queryset=models.Post.objects.all()

#--------Student
class ListEvents(generics.ListAPIView):
    serializer_class=serializers.AddEventserializer
    queryset=models.Event.objects.all()
    permission_classes=[IsAuthenticated]

class RegisterEvent(generics.CreateAPIView):
    queryset = models.EventRegistration.objects.all()
    serializer_class = serializers.EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Retrieve the event ID from the URL kwargs
        event_id = self.kwargs.get('event_id')
        # Get the event object using event_id
        event = get_object_or_404(models.Event, id=event_id)
        # Update the request data to include the event ID
        request.data['Event'] = event_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Associate the logged-in user with the registration
        serializer.save(user=request.user, Event=event)
        return Response(serializer.data)
    
class ListMyReg(generics.ListAPIView):
    queryset=models.EventRegistration.objects.all()
    serializer_class = serializers.myEventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        return models.EventRegistration.objects.filter(user=user)
    
class DeleteRegistration(generics.RetrieveDestroyAPIView):
    queryset=models.EventRegistration.objects.all()
    # serializer_class = serializers.EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

#sponsor-----------------------------------------
class Seeposts(generics.ListAPIView):
    serializer_class = serializers.AddPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile = models.SponsorProfile.objects.filter(sponsor=self.request.user).first()
        if profile and profile.is_ok:
            return models.Post.objects.filter(is_sponsored=False)
        else:
            raise PermissionDenied("Your account needs to be verified by an admin to view posts. Please wait for the verification process to complete. We apologize for the inconvenience.")

class CreateProfile(generics.CreateAPIView):
    serializer_class=serializers.CreateProfileSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(sponsor=user)

class SendRequest(generics.CreateAPIView):
    serializer_class=serializers.RequestCreate
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user=self.request.user
        post_id=self.kwargs.get('post_id')
        post=get_object_or_404(models.Post,id=post_id)
        serializer.save(sponsor=user,post=post)

class SponsoredRequest(generics.ListAPIView):
    serializer_class=serializers.PostRequestSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        return models.Request.objects.filter(sponsor=user)
    
class DeleteRequest(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset=models.Request.objects.all()

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        receiver_id = self.kwargs['receiver']
        # Mark messages as read
        messages = models.Message.objects.filter(receiver_id=receiver_id)
        for message in messages:
            message.is_read = True
            message.save()
        return messages
    
    def perform_create(self, serializer):
        receiver_id = self.kwargs.get('receiver')
        post_id=self.kwargs.get('post_id')
        post=get_object_or_404(models.Post,id=post_id)
        receiver = get_object_or_404(models.CustomUser, id=receiver_id)
        serializer.save(sender=self.request.user, receiver=receiver,post=post)


class MessageListAPIView(generics.ListCreateAPIView):
    serializer_class =serializers.MessageListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        post_id=self.kwargs.get('post_id')
        post=get_object_or_404(models.Post, id=post_id)
        query=models.Message.objects.filter(sender=user, receiver_id=receiver_id,post=post) | \
               models.Message.objects.filter(sender_id=receiver_id, receiver=user,post=post)
        queryset = query.order_by('-timestamp')
        return queryset

class PayAndCreateSposored(generics.CreateAPIView):
    serializer_class=serializers.sponsoredserializer
    queryset=models.Sponsored.objects.all()

    def perform_create(self, serializer):
        user=self.request.user
        post_id=self.kwargs.get('post_id')
        post=get_object_or_404(models.Post,id=post_id)
        pay=serializer.save(sponsor=user,post=post)
        if pay:
           post.is_sponsored=True
           post.save()
        return super().perform_create(serializer)
    
class Allcollege(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=serializers.collegenameserializer
    queryset=models.CustomUser.objects.filter(is_college=True)

class StudentsList(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=serializers.ListStudentsSerializer
    queryset=models.CustomUser.objects.filter()
    def get_queryset(self):
        college_id=self.kwargs.get('college_id')
        return models.StudentDetails.objects.filter(college=college_id)

class AllUSers(generics.ListAPIView):
    queryset=models.CustomUser.objects.all()
    serializer_class=serializers.AllUSers

class CollegeUserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_college=True)
    serializer_class = serializers.AllUSers

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        actual_name = self.request.query_params.get('actual_name')
        if username:
            queryset = queryset.filter(username__icontains=username)
        if actual_name:
            queryset = queryset.filter(actual_name__icontains=actual_name)
        return queryset
    

class CreatecollegeProfile(generics.CreateAPIView):
    serializer_class=serializers.CreatecollegeProfileSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(college=user)

class CreatestudentProfile(generics.CreateAPIView):
    serializer_class=serializers.studentProfileSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(student=user)