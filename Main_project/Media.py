import mysql.connector
from mysql.connector import Error
import json

class Db:
    def connect(self):
        """ Connect to MySQL database """
        self.conn = None
        try:
            self.conn = mysql.connector.connect(host='127.0.0.1', database='rohan1', user='rohan', password='Lollol786', auth_plugin='mysql_native_password', port=9999)
            self.pointer = self.conn.cursor()
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)

    def InitializeUserTraceInMedia(self,email):
        self.connect(self)
        SerializedDict=json.dumps({})
        User_Info=[email,SerializedDict,SerializedDict]
        UserQuery=("INSERT INTO media(email, Videos, Images)VALUES (%s, %s, %s)")
        self.pointer.execute(UserQuery,User_Info)
        self.conn.commit()
        
    def Upload_Video(self,email,VideosDict):
        SerializedDict=json.dumps(VideosDict)
        UploadQueryForVideos = (f"update media set Videos = '{SerializedDict}' where email = '{email}'")
        self.pointer.execute(UploadQueryForVideos)
        self.conn.commit()

    def Upload_Image(self,email,ImagesDict):
        SerializedDict=json.dumps(ImagesDict)
        UploadQueryForImages = (f"update media set Images = '{SerializedDict}' where email = '{email}'")
        self.pointer.execute(UploadQueryForImages)
        self.conn.commit()

    def Query(self,email):
        try:
            UserQuery=(f"select * from media where email = '{email}'")
            self.pointer.execute(UserQuery)
            for Query in self.pointer:
                return Query
        except:
            return False