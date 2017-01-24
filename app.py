# This Python file uses the following encoding: utf-8

import os
import bottle
from bottle import *
import requests
import xlrd
from openpyxl import load_workbook
import beaker.middleware
from passlib.hash import pbkdf2_sha256
import time


#================DECLARING CONSTANTS (NAMES USE ONLY CAPS)=================#

#session encryption key
RANDOMKEY = '''8RCURFLxYpQvehdTSe2I
K76Kl6d5V1A9MGaGggni
cfEjHrIG9tHHvkEeddkM
zvXYeN1tmK9PKRvwb8V5
cquNfumzsM5qEhkNEXsM'''


#encryption validate key
VALIDATEKEY = 'JUKI'


#cookie lifetime, seconds
CTIME = 1800 # 1/2 hour


#hashing round number (how many times we apply hash algorythm)
HRN = 20000


#static file root directory
STAT_FILE_ROOT = 'static/static/alco/'



#=======================DESCRIBING STUFF=========================#

#bottle.debug(True)


session_opts = {
    'session.type': 'cookie',
    'session.data_dir': './session/',
    'session.auto': True,
    'session.cookie_expires': True,
    'session.encrypt_key': RANDOMKEY,
    'session.validate_key': VALIDATEKEY,
    'session.timeout': CTIME,
    #'session.type': 'cookie',
    #'session.type': 'file',
    'session.validate_key': True,
    'session.secure': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


#dics, where user info is stored
d = {}       #dic for username and password hashes: d[username] returns hash
access = {}  #dic for access levels
email = {}


d['user1'] = pbkdf2_sha256.hash("qwerty", rounds=HRN)
d['admin'] = pbkdf2_sha256.hash("adminpsw", rounds=HRN)
d['user_test'] = pbkdf2_sha256.hash("qwerty", rounds=HRN)

access['user1'] = "10kl"
access['admin'] = "admin"
access['user_test'] = "10kl"

email['user1'] = "email@example.com"
email['admin'] = "email@example.com"
email['user_test'] = "email@example.com"


#function returns True if login and pwd match
def check_login(username, password):
    if username in d:
        return pbkdf2_sha256.verify(password, d[username])
    return False


#maintaining session
@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


#request.session['logged_in'] = False


#===============DECORATORS&FUNCTIONS====================#

def need_auth(webpage):   #see how it works in the code down
    def wrapper():
        
        if 'logged_in' in request.session:
            
            if request.session['logged_in']:
                return webpage()
            
        redirect("/")
        #return 'adas'
    return wrapper


def access_is(access_level):   #used to check the access level
    ans = (access_level == request.session['access'])
    return ans


def stat_file(filename):   #an easier way to return static file
    return static_file(filename, root = STAT_FILE_ROOT)


def logout():
    request.session['access'] = ""
    request.session['username'] = ""
    request.session['logged_in'] = False


def syncdics():     # in case the server crashes, all dics will be stored in .txt files
    hash_file = open("hash_file.txt", 'a')
    access_file = open("access_file.txt", 'a')
    email_file = open("email_file.txt", 'a')

    curtime = time.asctime()

    hash_file.write('\n \n '+curtime+"   -----------------    ")
    access_file.write('\n \n '+curtime+"   -----------------    ")
    email_file.write('\n \n '+curtime+"   -----------------    ")

    hash_file.write(str(d))
    access_file.write(str(access))
    email_file.write(str(email))

    hash_file.close()
    access_file.close()
    email_file.close()


    
#=====================USER PAGES========================#
    
@get("/")   #login html
def login():
    if 'logged_in' in request.session:
        
        if request.session['logged_in']:
            redirect("/main")
            
    return stat_file("login.html")


@post("/")   #processing login info
def chklgn():
    username = request.forms.get('username')    #getting usrname & pw
    password = request.forms.get('password')
    
    request.session['logged_in'] = check_login(username, password)  #if pw and usrname match, 'logged_in' in cookie is set to True
    
    if request.session['logged_in']:    #if already in, you'll be redirected to the menu page
        request.session['access'] = access[username]
        request.session['username'] = username      #setting atributes of the cookie
        redirect("/menu")

    else:   # if password and login don't match
        redirect("/logerror")


@get("/menu")   # main page for the user
@need_auth      # need_auth decorator: if not authorized, you'll get 401 Error
def menu():
    if access_is('10kl'):
        return stat_file("menu.html")
    
    return ('menu unavailable for this user')


#!!!REQUEST.SESSION['USERNAME'] WILL RETURN THE USRNAME OF THE LOGGED IN USER!!!
        

@get("/logerror")   # if pw didn't match login
def logerror():
    return stat_file("login-notlogged.html")


@route("/main")   # main page
@need_auth
def main():
    
    if access_is('10kl'):   
        return stat_file("path.html")

    if access_is('admin'):
        return stat_file("admin_page.html")


#--------------------working with calendar-----------------------

@route("/submit", method="POST")
@need_auth
def do_form():

    
    def cal(calendar_str):  #turns yyyy-mm-dd  into  'monthname' and date
        indx = calendar_str.find('-')
        calendar_str = calendar_str[(indx+1):]
        indx = calendar_str.find('-')
        monthnum = calendar_str[:indx]
        calendar_str = calendar_str[(indx+1):]
        
        month = {'01': "январь", '02': "февраль", '03': "март", '04': "апрель", '05': "май", '06': "июнь", '07': "июль",
             '08': "август", '09': "сентябрь", '10': "октябрь", '11': "ноябрь", '12': "декабрь"}
        
        return calendar_str, month[monthnum]


           #getting info from the form 
    fio=request.forms.get('FIO')
    cal_str=request.forms.get('calendar')
    YesNo=request.forms.get('YesNo')
    
           #formatting info
    date, month = cal(cal_str)

        
    #print(fio, date, month, YesNo)

    
           #working with table    
    workbook = xlrd.open_workbook('export.xlsx')
    sheet = workbook.sheet_by_index(0)
    #curcol = 1
    
    for i in range(sheet.nrows):
        data = sheet.cell_value(i, 0)
        if data == fio.decode('utf-8'):
            currow = i
            break
        
    for i in range(sheet.ncols):
        data = sheet.cell_value(0, i)
        if data == month.decode('utf-8'):
            curcol = i
            break
        
    for i in range(curcol, sheet.ncols - curcol):
        data = sheet.cell_value(1, i)
        if data == int(date):
            curcol = i
            break

    book=load_workbook('export.xlsx')
    sheet = book.active
    currow += 1
    curcol += 1

            #deciding what to insert into the cell
    if YesNo == 'Yes':
        sheet.cell(row=currow, column=curcol).value = ""
    else:
        sheet.cell(row=currow, column=curcol).value = "H"
    book.save('export.xlsx')

            #returning success page
    return stat_file("back.html")


#--------------------------------------------------------------------

@route("/fileDownload")
@need_auth
def download():
    return static_file("export.xlsx", root='.', download=True)


@get("/logout")
def lout():
    logout()
    
    redirect ("/")
    #redirect("/main?1")


@route("/forgot_password")
def forgot():
    return '''Если забыли пароль, напишите <a href="http://vk.com/easytofindme">администратору сайта.</a>'''


@get("/change_password")    # change password html
@need_auth
def chngpsw_html():
    return stat_file("change_pswd.html")


@post("/change_password")   # processing the info from html, changing password
@need_auth
def chngpsw_process():
    
    its_username = request.session['username']
    old_password = request.forms.get('old_password')
    new_password = request.forms.get('new_password')
    new_password_conf = request.forms.get('new_password_repeated')
    
    if new_password != new_password_conf:
        return stat_file("fail_to_change_pwd.html")
    
    global d
    if ((its_username in d) and (pbkdf2_sha256.verify(old_password, d[its_username]))):   # if the username exists and the old password is correct
        
        d[its_username] = pbkdf2_sha256.hash(new_password, rounds=HRN)  # generate new pwd hash
        logout()
        
        return stat_file("pwd_changed.html")
    return stat_file("something_wrong_pwd.html")


@get("/check_user")
def chk_usr():
    return request.session['username']

#======================================================================
#                     ADMIN STUFF

@route("/showuserlist")
@need_auth
def showusr():
    if access_is('admin'):
        
        return(str(access))


@route("/userlistdownload")
@need_auth
def downloadusr():
    if access_is('admin'):
        
        ulist = open('usrlist.txt', 'w')
        ulist.writelines(str(access))
        ulist.close()
        
    return static_file("usrlist.txt", root='.', download=True)

@route("/delete_user")
@need_auth
def delusr():
    if access_is('admin'):
        
        global d
        global access
        username = str(request.query.username)  #username is the one we entered
        
        if username in d:   # deleting user
            del d[username]
            del access[username]
            syncdics()
            
        return ("User "+username+" deleted!")
    else:
        return "No such user"


@post("/add_user")
@need_auth
def addusr():
    global d
    global access
    global email
    if access_is('admin'):
        
        his_username = request.forms.get('username')    #getting info from the form
        his_password = request.forms.get('password')
        his_access_level = request.forms.get('access_level')
        his_email = request.forms.get('email')
        
        if his_username in d:
            return "User already exists"
        
        d[his_username] = pbkdf2_sha256.hash(his_password, rounds=HRN)  #generating password hash
        access[his_username] = his_access_level     #setting access
        email[his_username] = his_email
        syncdics()

        return ("created user: username="+his_username+", password="+his_password+", access_level="+his_access_level+", email="+his_email)


@post("/change_access")
@need_auth
def chngaccs():
    global d
    global access
    if access_is('admin'):
        
        his_username = request.forms.get('username')
        new_access_level = request.forms.get('access_level')
        
        if his_username in d:
            access[his_username] = new_access_level
            syncdics()
            return ("Access level for "+his_username+" changed to "+ new_access_level)

        return "No such user"

@post("/change_email")
@need_auth
def chngemail():
    global d
    global email
    if access_is('admin'):
        
        his_username = request.forms.get('username')
        new_email = request.forms.get('email')
        
        if his_username in d:
            email[his_username] = new_email
            syncdics()
            return ("Email for "+his_username+" changed to "+ new_email)

        return "No such user"


@get("/download")
@need_auth
def gt_accs():
    if access_is('admin'):
        load = str(request.query.load)
        
        if load == 'access':
            filename = 'access_file.txt'
            
        if load == 'email':
            filename = 'email_file.txt'
            
        if load == 'hash':
            filename = 'hash_file.txt'
            
        return static_file(filename, root='.', download = True)




#======================================================================
#                       STYLES & IMAGES

@route("/style.css")
def style():
    return stat_file("style.css")

@route("/style2.css")
def style2():
    return stat_file("style2.css")

@route("/style3.css")
def style3():
    return stat_file("style3.css")

@route("/style4.css")
def style3():
    return stat_file("style4.css")

@route("/Pencil.png")
def pencil():
    return stat_file("Pencil.png")

@route("/download.png")
def dencil():
    return stat_file("download.png")

@route("/test1.png")
def return_img():
    return stat_file("test1.png")



#======================================================================
#                        ERRORS CATCHING

@bottle.error(500)
def ff(error):
    return stat_file("err500page.html")

@bottle.error(404)
def notfound(error):
    return stat_file("404error.html")

@bottle.error(401)
def fff(error):
    redirect("/")

#========================================================================
#===========================RUN========RUN===============================

bottle.run(app=app, host="0.0.0.0", port=os.environ.get('PORT', 5000), quiet=False)

