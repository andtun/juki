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
    def cal(calendar_str):
      indx = calendar_str.find('-')
      calendar_str = calendar_str[(indx+1):]
      indx = calendar_str.find('-')
      month = calendar_str[:indx]
      calendar_str = calendar_str[(indx+1):]
      date = calendar_str
      d={}
      d['01'] = "январь".decode('utf-8')
      d['02'] = "февраль".decode('utf-8')
      d['03'] = "март".decode('utf-8')
      d['04'] = "апрель".decode('utf-8')
      d['05'] = "май".decode('utf-8')
      d['06'] = "июнь".decode('utf-8')
      d['07'] = "июль".decode('utf-8')
      d['08'] = "август".decode('utf-8')
      d['09'] = "сентябрь".decode('utf-8')
      d['10'] = "октябрь".decode('utf-8')
      d['11'] = "ноябрь".decode('utf-8')
      d['12'] = "декабрь".decode('utf-8')
      ans={}
      ans['data'] = date
      ans['month'] = month
      return ans

    
    fio=request.forms.get('fio')
    cal_str=request.forms.get('calendar')
    YesNo=request.forms.get('YesNo')


    date = cal(cal_str)['data']
    month = cal(cal_str)['month']

    
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
