def start_options():   # HOME SCREEN
    choice = input('''______________Welcome to My Library______________
    Login to Library as
    1. Librarian(Staff only)
    2. Individual User
    3. Exit
    ''')
    return choice

#Create Tables
def books_table():
    return  ("create table if not exists books_table(Book_Code varchar(255) Unique, Name varchar(255), Author varchar(255), Publisher varchar(255), Availability varchar(255) Default 'Available');")
    
def admin_table():
    return ("create table if not exists admin_table(Username varchar(255) Unique, Password varchar(255), Mobile int(30) Unique, Account_type varchar(255) Default 'User', Primary key(Mobile));")

def user_table():
    return ("create table if not exists user_table(Username varchar(255),Mobile int(30), Book_taken varchar(255) Default 'Not Available', Rented_date date, Return_date date, Returned_On date Default NULL, FOREIGN KEY (Username) REFERENCES admin_table(Username),FOREIGN KEY (Mobile) REFERENCES admin_table(Mobile),FOREIGN KEY (Book_taken) REFERENCES books_table(Book_Code));")

def user_status():
    return ('create view user_status as select Mobile,Book_taken,Rented_date from user_table;')

#Login

def admin_login():
    username = input("Enter your username : ")
    password = input("Enter your password : ")
    return username,password

def user_login():
    mobile = int(input("Enter Registered Mobile Number : "))
    password = input("Enter your Password : ")
    return mobile,password

def success_login():
    print("Login Successful.")

def invalid_credentials():
    print("Invalid credentials.")

def login_as_user():
    print("Password Incorrect / You are not Admin, Please login using Individual User Option.")

def login_as_admin():
    print("Mobile registered as Admin(Staff). Please Login in Admin Portal.")



def admin_home():  #Admin Home
    options = input('''_________Welcome Admin_________
    1. Add/Delete Books
    2. Search Book and Availability
    3. Add New User Details
    4. Display All Users
    5. Modify User Details
    6. Rent a Book
    7. Logout
    ''')  # 4.Earlier only Delete option available b 
    return options

def modify_books():
    options = input('''Select an option:
    1. Add Books
    2. Delete Books
    ''')
    return options

def add_books():
    code = input("Enter Book Code : ")
    name = input("Enter Book Name : ")
    author = input("Enter Book Author : ")
    publisher = input("Enter Book Publisher : ")
    return code,name,author,publisher

def book_success():
    print("Book Sucessfully Inserted to the Library.")

def book_details():
    code = input("Enter Book Name or any Key Word : ")
    return code

def details(result):
    x=0
    a = ['Code','Name','Author','Publisher','Availability']
    for i in result:
        print(a[x], ":", i)
        x += 1

def new_user():
    username = input("Enter New Username : ")
    password1 = input("Enter New Password : ")
    password2 = input("Re-enter New Password : ")
    mobile = input("Enter Mobile : ")
    if password1 == password2:
        return username,password1,mobile
    else:
        print("Password Mismatch")
        new_user()
def admin_new_user():
    username = input("Enter New Username : ")
    password1 = input("Enter New Password : ")
    password2 = input("Re-enter New Password : ")
    mobile = input("Enter Mobile : ")
    account_type = input("Enter Account Type(Admin/User) : ")
    if password1 == password2:
        return username,password1,mobile,account_type
    else:
        print("Password Mismatch")
        admin_new_user()

def user_created():
    print("User Created Successfully.")

def delete_user():
    user = input("Enter Mobile number of the user to delete : ")
    return user
def confirm(result):
    if result != None:
        x=0
        list = ("Username","Password","Mobile","Account-type")
        for i in result:
            print(list[x] ,":", i )
            x+=1
        choice = input('''Do you want to proceed : 
        1. Yes      2. No
        ''')
        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("Invalid Input")
    else:
        print("User not available with given mobile number.")
def user_deleted():
    print("User Deleted Successfully.")
def notdeleted():
    print("User Not Deleted")
def invalid():
    print("Invalid Mobile number.")

def username():
    username = input("Enter Username of User : ")
    return username

def  Modify():
    choice = input('''Select an Option:
    1. Modify User Details
    2. Delete User
    3. Back to Menu
    ''')
    return choice

def Modify_user():
    print("----------Edit New Details----------")
    username = input("Enter New Username : ")
    password1 = input("Enter New Password : ")
    mobile = input("Enter Mobile : ")
    account_type = input("Enter Account Type(Admin/User) :")
    return username,password1,mobile, account_type

def updated_user(output):
    print("Updated Details:")
    x=0
    list = ("Username","Password","Mobile","Account-type")
    for i in output:
        print(list[x] ,":", i )
        x+=1

def duplicates_found():
    print("New Username or New Mobile already exists.")

def delete_error():
    print("Books reserved on User Mobile. Kindly clear dues to delete user.")

def confimation():
    choice = input('''Confirm Deletion:
    1. Yes     2. No
    ''')
    return choice

def book_deleted():
    print("Book deleted Successfully.")

def book_notdeleted():
    print("Book not Deleted.")

#RENTIng book

def rent_book():
    print("Add Details Below : ")
    username = input("Enter Username : ")
    mobile = input("Enter Mobile Number : ")
    book_taken = input("Enter Book Code : ")
    return username,mobile,book_taken

def rent_menu():
    choice = input('''-----Rent Menu-----
    1. Rent New Book
    2. Update Return Details
    3. Display all Rented Details
    4. Back to Menu
    ''')
    return choice

def details_added():
    print("Details added Successfully")

def details_mismatch():
    print("Mentioned Username or Mobile Number were not Registered.")

def invalid():
    print("Invalid.")

def exit():
    print("Exited Succesfully.")

def user_mobile():
    mob = int(input("Enter User Mobile : "))
    return mob

def rent_details(rt_details):
    x=0
    a = ['Username','Mobile','Book_taken','Rented_date','Return_by','Returned_On','Fees_Due','Payment']
    if len(rt_details) == 1:
        list = rt_details[0]
        for i in list:
            print(a[x], ":", i)
            x += 1
    else:
        for row in rt_details:
           print("___________________________")
           x = 0
           for y in row:
               print(a[x],":", y)
               x += 1

def update_rtn():
    book_id = input("Select Book ID : ")
    rtn_date = input("Input Return Date (YYYY-MM-DD) : ")
    return book_id,rtn_date

def fee_calculations(days):
    fee = 0
    while True:
        if days <= 20:
            return fee
        elif days > 20:
            fee = 50
            total = fee + fee_calculations(days-20)
            return  total


def Fee_details():
    print('''Fee Details:
    1. If Book Returned in less than 20 days = Rs.0
    2. If Book Returned after 20 days = Rs. 50/-
    3. And there after Rs.50 will be added for every 20 days
    ''')

def return_fees(result):
    x = 0
    list = ['Username','Mobile','Book_ID','Rented_date','Return_by','Returned_On','Fees_Due','Payment']
    for i in result:
        print(list[x], ":", i)
        x += 1

def amount_rec():
    choice = input('''Fee Amount Recieved ?
    1. Yes     2. No
    ''')
    return choice

def payment():
    print("Payment Successful.")

def users(rt_details):
    x=0
    a = ["Username","Password","Mobile","Account-type"]
    if len(rt_details) == 1:
        list = rt_details[0]
        for i in list:
            print(a[x], ":", i)
            x += 1
    else:
        for row in rt_details:
           print("___________________________")
           x = 0
           for y in row:
               print(a[x],":", y)
               x += 1



#USER MENU

def user_home():
    choice = input('''----------User Home-----------
    Select an Option:
    1. Login
    2. Register
    3. Exit
    ''')
    return choice

def user_exists():
    print("User details already exists, Please Login.")

def acc_status(status):
    x = 0
    list = ("Mobile","Book Code","Rented date","Return_by","Returned_On","Fees_Due","Payment")
    for row in status:
        x = 0
        print("___________________________")
        for y in row:
            print(list[x],":", y)
            x += 1
    
def user_options():
    option = input('''----------User Menu----------
    Select an option:
    1. Show All Books
    2. Search a Book and Rent
    3. Check Fees Due   
    4. Change password
    5. Exit
    ''')
    return option    

def select_book():
    book_id = input("Enter Book Code : ")
    return book_id

def book_rented():
    print("Book Reserved for you. Please collect it from Librarian.")

def books_full_details(status):
     list = ("Book Code","Name","Author","Publisher","Availability")
     for row in status:
        x = 0
        print("___________________________")
        for y in row:
            print(list[x],":", y)
            x += 1

def password():
    password1 = input("Enter New Password : ")
    password2 = input("Re-enter New Password : ")
    if password1 == password2:
        return password1
    else:
        print("Password Mismatched. Try Again.")

def password_updated():
    print("Password Updated.")