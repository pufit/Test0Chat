#!c:\Python34\python.exe

import cgi
import html
import http.cookies
import os
import json
from _wall import Wall
wall= Wall()

if wall.check_ban(html.escape(os.environ["REMOTE_ADDR"]))==True: #Проверяем ip в бан листе
    ban='<a>Ваш ip добавлен в чёрный список<a>'
    user = None
#Находим пользователя по куки
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)
status = wall.get_status(user)[3]

storage = cgi.FieldStorage()
delete = storage.getvalue('delete', '')
delete = delete.split('-')

wall.del_message(delete, status)

print('Content-type: text/html\n')
print(delete)
