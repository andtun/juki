import os
from bottle import run, request, get, post, route, static_file, template
import requests
import xlrd
from openpyxl import load_workbook

@route("/")
def index():
  return static_file("login.html", root='static/static/alco/')

@route("/alco")
def get_stat():
  return static_file("path.html", root='static/static/alco/')

@route("/submit", method="POST")
def do_form():
    fio=request.forms.get('fio')
    month=request.forms.get('month')
    date=request.forms.get('day')
    YesNo=request.forms.get('YesNo')
    
    workbook = xlrd.open_workbook('export.xlsx')
    sheet = workbook.sheet_by_index(0)
    curcol = 1    
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
    sheet.cell(row=currow, column=curcol).value = "X"
    book.save('export.xlsx')
    return static_file("back.html", root='static/alco/')

@route("/fileDownload")
def download():
    return static_file("export.xlsx", root='.', download=True)
    
run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
