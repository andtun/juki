# This Python file uses the following encoding: utf-8

#import time
import os
import bottle
import requests
import xlrd
import beaker.middleware
import json
from bottle import *
from funcslist import *
from passlib.hash import pbkdf2_sha256
from openpyxl import load_workbook



@hook('before_request')
def setup_request():
    #time.sleep(0.159)
    request.session = request.environ['beaker.session']
    #request.session.save()

    
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
    
    redirect('/main')


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
    return do_calendar_form()
#--------------------------------------------------------------------

@route("/fileDownload")
@need_auth
def download():
    return static_file("export.xlsx", root='.', download=True)


@get("/logout")
def lout():
    logout()
    
    #redirect ("/")
    redirect("/main?1")


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
@need_auth
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
        new_email = request.forms.get('new_mail')
        
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


@get("/syncdics")
@need_auth
def syncalldics():
    syncdics()


@post("/post_info")
def postinfo():
    if schoolserver():
        new_events = json.loads(str(request.forms.get('new_events_json')))
        print(new_events['a'])



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

@route("/stylechangepassword.css")
def st():
    return stat_file("stylechangepassword.css")

@route("/smtwrpswd.css")
def smth():
    return stat_file("smtwrpswd.css")

@route("/background2-min.png")
def pencil():
    return stat_file("background2-min.png")

@route("/download.png")
def dencil():
    return stat_file("download.png")

@route("/downl.png")
def dencil():
    return stat_file("downl.png")

@route("/edit.png")
def return_img():
    return stat_file("edit.png")

@route("/lock.png")
def return_img():
    return stat_file("lock.png")

@route("/lock1.png")
def return_img():
    return stat_file("lock1.png")

@route("/Pencil.png")
def return_img():
    return stat_file("Pencil.png")

@route("/login.png")
def return_img():
    return stat_file("login.png")

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

