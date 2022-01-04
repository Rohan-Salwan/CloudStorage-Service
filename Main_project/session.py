import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random
import time
import json

class Db:
    def connect(self):
        """ Connect to MySQL database """
        self.conn = None
        try:
            self.conn = mysql.connector.connect(host='rohan1.clcyfsk0gweh.us-east-1.rds.amazonaws.com', database='UserInfoDatabase', user='djangoDb', password='Lollol786+', auth_plugin='mysql_native_password', port=3306)
            self.pointer = self.conn.cursor()
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)
    
    def Session_Generator(self,User_Info):
        User_Info=self.TimeDateSetter_And_Serialization(self, User_Info)
        add_user = ("INSERT INTO session(session_id, session)VALUES (%s, %s)")
        self.pointer.execute(add_user, User_Info)
        self.conn.commit()
    
    def SessionId_Generator(self):
        try:
            id=random.randint(1,1000000000)
            return id
        except Exception as e:
            print("Error Occured in random module")    
    
    def Query(self,session_id):
        query = f"select * from session where session_id = {session_id}"
        try:
            self.pointer.execute(query)
            for user in self.pointer:
                return user
        except Exception as e:
            return "Invalid Query" 
    
    def Delete_Session(self,session_id):
        query=f"delete from session where session_id = {session_id}"
        try:
            self.pointer.execute(query)
        except Exception as e:
            return "Invalid Query"

    def TimeDateSetter_And_Serialization(self,List):
        Local_Time=datetime.now()
        Login_Time=Local_Time.strftime("%H:%M:%S")
        date=time.strftime("%d %b %Y ")
        List[1]['Date'] = date
        List[1]['Time'] = Login_Time
        Session_Dict = List.pop(-1)
        Serialized_Dict = json.dumps(Session_Dict)
        List.append(Serialized_Dict)
        return List
