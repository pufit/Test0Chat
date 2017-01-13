import cgi
import cgitb
import html
import http.cookies
import os
import sys
import codecs
import smtplib
import random
import time
import json
from _wall import Wall
wall= Wall()

if wall.check_ban(cgi.escape(os.environ["REMOTE_ADDR"]))==True: #Проверяем ip в бан листе
    ban='<a>Ваш ip добавлен в чёрный список<a>'
    user = None
else: #Находим пользователя по куки
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    session = cookie.get("session")
    if session is not None:
        session = session.value
    user = wall.find_cookie(session)
status = wall.get_status(user)[3]

storage = cgi.FieldStorage()
delete = storage.getvalue('delete')
delete = delete.split('-')

if int(status)==9:
    with open('cgi-bin/bd/wall.json', 'r', encoding='utf-8') as f:
        wall = json.load(f)
    for i in range(len(wall["posts"])):
        if (delete[0] == wall["posts"][i]['user']) and(delete[1] == wall["posts"][i]['time']):
            wall["posts"].pop(i)
            break
    with open('cgi-bin/bd/wall.json', 'w', encoding='utf-8') as f:
        wall = json.dump(wall, f)
