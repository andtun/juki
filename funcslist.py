# This Python file uses the following encoding: utf-8

import os
import bottle
import requests
import xlrd
import beaker.middleware
from openpyxl import load_workbook
from passlib.hash import pbkdf2_sha256
from bottle import *
#from socket import gethostname, gethostbyname

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
    #'session.validate_key': True,
    #'session.secure': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


#------DICS FOR AUTH-------------------------------------------------------#

def hsh(password): #hashing pwd
    return pbkdf2_sha256.hash(password, rounds=HRN)


#--------------------------------------------------------------------------


#function returns True if login and pwd match
def check_login(username, password):
    if UserDB.check(username):
        return pbkdf2_sha256.verify(password, UserDB.get(username).pw)
    return False

#request.session['logged_in'] = False



#===============DECORATORS&FUNCTIONS====================#

def need_auth(webpage):   #see how it works in the code down
    def wrapper():
        #request.session = request.environ['beaker.session']        
        if 'username' in request.session:
            #print("logged in !!!!!!!!")            
            if request.session['username'] != "":
                return webpage()
            
        redirect("/")

    return wrapper


def access_is(access_level):   #used to check the access level
    ans = (access_level == UserDB.get(request.session['username']).access_level)
    return ans


def stat_file(filename):   #an easier way to return static file
    return static_file(filename, root = STAT_FILE_ROOT)


def logout():
    request.session['username'] = ""
    response.set_cookie("failed_login", 'undefined')



#=======================FORM METHODS==========================#    


def find_cell(fio, month, date):        #find a cell
    
               #setting up table    
    workbook = xlrd.open_workbook('export.xlsx')
    sheet = workbook.sheet_by_index(0)
    curcol = 1
    currow = 1

               #finding fio
    for i in range(sheet.nrows):
        data = sheet.cell_value(i, 0)
        if data == fio.decode('utf-8'):
            currow = i
            break

                #finding month
    for i in range(sheet.ncols):
        data = sheet.cell_value(0, i)
        if data == month.decode("utf-8"):
            curcol = i
            break

                #finding date
    curcol += int(date)

                #ending work
    book=load_workbook('export.xlsx')
    sheet = book.active
    currow += 1

    #return the cell we need and the table object, in which the cell is
    return currow, curcol, book, sheet



def do_calendar_form():     #filling the table using form (manual)

    
    def cal(calendar_str):  #turns yyyy-mm-dd  into  'monthname' and date
        indx = calendar_str.find('.')
        day = calendar_str[:indx]
        calendar_str = calendar_str[(indx+1):]
        indx = calendar_str.find('.')
        monthnum = calendar_str[:indx]
        
        month = {'01': "январь", '02': "февраль", '03': "март", '04': "апрель", '05': "май", '06': "июнь", '07': "июль",
             '08': "август", '09': "сентябрь", '10': "октябрь", '11': "ноябрь", '12': "декабрь"}
        
        return day, month[monthnum]



           #getting info from the form
    data = request.body.read()
    cut = data.find("|")
    fio = data[:cut]
    data = data[cut+1:]
    cut = data.find("|")
    cal_str = data[:cut]
    YesNo = data[cut+1:]
    print(fio, cal_str, YesNo)
    
           #formatting info
    date, month = cal(cal_str)

            #finding the cell
    currow, curcol, book, sheet = find_cell(fio, month, date)


            #deciding what to insert into the cell
    if YesNo == 'Yes':
        sheet.cell(row=currow, column=curcol).value = ""
    else:
        sheet.cell(row=currow, column=curcol).value = "X"
    book.save('export.xlsx')

            #returning success page
    return stat_file("back.html")



def do_calendar_from_db(name, month, date):   #filling the table using DB (automatic)
    currow, curcol = find_cell(name, month, date)
    data = sheet.cell_value(currow, curcol)
    
    if data != X:  #if data is X, don't change the cell. If not X - the student is in school, so set the cell empty
        sheet.cell(row=currow, column=curcol).value = ""


#======================================USERDB HERE=================================================
#==============================================================================================

import sqlite3
#from passlib.hash import pbkdf2_sha256


class DataBase:
    name = 'UserList.db'

    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = sqlite3.connect(self.name)
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        self._db_cur.execute(query)
        self._db_connection.commit()
        return

    def fetch(self, query):
        return self._db_cur.execute(query).fetchall()

    def save(self):
        self._db_connection.commit()

    def __del__(self):
        self._db_connection.close()

#------------------------------------------------------------


def add(username, pw, fio, access_level):
    cmnd = "INSERT INTO Userlist VALUES ('%s','%s','%s','%s');" % (username, pw, fio, access_level)
    db.query(cmnd)


def check(username):        # True if user exists, False if doesn't
    cmnd = "SELECT pw FROM Userlist WHERE username='%s';" % username
    reslt = db.fetch(cmnd)
    if reslt:
        return True
    return False


def get(username):
    d =  {}
    for i in ['username', 'pw', 'fio', 'access_level']:
        cmnd = "SELECT %s FROM Userlist WHERE username='%s';" % (i, username)
        t = str(db.fetch(cmnd))
        d[i] = t[3:len(t)-4]
    reslt = User(d['username'], d['access_level'], d['fio'], d['pw'])
    return reslt

# =============================================================

class User:
    username = ""
    access_level = ""
    fio = ""
    pw = ""

    def __init__(self, username, access_level, fio, pw):
        self.username = username
        self.access_level = access_level
        self.fio = fio
        self.pw = pw

# ==============================================================

db = DataBase()

"""cmnd = '''CREATE TABLE UserList (
username text, pw text,
fio text, access_level text);'''
db.query(cmnd)

add('user1', hsh('qwerty'), 'Петров И. И.', '10kl')
add('usertest', hsh('123'), 'Иванов А. А.', '10kl')
add('sgibnev', hsh('aisgi'), 'Сгибнев А. И.', '10kl')
add('anikina', hsh('eaani'), 'Аникина Е. А.', '10kl')
add('zapolsky', hsh('iazap'), 'Запольский И. А.', '10kl')
add('tiunova', hsh('mvtiu'), 'Тиунова М. В.', '10kl')
add ('admin', hsh('adminpsw'), 'Администратор', 'admin')"""
