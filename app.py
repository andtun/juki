# This Python file uses the following encoding: utf-8

import os
import bottle
from bottle import *
import requests
import xlrd
from openpyxl import load_workbook
import beaker.middleware
#from passlib.hash import pbkdf2_sha256


bottle.debug(True)

randomkey = '''8RCURFLxYpQvehdTSe2I
K76Kl6d5V1A9MGaGggni
cfEjHrIG9tHHvkEeddkM
zvXYeN1tmK9PKRvwb8V5
cquNfumzsM5qEhkNEXsM'''

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
    'session.cookie_expires': True,
    'session.encrypt_key': randomkey,
    'session.valiate_key': 'JUKI',
    'session.timeout': 1800,  # 1/2 hour
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.secure': True,
    

}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


d = {}
access = {}
d['user1'] = "qwerty"
access['user1'] = "10kl"
d['admin'] = "adminpsw"
access['admin'] = "admin"


def check_login(username, password):
    if username in d:
        if d[username] == password:
            return True
    return False

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

#request.session['logged_in'] = False

    
@get("/")
def login():
    if 'logged_in' in request.session:
        if request.session['logged_in']:
            redirect("/main")
    return static_file("login.html", root='static/static/alco/')

@post("/")
def chklgn():
    username = request.forms.get('username')
    password = request.forms.get('password')
    request.session['logged_in'] = check_login(username, password)
    if request.session['logged_in']:
        request.session['access'] = access[username]
        request.session['username'] = username
        redirect("/main")
    else:
        redirect("/logerror")

@get("/logerror")
def logerror():
    return static_file("login-notlogged.html", root='static/static/alco/')


@route("/main")
def main():
    if 'logged_in' in request.session:
        if request.session['logged_in']:
            if request.session['access'] == "10kl":
                return static_file("path.html", root='static/static/alco/')
            elif request.session['access'] == "admin":
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

    if request.session['logged_in']:

    
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
        if request.session['logged_in']:
            return static_file("back.html", root='static/static/alco/')
    return HTTPError(401)


@route("/fileDownload")
def download():
    if request.session['logged_in']:
        return static_file("export.xlsx", root='.', download=True)

@get("/logout")
def lout():
    request.session['access'] = ""
    request.session['logged_in'] = False
    #redirect ("/")
    redirect("/main")

@route("/forgot_password")
def forgot():
    return '''Если забыли пароль, напишите <a href="http://vk.com/easytofindme">администратору сайта.</a>'''

@get("/change_password")
def chngpswhtml():
    if 'logged_in' in request.session:
        if request.session['logged_in']:
            return static_file("change_pswd.html", root='static/static/alco/')
    return HTTPError(401)

@post("/change_password")
def chngpswprocess():
    if request.session['logged_in']:
        its_username = request.session['username']
        old_password = request.forms.get('old_password')
        new_password = request.forms.get('new_password')
        new_password_conf = request.forms.get('new_password_repeated')
        if new_password != new_password_conf:
            return '''Пароли не совпадают. <a href="/change_password">Повторить.</a>'''
        global d
    if ((its_username in d) and (d[its_username] == old_password)):
        d[its_username] = new_password
        request.session['logged_in'] = False
        return '''Пароль изменён. Нажмите <a href="/logout">здесь</a>, чтобы войти заново'''
    return '''Вы что-то ввели не так:( <a href="/change_password">Попробуйте снова</a> '''

@get("/check_user")
def chk_usr():
    return request.session['username']

#======================================================================
#                     ADMIN STUFF

@route("/showuserlist")
def showusr():
    if (request.session['logged_in'] and (request.session['access'] == "admin")):
        return(str(d), str(access))
    return HTTPError(401)

@route("/userlistdownload")
def downloadusr():
    if (request.session['logged_in'] and (request.session['access'] == "admin")):
        print("started")
        ulist = open('usrlist.txt', 'w')
        ulist.writelines(str(d))
        ulist = open('usrlist.txt', 'a')
        ulist.write(str(access))
        ulist.close()
        return static_file("usrlist.txt", root='.', download=True)
    return HTTPError(401)

@route("/delete_user")
def delusr():
    if (request.session['logged_in'] and (request.session['access'] == "admin")):
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
    global d
    global access
    if (request.session['logged_in'] and (request.session['access'] == "admin")):
        his_username = request.forms.get('username')
        his_password = request.forms.get('password')
        his_access_level = request.forms.get('access_level')
        if his_username in d:
            return "User already exists"
        d[his_username] = his_password
        access[his_username] = his_access_level
        return ("created user: username="+his_username+", password="+his_password+", access_level="+his_access_level)
    return HTTPError(401)

@post("/change_access")
def chngaccs():
    global d
    global access
    if (request.session['logged_in'] and (request.session['access'] == "admin")):
        his_username = request.forms.get('username')
        new_access_level = request.forms.get('access_level')
        if his_username in d:
            access[his_username] = new_access_level
            return ("Access level for "+his_username+" changed to "+ new_access_level)
        return "No such user"
        
    return HTTPError(401)




#======================================================================


@bottle.error(500)
def ff(error):
    return static_file("err500page.html", root='static/static/alco/')

@bottle.error(404)
def notfound(error):
    return('''Страница не найдена. <a href="/main">Выйти на главную.</a> ''')

@bottle.error(401)
def fff(error):
    return static_file("notloggederror.html", root='static/static/alco/')

bottle.run(app=app, host="0.0.0.0", port=os.environ.get('PORT', 5000), quiet=False)

