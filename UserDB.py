# This Python file uses the following encoding: utf-8

import sqlite3
#from funcslist import hsh
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
        d[i] = t[4:len(t)-4]
    reslt = User(d['username'], d['access_level'], d['fio'], d['pw'])
    return reslt

def set(username, column, value):
    cmnd = "UPDATE Userlist SET %s=%s WHERE username = '%s';" % (column, value, username)
    db.query(cmnd)

def delete(username):
    cmnd = "DELETE FROM Userlist WHERE username = '%s';" % username
    db.query(cmnd)


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

#print(get('tiunova').fio)