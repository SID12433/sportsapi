from . import models 
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# Create your views here.

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.CustomUser
        fields = ['username', 'email', 'password','is_superuser','is_college','is_sponsor','actual_name','profile_picture','is_student']

    def create(self, validated_data):
        user = models.CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
#college
    
class AddStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.StudentDetails
        fields=['name','roll_no','event','item','position']

class ListStudentsSerializer(serializers.ModelSerializer):
    item_name=serializers.CharField(source="item.name")
    position_name=serializers.CharField(source="position.name")
    class Meta:
        model=models.StudentDetails
        fields=['name','roll_no','event','item_name','position_name']

class AddEventserializer(serializers.ModelSerializer):
    class Meta:
        model=models.Event
        fields='__all__'

class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Post
        fields=['student_name','event','item','description','roll_no','image','is_sponsored','needed']

class PostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Request
        fields='__all__'

from rest_framework import serializers
from .models import EventRegistration

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['items', 'description']  

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])  # Pop 'items' from validated_data
        event_registration = EventRegistration.objects.create(**validated_data)
        event_registration.items.set(items_data)  # Set the many-to-many relationship
        return event_registration
  
class myEventRegistrationSerializer(serializers.ModelSerializer):
    Eventname=serializers.CharField(source='Event.title')
    class Meta:
        model = EventRegistration
        fields = ['items', 'description','Eventname']  

class ListMyEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventRegistration
        fields='__all__'
        
class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SponsorProfile
        fields=['description','document','ph']

class CreatecollegeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.College
        fields=['description','document','ph',"address"]

class studentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Student
        fields=['description','document','ph',"address"]

class RequestCreate(serializers.ModelSerializer):
    class Meta:
        model=models.Request
        fields=['description']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ['message']

class MessageListSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    class Meta:
        model = models.Message
        fields = ['sender_username','receiver_username','message',"timestamp"]

class sponsoredserializer(serializers.ModelSerializer):
    class Meta:
        model=models.Sponsored
        fields=["payment"]

class collegenameserializer(serializers.ModelSerializer):
    # collegename=serializers.CharField(source="CustomUser.username")
    class Meta:
        model=models.CustomUser
        fields=["id","username"]

class AllUSers(serializers.ModelSerializer):
    class Meta:
        model=models.CustomUser
        fields='__all__'

