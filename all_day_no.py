# This Python file uses the following encoding: utf-8

import xlrd
from openpyxl import load_workbook
#import warnings
from datetime import datetime
from insertPoint import convert
from datetime import datetime

def allNo():
    d = str(datetime.now())
    d = d[:d.find(" ")]
    d = d.split("-")
    month = convert(d[1])
    date = int(d[2])

    workbook = xlrd.open_workbook('export.xlsx')
    sheet = workbook.sheet_by_index(0)

    for i in range(sheet.ncols):
        data = sheet.cell_value(0, i)
        if data == month.decode("utf-8"):
            break

    curcol = i + date

    for i in range(3, sheet.nrows + 1):
        book = load_workbook('export.xlsx')
        sheet = book.active
        sheet.cell(row=i, column=curcol).value = "H"
        book.save('export.xlsx')


print('start')
allNo()
print('end')
