# This Python file uses the following encoding: utf-8

import xlrd
from openpyxl import load_workbook
import warnings
import funcslist

# name = 'Бешкуров Михаил Борисович'
# month = 'сентябрь'
# date = 10


list1 = ["Алеев Мурат Дмитриевич", "Алексеев Илья Сергеевич", "Архипова Анастасия Станиславовна",
         "Балакшина Мария Евгеньевна", "Барциц Никита Теймуразович", "Бешкуров Михаил Борисович",
         "Бешкуров Тимофей Борисович", "Блынская София Владимировна", "Богдан Дарья Александровна",
         "Браздникова Ульяна Викторовна", "Букин Андрей Владимирович", "Волков Георгий Васильевич",
         "Григорян Виктория Рубеновна", "Губанова Полина Сергеевна", "Данилов Руслан Игоревич",
         "Деева Александра Андреевна", "Евдокимова Наталья Николаевна", "Жуковская Кира Леонидовна",
         "Иевлева Валерия Андреевна", "Капкова Мария Александровна", "Каргинова Анна Евгеньевна",
         "Кин Александр Алексеевич", "Козлова Мария Сергеевна", "Косарева Олеся Алексеевна",
         "Кубрак Катерина Вадимовна", "Левин Ефим Михайлович", "Ли Тимофей Александрович",
         "Мазурова Варвара Владимировна", "Печникова Галина Сергеевна", "Пужаев Илия Юрьевич", "Разин Денис Валерьевич",
         "Ракитина Наталия Андреевна", "Рудый Всеволод Вадимович", "Святловская София Владимировна",
         "Смолярова Юлия Дмитриевна", "Сокова Анастасия Алексеевна", "Солопова Елена Валерьевна",
         "Сонькин Михаил Викторович", "Спасенкова Арина Владимировна", "Стрелкова Марья Михайловна",
         "Титкова Александра Сергеевна", "Тиунова Ольга Никитична", "Тюняткин Андрей Александрович",
         "Уманский Вениамин Алексеевич", "Халитова Эльмира Тимуровна", "Хаханова Маргарита Сергеевна",
         "Чернышев Артём Кириллович", "Шашкин Иван Александрович", "Шерстнева Мария Ивановна",
         "Элиович Алиса Александровна"]

list2 = ['Алеев Мурат', 'Алексеев Илья', 'Архипова Анастасия', 'Балакшина Мария', 'Барциц Никита', 'Бешкуров Михаил',
         'Бешкуров Тимофей', 'Блынская София', 'Богдан Дарья', 'Браздникова Ульяна', 'Букин Андрей', 'Волков Георгий',
         'Григорян Виктория', 'Губанова Полина', 'Данилов Руслан', 'Деева Александра', 'Евдокимова Наталья',
         'Жуковская Кира', 'Иевлева Валерия', 'Капкова Мария', 'Каргинова Анна', 'Кин Александр', 'Козлова Мария',
         'Косарева Олеся', 'Кубрак Катерина', 'Левин Ефим', 'Ли Тимофей', 'Мазурова Варвара', 'Печникова Галина',
         'Пужаев Илиа', 'Разин Денис', 'Ракитина Наталия', 'Рудый Всеволод', 'Светловская София', 'Смолярова Юлия',
         'Сокова Анастасия', 'Солопова Елена', 'Сонькин Михаил', 'Спасенкова Арина', 'Стрелкова Марья',
         'Титкова Александра', 'Тиунова Ольга', 'Тюняткин Андрей', 'Уманский Вениамин', 'Халитова Эльмира',
         'Хаханова Маргарита', 'Чернышев Артем', 'Шашкин Иван', 'Шерстнева Мария', 'Элиович Алиса']


def rdname(name):
    print(name)
    name = name.decode('utf8')
    print(name)
    for item in list2:
        if name==item:
            print(name, item)
            
    # ans = list1[list2.index(name)]
    return ans


def addPoint(name, month, date):

    currow, curcol, book, sheet = funcslist.find_cell(name, month, date)
    print(currow, curcol)
    sheet.cell(row=currow, column=curcol).value = "thru INSERTPOINT"
    book.save('export.xlsx')


def convert(month_number):
    month = {'01': "январь", '02': "февраль", '03': "март", '04': "апрель", '05': "май", '06': "июнь", '07': "июль",
             '08': "август", '09': "сентябрь", '10': "октябрь", '11': "ноябрь", '12': "декабрь"}
    return month[month_number]

