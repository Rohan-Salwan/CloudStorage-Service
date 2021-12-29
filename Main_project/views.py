from django.http import request, response
from django.shortcuts import render, resolve_url
from . import Mysql
from . import Fn 
# Create your views here.

def Home(request):
    if 'id' in request.COOKIES:
        sessionid = request.COOKIES['id']
        Verified = Fn.Verify_Session(sessionid)
        if Verified:
            return render(request,"Home.html")
    return render(request, "Login.html")

def Login(request):
    if request.method=='POST':
        Email=request.POST['Email']
        Password=request.POST['Password']
        Fn.Connection_Establishment(Email,Password)
        Response, SessionId = Fn.Assign_SessionId(request) 
        Fn.Generate_Session(SessionId)
        return Response
    else:
        return render(request, "Login.html")

def Register(request):
    if request.method=='POST':
        User_Info = Fn.Get_UserFieldValues(request)
        Fn.Create_User(User_Info)
        return render(request, "Register_Sucessfully.html")
    else:
        return render(request, "Register.html")

def Logout(request):
    if request.method == 'POST':
        email = request.POST['Email']
        Mysql.Db.connect(Mysql.Db,'rohan1')
        Mysql.Db.logout(Mysql.Db,email)
        return render(request,'Logout_Sucessfull.html')
    else:
        return render(request,'Logout.html')

     