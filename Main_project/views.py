from django.http import request, response
from django.shortcuts import render, resolve_url
from . import User
from . import Fn
# Create your views here.

def Home(request):
    if 'id' in request.COOKIES:
        sessionid = request.COOKIES['id']
        Verified, User_Session = Fn.Verify_Session(sessionid)
        if Verified and User_Session:
            return render(request,"Home.html")
    return render(request, "Login.html")

def AddVideo(request):
    if request.method=="POST":
        if 'id' in request.COOKIES:
            sessionid = request.COOKIES['id']
            VideoLink=request.FILES['FileName']
            Verified, User_Session = Fn.Verify_Session(sessionid)
            return Fn.UploadVideoRequest_Handler(request, Verified, User_Session,VideoLink)
        else:
            return render(request, "Login.html")
    else:
        return render(request, "UploadVideo.html")

def AddImage(request):
    if request.method=="POST":
        if 'id' in request.COOKIES:
            sessionid = request.COOKIES['id']
            Image=request.FILES['Image']
            Verified, User_Session = Fn.Verify_Session(sessionid)
            return Fn.UploadImageRequest_Handler(request, Verified, User_Session, Image)
        else:
            return render(request,"Login.html")
    else:
        return render(request, "UploadImages.html")

def Get_AllImages(request):
    if 'id' in request.COOKIES:
        sessionid = request.COOKIES['id']
        Verified, User_Session = Fn.Verify_Session(sessionid)
        return Fn.ImageRequest_Handler(request, Verified, User_Session)
    else:
        return render(request, "Login.html")

def Get_AllVideos(request):
    if 'id' in request.COOKIES:
        sessionid = request.COOKIES['id']
        Verified, User_Session = Fn.Verify_Session(sessionid)
        return Fn.VideoRequest_Handler(request,Verified,User_Session)
    else:
        return render(request,"Login.html")

def Login(request):
    if request.method=='POST':
        if 'id' not in request.COOKIES:
            Email=request.POST['Email']
            Password=request.POST['Password']
            return Fn.Connection_Establishment(Email,Password,request)
        sessionid = request.COOKIES['id']
        Verified, User_Session = Fn.Verify_Session(sessionid)
        return Fn.ProflieRequest_Handler(request, Verified, User_Session, sessionid)
    else:
        if "id" in request.COOKIES:
            sessionid = request.COOKIES['id']
            Verified, User_Session = Fn.Verify_Session(sessionid)
            return Fn.ProflieRequest_Handler(request, Verified, User_Session, sessionid)
        return render(request, "Login.html")

def Register(request):
    if request.method=='POST':
        User_Info = Fn.Get_UserFieldValues(request)
        Fn.Create_User(User_Info)
        return render(request, "Register_Sucessfully.html")
    else:
        return render(request, "Register.html")

def Logout(request):
    try:
        sessionid = request.COOKIES['id']
        Fn.delete_session(sessionid)
        return render(request,'Logout_Sucessfull.html')
    except:
        return render(request, 'Login.html')
