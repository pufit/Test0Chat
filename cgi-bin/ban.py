#!c:\Python34\python.exe
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

if wall.check_ban(html.escape(os.environ["REMOTE_ADDR"]))==True: #Проверяем ip в бан листе
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
ban = storage.getvalue('ban')
ban = ban.split('-')
wall.get_ban(ban, status)
print('Content-type: text/html\n')
print("OK")


