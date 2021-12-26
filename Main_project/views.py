from django.http import request, response
from django.shortcuts import render, resolve_url
from . import sql
# Create your views here.

def Home(request):
    return render(request,"Home.html")

def Login(request):
    if request.method=='POST':
        email=request.POST['Email']
        password=request.POST['Password']
        sql.Db.connect(sql.Db)
        sql.Db.login(sql.Db,email,password)
        return render(request, "Login_Sucessful.html")
    else:
        return render(request, "Login.html")

def Register(request):
    if request.method=='POST':
        User_Info_fields = ['FirstName', 'LastName', 'Username', 'Email', 'Contact', 'DOB', 'Password']
        User_Info = []
        for field in User_Info_fields:
            if field=='Contact':
                User_Info.append(False)
            User_Info.append(request.POST[field])
        sql.Db.connect(sql.Db)
        sql.Db.create_user(sql.Db,User_Info)
        return render(request, "Register_Sucessfully.html")
    else:
        return render(request, "Register.html")

def Logout(request):
    if request.method == 'POST':
        email = request.POST['Email']
        sql.Db.connect(sql.Db)
        sql.Db.logout(sql.Db,email)
        return render(request,'Logout_Sucessfull.html')
    else:
        return render(request,'Logout.html')
