import mysql.connector
from mysql.connector import Error


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

    def create_user(self, User_Info):
        add_user = ("INSERT INTO UserInfo(firstname, lastname, username, email, cell, DOB, password)VALUES (%s, %s, %s, %s, %s, %s, %s)")
        self.pointer.execute(add_user, User_Info)
        self.conn.commit()

    def display(self):
        self.connect(self)
        self.pointer.execute("select * from proxect")
        for content in self.pointer:
            print(content)

    def login(self,mail,password):
        result=self.Query(self,mail)
        if type(result) is str or password != result[-1]:
                result=None
        return result

    def Query(self,email):
        query = f"select * from proxect where email='{email}'"
        try:
            self.pointer.execute(query)
        except Exception as e:
            return "Invalid Query"
        for user in self.pointer:
            return user
