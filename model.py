import mysql.connector
from mysql.connector import Error
from datetime import datetime 
from datetime import timedelta 

import logging
 
logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(filename="Books_rent_data.log", format = "%(message)s", filemode='w')

#MySQL Connection and Query Execution


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host = 'localhost', database = 'library', user = 'root', password = 'Nani')
            if self.connection.is_connected:
                self.cursor = self.connection.cursor(buffered=True)
                #print (f'Database connnected to ''Library'' and Cursor created')
        except Error as e:
            return e

    def execute_query(self,query):
        try:
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            return e
        finally:
            return self.cursor
            self.cursor.close()
Db = Database()

def create_databases():
    b_table = "create table if not exists books_table(Book_Code varchar(255) Unique, Name varchar(255), Author varchar(255), Publisher varchar(255), Availability varchar(255) Default 'Available');"
    Db.execute_query(b_table)
    a_table = "create table if not exists admin_table(Username varchar(255) Unique, Password varchar(255), Mobile bigint(30) Unique, Account_type varchar(255) Default 'User', Primary key(Mobile));"
    Db.execute_query(a_table)
    u_table = "create table if not exists user_table(Username varchar(255),Mobile bigint(30), Book_Code varchar(255) UNIQUE, Rented_date date, Return_by date NULL, Returned_On date Default NULL, Fees_Due int Default 0, Payment varchar(255) Default 'Unpaid', FOREIGN KEY (Username) REFERENCES admin_table(Username),FOREIGN KEY (Mobile) REFERENCES admin_table(Mobile),FOREIGN KEY (Book_Code) REFERENCES books_table(Book_Code));"
    Db.execute_query(u_table)
    u_status = 'create view user_status as select Mobile,Book_Code,Rented_date,Return_by,Returned_On, Fees_Due, Payment from user_table;'
    Db.execute_query(u_status)

class Library:
    def __init__(self,username,password,mobile,account_type):
        self.username = username
        self.password = password
        self.mobile = mobile
        self.account_type = account_type

    @classmethod   
    def admin_login(cls,username,password):    
        try:            
           query = (f"select * from admin_table where Username = '{username}';")
           my_cursor = Db.execute_query(query)
           row = my_cursor.fetchone()
        except Error as e:
           print (e)
        finally:
           if row == None:
               return None
           elif username in row and password in row and 'Admin' in row:
               mobile = row[2]
               account_type = row[3]
               login = Library(username,password, mobile,account_type)
               return login
           elif username in row and password in row and 'Admin' not in row:
               return False

    def user(self):
        try:
            query = ("select * from admin_table;")
            my_cursor = Db.execute_query(query)
            row = my_cursor.fetchall()
            return row
        except Error as e:
           print (e)
    
    @classmethod
    def user_login(cls,mobile,password):                                   
        try:
            query = (f"select * from admin_table where Mobile = {mobile};")
            my_cursor = Db.execute_query(query)
            row = my_cursor.fetchone()
        except Error as e:
            print (e)
        finally:
            if row == None:
               return False
            elif mobile in row and password in row and 'User' in row:
                username = row[0]
                account_type = row[3]
                login = Library(username,password, mobile,account_type)
                return login
    
    def new_user(self):
        result = Library.admin_login(self.username,self.password)
        if result == None:
            try:
               query = (f"insert into admin_table values('{self.username}', '{self.password}', {self.mobile}, '{self.account_type}');")
               Db.execute_query(query)
               return result
            except Error as e:
                print (e)
        else:
            return False

    def admin_new_user(self):
        try:
            result = Library.admin_login(self.username,self.password)
            if result == None:
                 query = (f"insert into admin_table values('{self.username}', '{self.password}', {self.mobile},'{self.account_type}');")
                 Db.execute_query(query)
                 return result
            else:
                return False
        except Error as e:
           print (e)

    def user_details(self,mobile):
        try:
            query = (f"select * from admin_table where mobile = {mobile};")
            my_cursor = Db.execute_query(query)
            row = my_cursor.fetchone()
            return row
        except Error as e:
            print("User Not Found :",e)
    
    def delete(self,mobile):
        try:
           query = (f"delete from admin_table where mobile = {mobile};")
           Db.execute_query(query)
           return True
        except Error as e:
            return False

    def rent_details(self,username,mobile,book_taken):
        try:
           today = datetime.now()
           rented_date = today.strftime("%Y-%m-%d")
           rtn =  today + timedelta(days=20)
           return_date = rtn.strftime("%Y-%m-%d")
           query =  (f"insert into user_table(Username, Mobile, Book_Code, Rented_date, Return_by) values('{username}', {mobile}, '{book_taken}','{rented_date}','{return_date}');")
           Db.execute_query(query)
           return True
        except Error as e:
           print (e)
    
    def user_home(self):
        try:
           query = (f"select * from user_status where mobile = {self.mobile} and Payment = 'Unpaid';")
           my_cursor = Db.execute_query(query)
           status = my_cursor.fetchall()
           return status
        except Error:
             print("Books not Available")

    def rental_details(self):
        try:
           query = ("select * from user_table")
           my_cursor = Db.execute_query(query)
           status = my_cursor.fetchall()
           return status
        except Error as e:
           print (e)

    def rt_details(self,mobile_no):
        try:
           query = (f"select * from user_table where Mobile = {mobile_no}")
           my_cursor = Db.execute_query(query)
           status = my_cursor.fetchall()
           return status
        except Error as e:
           print (e)

    def update_rtn(self,book_id,rtn_date,mobile_no):
        try:
           query = (f"update user_table SET Returned_On ='{rtn_date}' where Book_Code = '{book_id}' and Mobile = {mobile_no};")
           Db.execute_query(query)
           query1 = (f"select *, DATEDIFF(Returned_On,Rented_date) as day from user_table where Book_Code = '{book_id}' and Mobile = {mobile_no};")
           my_cursor = Db.execute_query(query1)
           Output = my_cursor.fetchone()
           if Output != None:
               days = Output[8]
               return days
           else:
                return False
        except Error:
            print("Please check Date Format")
        finally:
            query2 = (f"update books_table set Availability = 'Available' where Book_Code = '{book_id}';")
            Db.execute_query(query2)

    def rent_result(self,fees,book_id,mobile_no):
        try:
           query = (f"Update user_table set Fees_Due = {fees}  where Book_Code = '{book_id}' and Mobile = {mobile_no};")
           Db.execute_query(query)
           query1 = (f"select * from user_table where Book_Code = '{book_id}' and Mobile = {mobile_no}")
           my_cursor = Db.execute_query(query1)
           Output = my_cursor.fetchmany()
           return Output
        except Error as e:
           print (e)

    def amount_received(self,book_id,mobile_no,fees,rtn_date):
        try:
           query = (f"update user_table set Payment = 'Paid' where Book_Code = '{book_id}' and Mobile = {mobile_no};")
           Db.execute_query(query)
           logging.info(f"User with Mobile - '{mobile_no}', rented Book - '{book_id}', returned on '{rtn_date}', Paid Amount - '{fees}'")
           return True
        except Error:
            return False
        
    def delete_record(self,book_id,mobile_no):
        try:
           query = (f"delete from user_table where Book_Code = '{book_id}' and Mobile = {mobile_no};")
           Db.execute_query(query)
        except Error as e:
           print (e)

    def duplicate_check(self,username,new_mobile, mobile):
        try:
           query = (f"select * from admin_table where Username = '{username}';")
           my_cursor = Db.execute_query(query)
           Username_list = my_cursor.fetchone()
           query = (f"select * from admin_table where Mobile = '{new_mobile}';")
           my_cursor = Db.execute_query(query)
           Mobile_list = my_cursor.fetchone()
           if Username_list != None:   # NEED to modify
               if mobile in Username_list:
                   result1 = False
           else:
               result1 = False
   
           if Mobile_list != None:
               if username in Mobile_list:
                   result2 = False
           else:
               result2 = False
                     
           if result1 == False or result2 == False:
               return False
          
           else:
               True
        except Error as e:
           print (e)

    def modify_user(self,username,password, new_mobile, account_type, mobile):
        try:
           query = (f"update admin_table set Username = '{username}', Password = '{password}', Mobile = {new_mobile},Account_type = '{account_type}' where Mobile = {mobile};")
           Db.execute_query(query)
           query1 = (f"select * from admin_table where Mobile = {new_mobile};")
           my_cursor = Db.execute_query(query1)
           Output = my_cursor.fetchone()
           return Output
        except Error as e:
           print (e)

    def rent_a_book(self,book_id):
        try:
           today = datetime.now()
           rented_date = today.strftime("%Y-%m-%d")
           rtn =  today + timedelta(days=20)
           return_date = rtn.strftime("%Y-%m-%d")
           query =  (f"insert into user_table(Username, Mobile, Book_Code, Rented_date, Return_by) values('{self.username}', {self.mobile}, '{book_id}','{rented_date}','{return_date}');")
           Db.execute_query(query)
           return True
        except Error:
            print("Selected Book not Available.")
        finally:
            query = (f"update books_table set Availability = 'Not Available' where Book_Code = '{book_id}';")
            Db.execute_query(query)

    def admin_rent_a_book(self,book_id):
        try:
            query = (f"update books_table set Availability = 'Not Available' where Book_Code = '{book_id}';")
            Db.execute_query(query)
        except Error as e:
           print (e)

    def password_update(self,password):
        try:
           query = (f"update admin_table set Password = '{password}' where Mobile = {self.mobile};")
           Db.execute_query(query) 
        except Error as e:
           print (e)

    def dues_status(self):
        try:
           query = (f"select * from user_table where Mobile = {self.mobile}")
           my_cursor = Db.execute_query(query)
           Output = my_cursor.fetchall()
           return Output
        except Error as e:
           print (e)

# Book Not Available Feature



class Books:
    def __init__(self,code,name,author,publisher):
        self.code = code
        self.name = name
        self.author = author
        self.publisher = publisher

    
    def add_books(self):
        try:
           query = (f"insert into books_table(Book_Code,Name,Author,Publisher) values('{self.code}','{self.name}','{self.author}','{self.publisher}');")
           Db.execute_query(query)
           return True
        except Error as e:
           print (e)

    @classmethod
    def book_details(cls,key):
        try:
           query = (f"select * from books_table where Name like '%{key}%';")
           my_cursor = Db.execute_query(query)
           row = my_cursor.fetchall()
           return row
        except Error as e:
           print (e)

    @classmethod
    def modify_book_details(cls,book_id):
       try:
           query = (f"select * from books_table where Book_Code = '{book_id}';")
           my_cursor = Db.execute_query(query)
           row = my_cursor.fetchall()
           return row
       except Error as e:
            print (e)

    def books_full_details():
        try:
           query = ("select * from books_table;")
           my_cursor = Db.execute_query(query)
           result = my_cursor.fetchall()
           return result
        except Error as e:
           print (e)
    
    @classmethod
    def books_delete(cls,book_id):
        try:
           query = (f"delete from books_table where Book_Code = '{book_id}';")
           Db.execute_query(query)
           return True
        except:
            return False

        