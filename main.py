#!/usr/bin/env python
                                                #Login System
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

root = Tk()
root.title("Login_screen")
root.geometry("420x300")

age = 0

# function to find age
def find_age():
    global age, birth, warning_label, age_box
    birth_date = cal.get()

    # replace "/" with "" <str> 29052021
    birth_date_stg = birth_date.replace("/", "")

    # convert <str> value to <datetime.datetime> value 2021-05-29 00:00:00
    birth = datetime.strptime(birth_date_stg, "%d%m%Y")

    # removes time stamp and return <datetime.datetime> value 2021-05-29
    birth = birth.date()

    # gives current date
    now = datetime.now()

    current_year = now.year
    birth_year = birth.year

    current_month = now.month
    birth_month = birth.month

    currrent_day = now.day
    birth_day = birth.day

    age = current_year - birth_year
    if age < 0:
        warning_label = Label(signup_window, text="WARNING!\nAge cannot be smaller than 0.")
        warning_label.place(x=10, y=300)
    else:
        warning_label.place_forget()
        if current_month == birth_month:
            if currrent_day < birth_day:
                age -= 1
            else:
                age = current_year - birth_year
        elif current_month < birth_month:
            age -= 1
        else:
            age = current_year - birth_year

        age_box = Label(signup_window, text=age, width="5", bd=3, relief=SUNKEN)
        age_box.place(x=230, y=130)

# show password (signup screen)
def tick_sign():
    global password_box, var_sign, val_sign
    val_sign = password_box.get()
    password_box.delete(0, END)
    # shows password if onvalue is show or otherwise its hidden
    if var_sign.get() == 'show':
        password_box.configure(show="")
        password_box.insert(0, val_sign)
    else:
        password_box.configure(show="*")
        password_box.insert(0, val_sign)

# show confirm password (signup screen)
def tick_sign1():
    global confirm_password_box, var_sign1, val_sign1
    val_sign1 = confirm_password_box.get()
    confirm_password_box.delete(0, END)
    # shows password if onvalue is show or otherwise its hidden
    if var_sign1.get() == 'show':
        confirm_password_box.configure(show="")
        confirm_password_box.insert(0, val_sign1)
    else:
        confirm_password_box.configure(show="*")
        confirm_password_box.insert(0, val_sign1)

def check():
    global repeat_mail, repeat_num
    login_db = sqlite3.connect(database='user_credential.db')

    # creating cursor object
    mycursor = login_db.cursor()

    # Checks for repeat mail and phone so that these can't be repeated
    check_mail = """
               SELECT COUNT(email_address) AS CNT, email_address
               FROM signup_credential
               GROUP BY email_address
               HAVING CNT = 1;                
               """
    check_num = """
               SELECT COUNT(phone_num) AS CNT, phone_num
               FROM signup_credential
               GROUP BY phone_num
               HAVING CNT = 1;
              """

    mycursor.execute(check_mail)
    mail_repeat = mycursor.fetchall()
    mycursor.execute(check_num)
    num_repeat = mycursor.fetchall()

    #Check repeat mail
    mail_list = []
    for x in range(len(mail_repeat)):
        for y in range(1, 2):
            mail_list.append(mail_repeat[x][y])
    to_check = email_address_box.get()
    repeat_mail = ""
    for i in mail_list:
        if i == to_check:
            repeat_mail = i
        else:
            continue

    #Check repeat phone no.
    num_list = []
    for p in range(len(num_repeat)):
        for q in range(1, 2):
            num_list.append(num_repeat[p][q])
    to_check = phone_box.get()
    repeat_num = ""
    for i in num_list:
        if i == to_check:
            repeat_num = i
        else:
            continue

    login_db.commit()

    login_db.close()


# define functionality of submit button
def submit():
    global warning_label, confirm_label, age_box, age, birth_date
    find_age()
    warning_label.place_forget()
    check()
    if first_name_box.get() == str(""):
        warning_label = Label(signup_window, text="WARNING!\nPlease fill the First name cell.")
        warning_label.place(x=10, y=300)
    elif last_name_box.get() == str(""):
        warning_label = Label(signup_window, text="WARNING!\nPlease fill the  Last name cell.")
        warning_label.place(x=10, y=300)
    elif email_address_box.get() == str(""):
        warning_label = Label(signup_window, text="WARNING!\nPlease fill the Email address cell.")
        warning_label.place(x=10, y=300)
    elif repeat_mail == email_address_box.get():
        warning_label = Label(signup_window, text="WARNING!\nEmail address already exist.")
        warning_label.place(x=10, y=300)
    elif select_gender.get() == "Choose":
        warning_label = Label(signup_window, text="WARNING!\nPlease select your gender from menu.")
        warning_label.place(x=10, y=300)
    elif age == 0:
        warning_label = Label(signup_window, text="WARNING!\nPlease select your date of birth, age cannot be 0.")
        warning_label.place(x=10, y=300)
    elif phone_box.get() == str(""):
        warning_label = Label(signup_window, text="WARNING!\nPlease fill the Mobile number cell.")
        warning_label.place(x=10, y=300)
    elif repeat_num == phone_box.get():
        warning_label = Label(signup_window, text="WARNING!\nPhone number already exist.")
        warning_label.place(x=10, y=300)
    elif password_box.get() == str(""):
        warning_label = Label(signup_window, text="WARNING!\nPlease fill the Password cell.")
        warning_label.place(x=10, y=300)
    elif confirm_password_box.get() == str(""):
        warning_label = Label(signup_window, text="WARNING!\nPlease fill the Confirm password cell.")
        warning_label.place(x=10, y=300)
    else:
        warning_label.place_forget()
        tick_sign()
        tick_sign1()
        confirm_label.place_forget()
        if val_sign != val_sign1:
            confirm_label = Label(signup_window, text="Password doesn't match")
            confirm_label.place(x=420, y=240)

        else:
            confirm_label = Label(signup_window, text="Password matched")
            confirm_label.place(x=420, y=240)

            """Insert collected data into DATABASE"""
            # Connecting to database
            login_db = sqlite3.connect(database='user_credential.db')

            # creating cursor object
            mycursor = login_db.cursor()

            # Preparing SQL query to INSERT a record into the database.
            sql = """
            INSERT INTO signup_credential 
            (first_name, last_name, email_address, sex, birth_date, age, phone_num, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            records = [
                (first_name_box.get(), last_name_box.get(), email_address_box.get(), select_gender.get(), birth, age, phone_box.get(), password_box.get())
            ]
            # Check weather user already exist in database

            try:
                # Executing the SQL command
                mycursor.executemany(sql, records)

                # Commit changes
                login_db.commit()

                # Popup message box to confirm data inserted successfully
                insert_message = messagebox.showinfo("Message", "Signup successful")
            except BaseException as e:
                # Rolling back in case of error
                login_db.rollback()
                print(e)

            # Close connection
            login_db.close()

            # Clear the cells
            email_address_box.delete(0, END)
            first_name_box.delete(0, END)
            last_name_box.delete(0, END)
            select_gender.set("Choose")
            cal = DateEntry(signup_window, locale="en_US", date_pattern="dd/mm/yyyy")
            cal.place(x=80, y=130)
            age_box = Label(signup_window, text=0, width="5", bd=3, relief=SUNKEN)
            age_box.place(x=230, y=130)
            phone_box.delete(0, END)
            password_box.delete(0, END)
            confirm_password_box.delete(0, END)
            confirm_label.place_forget()

            signup_window.destroy()


# define signup function
def signup():
    global cal, age_box, signup_window, password_box, var_sign, confirm_password_box, var_sign1, confirm_label, warning_label
    global first_name_box, last_name_box, email_address_box, select_gender, phone_box, password_box, confirm_password_box, age

    signup_window = Toplevel()
    signup_window.title("Signup_screen")
    signup_window.geometry("580x420")

    # signup screen entries box and labels
    intro_label = Label(signup_window, text="Enter correct information below and recheck before submitting.")
    intro_label.place(x=100, y=10)

    first_name_label = Label(signup_window, text="First name")
    first_name_label.place(x=10, y=50)
    first_name_box = Entry(signup_window, width=30, borderwidth=3)
    first_name_box.place(x=80, y=50)

    last_name_label = Label(signup_window, text="Last name")
    last_name_label.place(x=280, y=50)
    last_name_box = Entry(signup_window, width=30, borderwidth=3)
    last_name_box.place(x=350, y=50)

    email_address_label = Label(signup_window, text="Email address")
    email_address_label.place(x=10, y=90)
    email_address_box = Entry(signup_window, width=50, borderwidth=3)
    email_address_box.place(x=100, y=90)

    # Not funny :D
    sex_label = Label(signup_window, text="Sex")
    sex_label.place(x=420, y=90)
    options = ["Male", "Female", "Other"]
    select_gender = StringVar()
    select_gender.set("Choose")
    # Dropdown menu
    sex_box = OptionMenu(signup_window, select_gender, *options)
    sex_box.place(x=450, y=85)

    birth_date_label = Label(signup_window, text="Birth day")
    birth_date_label.place(x=10, y=130)
    # Date picker
    cal = DateEntry(signup_window, locale="en_US", date_pattern="dd/mm/yyyy")
    cal.place(x=80, y=130)

    # Age
    age_label = Label(signup_window, text="Age")
    age_label.place(x=190, y=130)
    age = 0
    age_box = Label(signup_window, text=age, width="5", bd=3, relief=SUNKEN)
    age_box.place(x=230, y=130)

    # gets calculated age
    get_button = Button(signup_window, text="Get", width=7, command=find_age)
    get_button.place(x=290, y=125)

    phone_label = Label(signup_window, text="Mobile number")
    phone_label.place(x=10, y=170)
    phone_box = Entry(signup_window, width=20, borderwidth=3)
    phone_box.place(x=110, y=170)

    # show password code snippet
    var_sign = StringVar()
    # checkbutton for show password
    show_clickbutton_sign = Checkbutton(signup_window, text="Show password", variable=var_sign, onvalue="show", offvalue="hide", command=tick_sign)
    show_clickbutton_sign.deselect()
    show_clickbutton_sign.place(x=270, y=220)

    password_label = Label(signup_window, text="Password")
    password_label.place(x=10, y=220)
    password_box = Entry(signup_window, show="*", width=30, borderwidth=3)
    password_box.place(x=80, y=220)

    # show confirm password code snippet
    var_sign1 = StringVar()
    # checkbutton for show confirm password
    show_clickbutton_sign1 = Checkbutton(signup_window, text="Show password", variable=var_sign1, onvalue="show", offvalue="hide", command=tick_sign1)
    show_clickbutton_sign1.deselect()
    show_clickbutton_sign1.place(x=320, y=260)

    confirm_password_label = Label(signup_window, text="Confirm password")
    confirm_password_label.place(x=10, y=260)
    confirm_password_box = Entry(signup_window, show="*", width=30, borderwidth=3)
    confirm_password_box.place(x=125, y=260)

    # Initial condition of this label's text is empty cause no password is entered
    confirm_label = Label(signup_window, text="")
    confirm_label.place(x=430, y=230)

    # Warning
    warning_label = Label(signup_window, text="")
    warning_label.place(x=10, y=300)

    # Submit button
    submit_button = Button(signup_window, text="Submit", width=12, height=4, command=submit)
    submit_button.place(x=240, y=330)

    exit_button = Button(signup_window, text="Exit", width=7, height=1, command=signup_window.destroy)
    exit_button.place(x=490, y=380)

# define login function
def login():
    global incorrect_label, prompt_window
    user_email = user.get()
    # Connecting to database
    login_db = sqlite3.connect(database='user_credential.db')

    # creating cursor object
    mycursor = login_db.cursor()

    retrive = """
    SELECT email_address, password
    FROM signup_credential;
    """
    mycursor.execute(retrive)
    info = mycursor.fetchall()

    # make mail, password dict
    user_mail_list = []
    for x in range(len(info)):
        for y in range(1):
            user_mail_list.append(info[x][y])


    user_pass_list = []
    for x in range(len(info)):
        for y in range(1, 2):
            user_pass_list.append(info[x][y])

    user_dict = {user_mail_list[i]: user_pass_list[i] for i in range(len(user_mail_list))}

    incorrect_label.place_forget()
    try:
        if user_email == str("") or psswd.get() == str(""):
            incorrect_label = Label(root, text="Fill the required field before login.")
            incorrect_label.place(x=100, y=200)

        elif user_dict[user_email] == psswd.get():
            user.delete(0, END)
            psswd.delete(0, END)

            prompt_window = Toplevel()
            prompt_window.title("User Info")
            prompt_window.geometry("370x300")

            # creating cursor object
            mycursor = login_db.cursor()

            user_info = """
            SELECT *
            FROM signup_credential
            WHERE email_address = ?            
            """

            selective_info = [user_email]
            mycursor.execute(user_info, selective_info)

            user_info_get = mycursor.fetchall()

            login_db.commit()

            login_db.close()

            login_label = Label(prompt_window, text="User Information(User ID: {})".format(user_info_get[0][0]), font=("Helvitica", 10))
            login_label.place(x=90, y=10)

            login_name_label = Label(prompt_window, text="Name:\t\t {0} {1}".format(user_info_get[0][1], user_info_get[0][2]))
            login_name_label.place(x=10, y=40)

            login_email_label = Label(prompt_window, text="Email address:\t {}".format(user_info_get[0][3]))
            login_email_label.place(x=10, y=60)

            login_sex_label = Label(prompt_window, text="Sex:\t\t {}".format(user_info_get[0][4]))
            login_sex_label.place(x=10, y=80)

            login_dob_label = Label(prompt_window, text="Date of Birth:\t {}".format(user_info_get[0][5]))
            login_dob_label.place(x=10, y=100)

            login_age_label = Label(prompt_window, text="Age:\t\t {}".format(user_info_get[0][6]))
            login_age_label.place(x=10, y=120)

            login_num_label = Label(prompt_window, text="Mobile number:\t {}".format(user_info_get[0][7]))
            login_num_label.place(x=10, y=140)

            login_pass_label = Label(prompt_window, text="Password:\t {}".format(user_info_get[0][8]))
            login_pass_label.place(x=10, y=160)

            exit_button1 = Button(prompt_window, text="Logout", padx=20, pady=5, bd=3, command=prompt_window.destroy)
            exit_button1.place(x=270, y=260)

        else:
            incorrect_label = Label(root, text="Incorrect Password")
            incorrect_label.place(x=140, y=200)

    except:
        incorrect_label = Label(root, text="Email address not registered. Please signup to access.")
        incorrect_label.place(x=60, y=200)



# show password (login screen)
def tick():
    global psswd, var
    val = psswd.get()
    psswd.delete(0, END)
    # shows password if onvalue is show or otherwise its hidden
    if var.get() == 'show':
        psswd.configure(show="")
        psswd.insert(0, val)
    else:
        psswd.configure(show="*")
        psswd.insert(0, val)


# Screen Label
screen_label = Label(root, text="WELCOME...", font=("Helvitica", 20))
screen_label.place(x=110, y=40)

# Credential entry box
user = Entry(root, width=30, borderwidth=3)
user.place(x=100, y=100)

psswd = Entry(root, show="*", width=30, borderwidth=3)
psswd.place(x=100, y=130)


var = StringVar()
# checkbutton for show password
show_clickbutton = Checkbutton(root, text="Show password", variable=var, onvalue="show", offvalue="hide", command=tick)
show_clickbutton.deselect()
show_clickbutton.place(x=290, y=130)

# Credential label
user_label = Label(root, text="Email")
user_label.place(x=60, y=100)

psswd_label = Label(root, text="Password")
psswd_label.place(x=40, y=130)

incorrect_label = Label(root, text="Fill the required field before login.")
incorrect_label.place(x=100, y=200)
# Login Button
login_button = Button(root, text="Login", bd=3, padx=20, command=login)
login_button.place(x=150, y=160)

# Signup Button
signup_button = Button(root, text="Signup", bd=3, padx=20, command=signup)
signup_button.place(x=320, y=260)

# signup label
signup_label = Label(root, text="If you don't have account please signup.")
signup_label.place(x=70, y=265)


root.mainloop()