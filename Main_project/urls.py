from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [path('Home',views.Home, name = 'Home'), path('Login',views.Login, name = 'Login'), path('Register',views.Register, name = 'Register'),
path('Logout',views.Logout, name = 'Logout'), path('Images', views.Get_AllImages, name='Images'),path('Videos', views.Get_AllVideos, name='Videos'), 
path('UploadImages', views.AddImage, name='UploadImages'),path('UploadVideo', views.AddVideo, name='UploadVideo'),path('Profile', views.Login, name='Login')]