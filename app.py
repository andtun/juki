# This Python file uses the following encoding: utf-8

import os
from bottle import *
import requests
import xlrd
from openpyxl import load_workbook

d = {}
access = {}
d['user1'] = "qwerty"
access['user1'] = "10kl"
d['admin'] = "adminpsw228"
access['admin'] = "admin"

global access_level
global logged_in
logged_in = False

def check_pass():
    username = request.forms.get('username')
    password = request.forms.get('password')
    global access_level
    '''print(username)
    print(password)'''
    if username in d:
        if d[username] == password:
            access_level = access[username]
            return True
    return False
        
def logout():
    global logged_in
    logged_in = False
    print(logged_in)
    
@get("/")
def login():
    global logged_in
    if logged_in:
        redirect("/main")
    return static_file("login.html", root='static/static/alco/')

@post("/")
def chklgn():
    if check_pass():
        global logged_in
        logged_in = True
        redirect("/main")
    else:
        redirect("/logerror")

@get("/logerror")
def logerror():
    return static_file("login-notlogged.html", root='static/static/alco/')


@route("/main")
def main():
    global logged_in
    global access_level
    if logged_in:
        if access_level == "10kl":
            return static_file("path.html", root='static/static/alco/')
        elif access_level == "admin":
            return static_file("admin_page.html", root='static/static/alco/')
        else:
            return "nolevel"
    redirect("/")


@route("/submit", method="POST")
def do_form():
    def cal(calendar_str):
      indx = calendar_str.find('-')
      calendar_str = calendar_str[(indx+1):]
      indx = calendar_str.find('-')
      month = calendar_str[:indx]
      calendar_str = calendar_str[(indx+1):]
      date = calendar_str
      d={}
      d['01'] = "январь"
      d['02'] = "февраль"
      d['03'] = "март"
      d['04'] = "апрель"
      d['05'] = "май"
      d['06'] = "июнь"
      d['07'] = "июль"
      d['08'] = "август"
      d['09'] = "сентябрь"
      d['10'] = "октябрь"
      d['11'] = "ноябрь"
      d['12'] = "декабрь"
      ans={}
      ans['data'] = date
      ans['month'] = month
      return ans

    global logged_in
    if logged_in:

    
        fio=request.forms.get('FIO')
        cal_str=request.forms.get('calendar')
        YesNo=request.forms.get('YesNo')


        date = cal(cal_str)['data']
        month = cal(cal_str)['month']

        
        workbook = xlrd.open_workbook('export.xlsx')
        sheet = workbook.sheet_by_index(0)
        curcol = 1
        currow = 1
        for i in range(sheet.nrows):
            data = sheet.cell_value(i, 0)
            if data == fio.decode("utf-8"):
                currow = i
                break
        for i in range(sheet.ncols):
            data = sheet.cell_value(0, i)
            if data == month.decode("utf-8"):
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
        if YesNo == "Yes":
            sheet.cell(row=currow, column=curcol).value = ""
        else:
            if YesNo == "No":
                sheet.cell(row=currow, column=curcol).value = "Н"
        book.save('export.xlsx')
        if logged_in:
            return static_file("back.html", root='static/static/alco/')
    return HTTPError(401)
    redirect("/")

@route("/fileDownload")
def download():
    return static_file("export.xlsx", root='.', download=True)

@get("/logout")
def lout():
    logout()
    redirect("/")

@route("/forgot_password")
def forgot():
    return "Если забыли пароль, напишите администратору: ..."

@get("/change_password")
def chngpswhtml():
    global logged_in
    if logged_in:
        return static_file("change_pswd.html", root='static/static/alco/')
    return HTTPError(401)

@post("/change_password")
def chngpswprocess():
    global logged_in
    if logged_in:
        username = request.forms.get('username')
        old_password = request.forms.get('old_password')
        new_password = request.forms.get('new_password')
        global d
        if ((username in d) and (d[username] == old_password)):
            d[username] = new_password
            logged_in = False
            return '''Пароль изменён. Нажмите <a href="http://jukiproject.herokuapp.com/logout">Скачать список пользователей</a>, чтобы войти заново'''
        return '''Вы что-то ввели не так:(<a href="http://jukiproject.herokuapp.com/change_password">Попробуйте снова</a> '''
    return HTTPError(401)

#======================================================================
#                     ADMIN STUFF

@route("/showuserlist")
def showusr():
    global logged_in
    global access_level
    if (logged_in and (access_level=="admin")):
        return(str(d), str(access))
    return HTTPError(401)

@route("/userlistdownload")
def downloadusr():
    global logged_in
    global access_level
    if (logged_in and (access_level=="admin")):
        print("started")
        ulist = open('usrlist.txt', 'w')
        print(str(d), file=ulist)
        ulist = open('usrlist.txt', 'a')
        print(str(access), file=ulist)
        ulist.close()
        return static_file("usrlist.txt", root='.', download=True)
    return HTTPError(401)

@route("/delete_user")
def delusr():
    global logged_in
    global access_level
    if (logged_in and (access_level=="admin")):
        global d
        global access
        username = str(request.query.username)
        if username in d:
            del d[username]
            del access[username]
            return ("User "+username+" deleted!")
        else:
            return "No such user"
    return HTTPError(401)

@post("/add_user")
def addusr():
    global logged_in
    global access_level
    global d
    global access
    if (logged_in and (access_level=="admin")):
        username = request.forms.get('username')
        password = request.forms.get('password')
        access_level = request.forms.get('acess_level')
        if username in d:
            return "User already exists"
        d[username] = password
        access[username] = access_level
        return ("created user: username="+username+", password="+password+", access_level="+access_level)
    return HTTPError(401)

@post("/change_access")
def chngaccs():
    global logged_in
    global access_level
    global d
    global access
    if (logged_in and (access_level=="admin")):
        username = request.forms.get('username')
        new_access_level = request.forms.get('acess_level')
        if username in d:
            access[username] = new_access_level
            return ("Access level for "+username+" changed to "+ new_access_level)
        return "No such user"
        
    return HTTPError(401)




#======================================================================


@error(401)
def notlogged(error):
    return static_file("notloggederror.html",root='static/static/alco/') 
    
    
run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
