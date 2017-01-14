# This Python file uses the following encoding: utf-8

import os
from bottle import *
import requests
import xlrd
from openpyxl import load_workbook

d = {}
d['user1'] = "qwerty"
d['user100500'] = "aswq"
d['admin'] = "adminpsw228"

global logged_in
logged_in = False

def check_pass():
    username = request.forms.get('username')
    password = request.forms.get('password')
    '''print(username)
    print(password)'''
    if username in d:
        if d[username] == password:
            return True
    return False
        
def logout():
    global logged_in
    logged_in = False
    
@get("/")
def login():
    if logged_in:
        redirect("/main")
    reason = request.query.reason
    if reason == "notlogged":
        return static_file("login-notlogged.html", root='static/static/alco/')
    return static_file("login.html", root='static/static/alco/')

@post("/")
def chklgn():
    if check_pass():
        global logged_in
        logged_in = True
        redirect("/main")
    else:
        redirect('''/?reason="notlogged"''')


@route("/main")
def main():
    global logged_in
    if logged_in:
        return static_file("path.html", root='static/static/alco/')
    return HTTPError(401)


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
        return static_file("back.html", root='static/static/alco/')
    return HTTPError(401)

@route("/fileDownload")
def download():
    return static_file("export.xlsx", root='.', download=True)

@get("/logout")
def lout():
    logout()
    redirect("/")


@error(401)
def notlogged(error):
    redirect("/")
    
    
run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
