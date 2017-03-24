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


def add(username, pw, fio, access_level, email):
    cmnd = "INSERT INTO Userlist VALUES ('%s','%s','%s','%s','%s');" % (username, pw, fio, access_level, email)
    db.query(cmnd)


def check(username):        # True if user exists, False if doesn't
    cmnd = "SELECT pw FROM Userlist WHERE username='%s';" % username
    reslt = db.fetch(cmnd)
    if reslt:
        return True
    return False


def get(username):
    d =  {}
    for i in ['username', 'pw', 'fio', 'access_level', 'email']:
        cmnd = "SELECT %s FROM Userlist WHERE username='%s';" % (i, username)
        t = str(db.fetch(cmnd))
        d[i] = t[4:len(t)-4]
    reslt = User(d['username'], d['access_level'], d['fio'], d['pw'], d['email'])
    return reslt

def set(username, column, value):
    cmnd = "UPDATE Userlist SET %s='%s' WHERE username = '%s';" % (column, value, username)
    db.query(cmnd)

def delete(username):
    cmnd = "DELETE FROM Userlist WHERE username = '%s';" % username
    db.query(cmnd)

import time

def new_restore(username, code):
    expires = int(time.time()) + 1800
    print("--------------------------------")
    print(username, expires)
    cmnd  ="INSERT INTO RestoreList VALUES ('%s', '%s', '%s');" % (username, code, expires)
    db.query(cmnd)

def get_restore_code(username):
    cmnd = "SELECT code FROM RestoreList WHERE username='%s';" % username
    return db.fetch(cmnd)

import time
def check_expire(code):     # True if still active, False if expired
    curtime = int(time.time())
    cmnd = "SELECT expires FROM RestoreList WHERE code='%s';" % code
    expire_time = str(db.fetch(cmnd))
    expire_time = int(expire_time[4:len(expire_time)-4])
    print("EXPIRE TIME IS!!!!")
    print(expire_time)
    ans = expire_time > curtime
    print("IS COOKIE EXPIRED &&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(ans)
    return ans

def check_code(username, code):
    return code==get_restore_code(username)

def check_link(code):
    print(code)
    print(db.fetch("SELECT * FROM RestoreList"))
    cmnd = "SELECT * FROM RestoreList WHERE code='%s';" % code
    result = db.fetch(cmnd)
    print(result)
    if result:
        if check_expire(code):
            return True
    return False

# =============================================================

class User:
    username = ""
    access_level = ""
    fio = ""
    pw = ""
    email = ""

    def __init__(self, username, access_level, fio, pw, email):
        self.username = username
        self.access_level = access_level
        self.fio = fio
        self.pw = pw
        self.email = email

# ==============================================================

db = DataBase()

"""cmnd = '''CREATE TABLE RestoreList (
username text, code text, expires text);'''
db.query(cmnd)
print(get('user1').email)"""

"""cmnd = '''CREATE TABLE UserList (
username text, pw text,
fio text, access_level text, email text);'''
db.query(cmnd)

add('user1', hsh('qwerty'), 'Петров И. И.', '10kl', 'andtun@yandex.ru')
add('usertest', hsh('123'), 'Иванов А. А.', '10kl', '')
add('sgibnev', hsh('aisgi'), 'Сгибнев А. И.', '10kl', '')
add('anikina', hsh('eaani'), 'Аникина Е. А.', '10kl', '')
add('zapolsky', hsh('iazap'), 'Запольский И. А.', '10kl', '')
add('tiunova', hsh('mvtiu'), 'Тиунова М. В.', '10kl', '')
add ('admin', hsh('adminpsw'), 'Администратор', 'admin', '')

#print(get('tiunova').fio)"""

print(db.fetch('select * from Userlist'))
