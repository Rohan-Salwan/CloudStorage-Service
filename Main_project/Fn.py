from urllib import response
from django.shortcuts import render
from . import cache
from . import User
from . import session
import json
import time
import Media
from datetime import datetime

Server_Cache=cache.Cache()

User_Info_fields = ['FirstName', 'LastName', 'Username', 'Email', 'Contact', 'DOB', 'Password']

def UploadVideoRequest_Handler(request,Verified,User_Session,sessionid,desc,Videolink):
    if Verified and User_Session:
        User_Session['User_Videos'][desc]=Videolink
        User_DesirializedVideosDict = User_Session['User_Videos']
        User_Email=User_Session['email']
        Media.Db.connect(Media.Db)
        Media.Db.Upload_Video(Media.Db,User_Email, User_DesirializedVideosDict)
        Server_Cache.get(sessionid,Update_Node=User_Session)
        return render(request, 'Videos.html', {'User_Videos': User_DesirializedVideosDict})
    else:
        return render(request, "Login.html")

def UploadImageRequest_Handler(request,Verified,User_Session,sessionid, ImageLink):
    if Verified and User_Session:
        ImageUploaded_Time=datetime.now()
        Uploaded_Time=ImageUploaded_Time.strftime("%H:%M:%S")
        User_Session['User_Images'][ImageLink]=Uploaded_Time
        User_DesirializedImagesDict=User_Session['User_Images']
        User_Email=User_Session['email']
        Media.Db.connect(Media.Db)
        Media.Db.Upload_Image(Media.Db, User_Email, User_DesirializedImagesDict)
        Server_Cache.get(sessionid,Update_Node=User_Session)
        return render(request, 'Images.html', {'User_Images': User_DesirializedImagesDict})
    else:
        return render(request, "Login.html")

def VideoRequest_Handler(request,Verified,User_Session,sessionid):
    if Verified and User_Session:
        if 'User_Videos' in User_Session:
            User_DesirializedVideosDict=User_Session['User_Videos']
            return render(request, 'Videos.html', {'User_Videos': User_DesirializedVideosDict})
        else:
            UserEmail=User_Session['email']
            User_VideoQueryResult=Media.Db.Query(Media.Db,UserEmail)
            User_SerializedVideosDict=User_VideoQueryResult[0]
            User_DesirializedVideosDict=json.loads(User_SerializedVideosDict)
            User_Session['User_Videos']=User_DesirializedVideosDict
            Server_Cache.get(sessionid,Update_Node=User_Session)
            return render(request,'Videos.html', {'User_Videos': User_DesirializedVideosDict})
    else:
        return render(request, 'Login.html')

def ImageRequest_Handler(request, Verified, User_Session, sessionid):
    if Verified and User_Session:
        if 'User_Images' in User_Session:
            User_DeserializedImagesDict=User_Session['User_Images']
            return render(request, 'Images.html', {'User_Images': User_DeserializedImagesDict})
        else:
            UserEmail=User_Session['email']
            User_ImageQueryResult=Media.Db.Query(Media.Db,UserEmail)
            User_SerializedImagesDict=User_ImageQueryResult[1]
            User_DeserializedImagesDict=json.loads(User_SerializedImagesDict)
            User_Session['User_Images']=User_DeserializedImagesDict
            Server_Cache.get(sessionid,Update_Node=User_Session)
            return render(request,'Images.html', {'User_Images': User_DeserializedImagesDict})
    else:
        return render(request, 'Login.html')

def ProflieRequest_Handler(request,Verified,User_Session,sessionid):
    if Verified and User_Session:
        if 'User_Profile' in User_Session:
            User_Profile=User_Session['User_Profile']
            return render(request, 'profile.html',{'User_Details':User_Profile})
        else:
            return Get_UserProfile(request,User_Session,sessionid)
    else:
        return render(request, "Login.html")

def Get_UserFieldValues(request):
    User_Info = []
    for field in User_Info_fields:
        User_Info.append(request.POST[field])
    return User_Info

def Create_User(User_Info):
    User.Db.connect(User.Db)
    User.Db.create_user(User.Db,User_Info)
    email=User_Info[3]
    Media.Db.InitializeUserTraceInMedia(Media.Db, email)

def Generate_Session(ID,email):
    session.Db.connect(session.Db)
    session.Db.Session_Generator(session.Db,email,[ID, {}])

def Connection_Establishment(email,password,request):
    User.Db.connect(User.Db)
    User_Details=User.Db.login(User.Db,email,password)
    SessionId = session.Db.SessionId_Generator(session.Db)
    User_Session=Generate_Session(SessionId,email)
    Response=UserProfileResponse(request,User_Session,SessionId,User_Details)
    Response.set_cookie('id', SessionId)
    return Response

def UserProfileResponse(request,User_Session,SessionId,User_Details):
    User_Profile=zip(User_Info_fields,User_Details)
    Response=render(request,'profile.html',{'User_Details': User_Profile})
    User_Session['User_Profile']=User_Profile
    Server_Cache.Put(SessionId,User_Session)
    return Response

def Get_UserProfile(request, User_Session,sessionid):
    User_Email=User_Session['email']
    User.Db.connect(User.Db)
    User_Details=User.Db.Query(User.Db, User_Email)
    return UserProfileResponse(request,User_Session,sessionid,User_Details)

def Verify_Session(SessionId):
    User_Session = Get_DeserializedSession(SessionId)
    if User_Session:
        Valid_Session = SessionExpire_Checker(User_Session)
        return Valid_Session, User_Session
    else:
        return False

def Get_DeserializedSession(SessionId):
    try:
        if SessionId not in Server_Cache.Map:
            session.Db.connect(session.Db)
            UserSessionInfo_List = session.Db.Query(session.Db,SessionId)
            User_Session = UserSessionInfo_List[1]
            Deserialized_UserSession = json.loads(User_Session)
            Server_Cache.Put(SessionId,Deserialized_UserSession)
        else:
            Deserialized_UserSession = Server_Cache.get(SessionId)
        return Deserialized_UserSession
    except Exception as e:
        return None

def SessionExpire_Checker(User_Session):
    date=time.strftime("%d %b %Y ")
    if date==User_Session['Date']:
        return True
    else:
        sessionid = User_Session['session_id']
        delete_session(sessionid)
        return False

def delete_session(session_id):
    session.Db.connect(session.Db)
    session.Db.Delete_Session(session.Db,session_id)
