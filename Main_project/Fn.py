from django.shortcuts import render
from . import Mysql
from . import session
import json
import time

    
def Get_UserFieldValues(request):
    User_Info_fields = ['FirstName', 'LastName', 'Username', 'Email', 'Contact', 'DOB', 'Password']
    User_Info = []
    for field in User_Info_fields:
        if field=='Contact':
            User_Info.append(False)
        User_Info.append(request.POST[field])
    return User_Info

def Create_User(User_Info):
    Mysql.Db.connect(Mysql.Db,'rohan1')
    Mysql.Db.create_user(Mysql.Db,User_Info)

def Assign_SessionId(User_Request):
    SessionId = session.Db.SessionId_Generator(session.Db)
    Response=render(User_Request,'Login_Sucessful.html')
    Response.set_cookie('id', SessionId)
    return Response, SessionId

def Generate_Session(ID):
    session.Db.connect(session.Db,'rohan1')
    session.Db.Session_Generator(session.Db,[ID, {}])

def Connection_Establishment(email,password):
    Mysql.Db.connect(Mysql.Db,'rohan1')
    Mysql.Db.login(Mysql.Db,email,password)

def Verify_Session(SessionId):
    User_Session = Get_DeserializedSession(SessionId)
    if User_Session:
        Valid_Session = SessionExpire_Checker(User_Session)
        return Valid_Session
    else:
        return False

def Get_DeserializedSession(SessionId):
    try:
        session.Db.connect(session.Db, 'rohan1')
        UserSessionInfo_List = session.Db.Query(session.Db,SessionId)
        User_Session = UserSessionInfo_List[1]
        Deserialized_UserSession = json.loads(User_Session)
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
    session.Db.connect(session.Db,'rohan1')
    session.Db.Delete_Session(session.Db,session_id)
