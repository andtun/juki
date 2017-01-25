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
    #'session.validate_key': True,
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


def do_calendar_form():

    
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

