from urllib import response
from django.shortcuts import render
from . import cache
from . import User
from . import session
import json
import time
from . import Media
from datetime import datetime

Server_Cache=cache.Cache()

User_Info_fields = ['FirstName', 'LastName', 'Username', 'Email', 'Contact', 'DOB', 'Password']

def UploadVideoRequest_Handler(request,Verified,User_Session,desc,Videolink):
    if Verified and User_Session:
        User_Email = User_Session['email']
        User_Dict=Server_Cache.get(User_Email)
        User_Dict['User_Videos'][desc]=Videolink
        User_DesirializedVideosDict = User_Dict['User_Videos']
        Media.Db.connect(Media.Db)
        Media.Db.Upload_Video(Media.Db,User_Email, User_DesirializedVideosDict)
        Server_Cache.get(User_Email,Update_Node=User_Dict)
        return render(request, 'UplaodVideos.html', {'User_Videos': User_DesirializedVideosDict})
    else:
        return render(request, "Login.html")

def UploadImageRequest_Handler(request,Verified,User_Session,ImageLink):
    if Verified and User_Session:
        User_Email = User_Session['email']
        User_Dict=Server_Cache.get(User_Email)
        ImageUploaded_Time=datetime.now()
        Uploaded_Time=ImageUploaded_Time.strftime("%H:%M:%S")
        User_Dict['User_Images'][ImageLink]=Uploaded_Time
        User_DesirializedImagesDict=User_Dict['User_Images']
        Media.Db.connect(Media.Db)
        Media.Db.Upload_Image(Media.Db, User_Email, User_DesirializedImagesDict)
        Server_Cache.get(User_Email,Update_Node=User_Dict)
        return render(request, 'UploadImages.html', {'User_Images': User_DesirializedImagesDict})
    else:
        return render(request, "Login.html")

def VideoRequest_Handler(request,Verified,User_Session):
    if Verified and User_Session:
        User_Email = User_Session['email']
        User_Dict=Server_Cache.get(User_Email)
        if 'User_Videos' in User_Dict:
            User_DesirializedVideosDict=User_Dict['User_Videos']
            return render(request, 'Videos.html', {'User_Videos': User_DesirializedVideosDict})
        else:
            User_VideoQueryResult=Media.Db.Query(Media.Db,User_Email)
            User_SerializedVideosDict=User_VideoQueryResult[1]
            User_DesirializedVideosDict=json.loads(User_SerializedVideosDict)
            User_Dict['User_Videos']=User_DesirializedVideosDict
            Server_Cache.get(User_Email,Update_Node=User_Dict)
            return render(request,'Videos.html', {'User_Videos': User_DesirializedVideosDict})
    else:
        return render(request, 'Login.html')

def ImageRequest_Handler(request, Verified, User_Session):
    if Verified and User_Session:
        User_Email = User_Session['email']
        User_Dict=Server_Cache.get(User_Email)
        if 'User_Images' in User_Dict:
            User_DeserializedImagesDict=User_Dict['User_Images']
            return render(request, 'Images.html', {'User_Images': User_DeserializedImagesDict})
        else:
            User_ImageQueryResult=Media.Db.Query(Media.Db,User_Email)
            User_SerializedImagesDict=User_ImageQueryResult[2]
            User_DeserializedImagesDict=json.loads(User_SerializedImagesDict)
            User_Dict['User_Images']=User_DeserializedImagesDict
            Server_Cache.get(User_Email,Update_Node=User_Dict)
            return render(request,'Images.html', {'User_Images': User_DeserializedImagesDict})
    else:
        return render(request, 'Login.html')

def ProflieRequest_Handler(request,Verified,User_Session,sessionid):
    if Verified and User_Session:
        User_Email = User_Session['email']
        User_Dict=Server_Cache.get(User_Email)
        if 'User_Profile' in User_Dict:
            User_Profile=User_Dict['User_Profile']
            User_Details=zip(User_Profile[0],User_Profile[1])
            return render(request, 'profile.html',{'User_Details':User_Details})
        else:
            return Get_UserProfile(request,User_Session,sessionid,User_Email)
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
    User_Session=session.Db.Session_Generator(session.Db,email,[ID, {}])
    if email not in Server_Cache.Map:
        Server_Cache.Put(email,{})
    return User_Session

def Connection_Establishment(email,password,request):
    User.Db.connect(User.Db)
    User_Details=User.Db.login(User.Db,email,password)
    SessionId = session.Db.SessionId_Generator(session.Db)
    User_Session=Generate_Session(SessionId,email)
    Response=UserProfileResponse(request,User_Session,SessionId,User_Details,email)
    Response.set_cookie('id', SessionId)
    return Response

def UserProfileResponse(request,User_Session,SessionId,User_Details,email):
    Details=zip(User_Info_fields,User_Details)
    Response=render(request,'profile.html',{'User_Details': Details})
    UserInfoDict=Server_Cache.get(email)
    Server_Cache.Put(SessionId,User_Session)
    UserInfoDict['User_Profile']=[User_Info_fields,User_Details]
    Server_Cache.get(email,Update_Node=UserInfoDict)
    return Response

def Get_UserProfile(request, User_Session,sessionid,User_Email):
    User.Db.connect(User.Db)
    User_Details=User.Db.Query(User.Db, User_Email)
    return UserProfileResponse(request,User_Session,sessionid,User_Details,User_Email)

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
        print(e)

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
