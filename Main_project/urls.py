from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns = [path('',views.Home, name = 'Home'), path('Login',views.Login, name = 'Login'), path('Register',views.Register, name = 'Register'), 
path('Logout',views.Logout, name = 'Logout')]