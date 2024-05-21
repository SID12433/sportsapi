from django.urls import path
from adminapp import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("event",views.EventView,basename="event")



urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
] +router.urls
