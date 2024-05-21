from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    #authentication---------------------------
    path('register/',views.RegistrationView.as_view(), name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('all/users/',views.AllUSers.as_view(),name='all-users'),

    #college------------------------------------
    path('add/list/Students/',views.StudentsAPI.as_view(),name='Add-list-StudentsAPI'),
    path('list/events/',views.Events.as_view(),name='list-event'),
    path('create/college/profile/',views.CreatecollegeProfile.as_view(),name='create-college-profile'),
    # path('update/events/<int:pk>/',views.UpdateEvents.as_view(),name='update'),
    path('add/list/post/',views.Posts.as_view(),name='create-list-post'),
    path('list/own/requests/<int:post_id>/',views.Myrequest.as_view(),name='own-requests'),
    path('update/requests/<int:pk>/',views.requestUpdate.as_view(),name='Update-requests'),
    # path('list/event/exclude/',views.Listeventsexc.as_view(),name='list_post_exclude_loggedin_user'),
    path('update/post/<int:pk>/',views.UpdatePost.as_view(),name='update-post'),
    path('list/all/college/',views.Allcollege.as_view(),name='all-college'),
    path('student/detail/college/<int:college_id>/',views.StudentsList.as_view(),name='student-details'),
    
    #student--------------------------------
    path('register/event/<int:event_id>/',views.RegisterEvent.as_view(),name='register-to-event'),
    path('my/registration/',views.ListMyReg.as_view(),name='list-my-registrations'),
    path('delete/registration/<int:pk>/',views.DeleteRegistration.as_view(),name='list-my-registrations'),
    path('create/student/profile/',views.CreatestudentProfile.as_view(),name='create-student-profile'),
   
    #Sponsor----------------------------------
    path('create/profile/',views.CreateProfile.as_view(),name='create-sponsor-profile'),
    path('list/posts/',views.Seeposts.as_view(),name='see-posts'),
    path('send/request/<int:post_id>/',views.SendRequest.as_view(),name='send-request'),
    path('sponsor/own/request/',views.SponsoredRequest.as_view(),name='sponsor-own-request'),
    path('delete/own/request/<int:pk>/',views.DeleteRequest.as_view(),name='delete-own-request'),
    path('send/money/<int:post_id>/',views.PayAndCreateSposored.as_view(),name='sponsor'),
    # path('send/money/<int:post_id>/',views.PayAndCreateSposored.as_view(),name='sponsor'),

   #chat--------------------------------
    path('messages/<int:receiver>/<int:post_id>/', views.MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('listmessages/<int:receiver_id>/', views.MessageListAPIView.as_view(), name='message-list-create'),

    #search
    path('college-users/', views.CollegeUserListAPIView.as_view(), name='college_users_list'),#college-users/?username=search_username

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)