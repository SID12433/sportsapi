from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.validators import RegexValidator



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    actual_name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)  
    is_sponsor = models.BooleanField(default=False)
    is_college = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ItemName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    posted_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None,blank=True)
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.TextField()
    description = models.TextField()
    
    def __str__(self):
        return self.title

class StudentDetails(models.Model):
   college = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   name = models.CharField(max_length=100)
   roll_no = models.CharField(max_length=100)
   event = models.CharField(max_length=100)
   item = models.TextField(default=None,blank=True)
   position = models.ForeignKey(Position, on_delete=models.CASCADE)

   def __str__(self):
        return self.name

class Post(models.Model):
    college = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_name = models.TextField()
    event = models.TextField()
    item = models.ManyToManyField(ItemName)
    description = models.TextField()
    roll_no=models.CharField(max_length=100,default=None,blank=True)
    is_sponsored = models.BooleanField(default=False)
    image=models.ImageField(default=None,blank=True)
    needed=models.IntegerField(default=0)
    
    def __str__(self):
        return self.student_name

class Sponsored(models.Model):
    sponsor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    payment=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return str(self.sponsor)

# class Chat(models.Model):
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
#     receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
#     message = models.CharField(max_length=1200)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.message

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return self.message
    
class Request(models.Model):
    sponsor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    pending = models.BooleanField(default=True)
    accept = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)

    def __str__(self):
        return f"Request from {self.sponsor.username} for post {self.post.id}"

class EventRegistration(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Event=models.ForeignKey(Event,on_delete=models.CASCADE)
    items=models.TextField(blank=True,default=None)
    date=models.DateTimeField(auto_now_add=True)
    description=models.TextField(blank=True,default=None)

class SponsorProfile(models.Model):
    sponsor=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    document=models.FileField()
    description=models.TextField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ph = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    is_ok=models.BooleanField(default=False)
    
class College(models.Model):
    college=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    document=models.FileField(upload_to='documents/',null=True)
    description=models.TextField()
    address=models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ph = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)

class Student(models.Model):
    Student=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    document=models.FileField(upload_to='documents/',null=True)
    description=models.TextField()
    address=models.TextField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ph = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
