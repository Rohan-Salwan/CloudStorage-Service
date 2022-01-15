from urllib import response
from django.shortcuts import render
from . import cache
from . import User
from . import session
import json
import time

Server_Cache=cache.Cache()

User_Info_fields = ['FirstName', 'LastName', 'Username', 'Email', 'Contact', 'DOB', 'Password']

def VideoRequest_Handler(request,Verified,User_Session,sessionid):
    if Verified and User_Session:
        if 'User_Videos' in User_Session:
            UserVideos_Dict=User_Session['User_Videos']
            return render(request, 'Videos.html', {'UserVideo': UserVideos_Dict})
        else:
            UserEmail=User_Session['email']
            UserVideos_Dict=None# query with UserEmail in video database and get deserialized dict object.
            User_Session['User_Videos']=UserVideos_Dict
            Server_Cache.get(sessionid,Update_Node=User_Session)
            return render(request,'Videos.html', {'UserVideo': UserVideos_Dict})

def Get_UserFieldValues(request):
    User_Info = []
    for field in User_Info_fields:
        User_Info.append(request.POST[field])
    return User_Info

def Create_User(User_Info):
    User.Db.connect(User.Db)
    User.Db.create_user(User.Db,User_Info)

def Generate_Session(ID,email):
    session.Db.connect(session.Db)
    session.Db.Session_Generator(session.Db,email,[ID, {}])

def Connection_Establishment(email,password,request):
    User.Db.connect(User.Db)
    User_Details=User.Db.login(User.Db,email,password)
    SessionId = session.Db.SessionId_Generator(session.Db)
    User_Session=Generate_Session(SessionId,email)
    Response=Preparing_ResponseForUser(request,User_Session,SessionId,User_Details)
    Response.set_cookie('id', SessionId)
    return Response

def Preparing_ResponseForUser(request,User_Session,SessionId,User_Details):
    User_Profile=zip(User_Info_fields,User_Details)
    Response=render(request,'profile.html',{'User_Details': User_Profile})
    User_Session['User_Profile']=User_Profile
    Server_Cache.Put(SessionId,User_Session)
    return Response

def Get_UserProfile(request, User_Session,sessionid):
    User_Email=User_Session['email']
    User.Db.connect(User.Db)
    User_Details=User.Db.Query(User.Db, User_Email)
    return Preparing_ResponseForUser(request,User_Session,sessionid,User_Details)

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
        email=User_Session['email']
        return True
    else:
        sessionid = User_Session['session_id']
        delete_session(sessionid)
        return False

def delete_session(session_id):
    session.Db.connect(session.Db)
    session.Db.Delete_Session(session.Db,session_id)
