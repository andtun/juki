import xlrd
from openpyxl import load_workbook
import warnings

# name = 'Бешкуров Михаил Борисович'
# month = 'сентябрь'
# date = 10


def addPoint(name, month, date):
    workbook = xlrd.open_workbook('export.xlsx')
    sheet = workbook.sheet_by_index(0)
    curcol = 1
    currow = 1
    for i in range(sheet.nrows):
        data = sheet.cell_value(i, 0)
        if data == name:
            currow = i
            break
    for i in range(sheet.ncols):
        data = sheet.cell_value(0, i)
        if data == month:
            curcol = i
            break
    for i in range(curcol, sheet.ncols - curcol):
        data = sheet.cell_value(1, i)
        if data == int(date):
            curcol = i
            break
    book = load_workbook('export.xlsx')
    sheet = book.active
    currow += 1
    curcol += 1
    sheet.cell(row=currow, column=curcol).value = "X"
    book.save('export.xlsx')


def convert(month_number):
    month = {'01': "январь", '02': "февраль", '03': "март", '04': "апрель", '05': "май", '06': "июнь", '07': "июль",
             '08': "август", '09': "сентябрь", '10': "октябрь", '11': "ноябрь", '12': "декабрь"}
    return month[month_number]

