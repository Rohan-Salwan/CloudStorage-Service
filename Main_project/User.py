import mysql.connector
from mysql.connector import Error


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

    def create_user(self, User_Info):
        add_user = ("INSERT INTO UserInfo(firstname, lastname, username, email, login, cell, DOB, password)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        self.pointer.execute(add_user, User_Info)
        self.conn.commit()

    def login(self,mail,password):
        result=self.Query(self,mail)
        result=result[0]
        if type(result) is str:
            print(result)
        else:
            if result[4] == 0 and password == result[-1]:
                self.Helper_For_LoginAndLogout(self,mail,1)
                print("login succesful")
            elif result[4] == 0 and password !=result[-1]:
                print("Invalid password")
            else:
                print("Invalid Email")
    
    def logout(self,email):
        try:
            self.Helper_For_LoginAndLogout(self,email,False)
        except Exception as e:
            print(e)

    def Helper_For_LoginAndLogout(self,email,command):
        try:
            query=f"update UserInfo set login = {command} where email = '{email}'"
            self.pointer.execute(query)
            self.conn.commit()
        except Exception as e:
            print("problem with database")    

    def Query(self,email):
        query = f"select * from UserInfo where email='{email}'"
        credentials=[]
        try:
            self.pointer.execute(query)
        except Exception as e:
            return "Invalid Query"
        for user in self.pointer:
            credentials.append(user)
        return credentials