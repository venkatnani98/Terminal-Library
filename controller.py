import view,model
 


def start():
    choice = '0'
    while choice != '3':
        choice = view.start_options()
        if choice == '1':     # Admin Login
            username,password = view.admin_login()
            login = model.Library.admin_login(username,password)
            if login == False:
                view.login_as_user()
            elif login == None:
                view.invalid_credentials()
            else:
                admin_options(login)
               # break
            
        elif choice == '2': # Individual Login
            choice = view.user_home()
            if choice == '1': #User Login
                mobile,password = view.user_login()
                login = model.Library.user_login(mobile,password)  #login should return Library(username,password, mobile)
                if login == False:
                    view.invalid_credentials()
                else:
                    view.success_login
                    user_options(login)

            elif choice == '2': #User Register
                username,password,mobile = view.new_user()
                account_type = 'User'
                new = model.Library(username,password,mobile,account_type)
                result = new.new_user()
                if result != False:
                    view.user_created()
                    user_options(new)
                else:
                    view.user_exists()
            elif choice == '3':
                view.exit()
                break
            else:
                view.invalid()
        
        elif choice == '3':
             view.exit()
             break
        else:
            view.invalid()

def admin_options(login):
    choice = '0'
    while choice != '7':
        choice = view.admin_home()
        if choice == '1':
             ch = view.modify_books()
             if ch == '1':
                code,name,author,publisher = view.add_books()
                book = model.Books(code,name,author,publisher)
                result = book.add_books()
                if result == True:
                   view.book_success()
             elif ch == '2':
                book_id = view.select_book()  
                result = model.Books.modify_book_details(book_id)
                view.books_full_details(result)
                choice = view.confimation()
                if choice == '1':
                    res = model.Books.books_delete(book_id)
                    if res == True:
                        view.book_deleted()
                    else:
                        view.book_notdeleted()
                else:
                    view.book_notdeleted()
        elif choice == '2':
             key = view.book_details()
             result = model.Books.book_details(key)
             view.books_full_details(result)
        elif choice == '3':
            username,password,mobile,account_type = view.admin_new_user()
            new = model.Library(username,password,mobile,account_type)
            if new != False:
                result = new.admin_new_user()
                view.user_created()
            else:
                view.user_exists()
        elif choice == '4':
            result = login.user()
            view.users(result)
        elif choice == '5':
            choice = view.Modify()
            if choice == '1':
                mobile = view.user_mobile()
                result = login.user_details(mobile) 
                choice = view.confirm(result)
                if choice == True:
                    username,password, new_mobile, account_type = view.Modify_user()
                    result = login.duplicate_check(username,new_mobile,mobile)
                    if result == False:
                        output = login.modify_user(username,password, new_mobile, account_type, mobile)
                        view.updated_user(output)
                    else:
                        view.duplicates_found()
            elif choice == '2':
                mobile = view.delete_user()
                result = login.user_details(mobile)  
                confirm = view.confirm(result)
                if confirm == True:
                    res = login.delete(mobile)
                    if res == True:
                        view.user_deleted()
                    else:
                        view.delete_error()
                else:
                    view.notdeleted()
            elif choice == '3':
                continue
            else:
                view.invalid()
        elif choice == '6':
            rent_choice = view.rent_menu()
            if rent_choice == '1':
                username,mobile,book_taken = view.rent_book()
                result = login.rent_details(username,mobile,book_taken)
                if result == True:
                    view.details_added()
                    login.admin_rent_a_book(book_taken)
                else:
                    view.details_mismatch()
            elif rent_choice == '2':
                mobile_no = view.user_mobile()
                rt_details = login.rt_details(mobile_no)
                view.rent_details(rt_details)
                book_id,rtn_date = view.update_rtn()
                output = login.update_rtn(book_id,rtn_date,mobile_no)
                if output != False:
                   fees = view.fee_calculations(output)
                   result = login.rent_result(fees,book_id,mobile_no)
                   view.rent_details(result)
                   choice = view.amount_rec()
                   if choice == '1':
                        result = login.amount_received(book_id,mobile_no,fees,rtn_date)
                        if result == True:
                           view.payment()
                           login.delete_record(book_id,mobile_no)
                   elif choice == '2':
                       continue
                else:
                    view.invalid()
            elif rent_choice == '3':
                status = login.rental_details()
                view.rent_details(status)
            elif rent_choice == '4':
                continue
            else:
                view.invalid()
        elif choice == '7':
            view.exit()
        else:
            view.invalid()
    
    

def user_options(new):
    if new == None:
        view.login_as_admin()
    else:
        status = new.user_home()
        view.acc_status(status)
        choice = '0'
        while choice != None:
            choice = view.user_options()
            if choice == '1':
                status = model.Books.books_full_details()
                view.books_full_details(status)

            elif choice == '2':
                key = view.book_details()
                result = model.Books.book_details(key)
                view.books_full_details(result)
                book_id = view.select_book()
                result = new.rent_a_book(book_id)
                if result == True:
                    view.book_rented()
            
            elif choice == '3':
                 status = new.dues_status()
                 view.rent_details(status)
                 view.Fee_details()

            elif choice == '4':
                password = view.password()
                result = new.password_update(password)
                view.password_updated()
            elif choice == '5':
                view.exit()
                return
            else:
                view.invalid()
    

model.create_databases()
start()