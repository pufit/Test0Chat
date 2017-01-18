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
ban = storage.getvalue('ban')
ban = ban.split('_')
if int(status)==9:
    with open('cgi-bin/bd/ip.json', 'r', encoding='utf-8') as f:
        ips = json.load(f)
    for i in ips:
        if i == ban[0]:
            with open('cgi-bin/bd/ban-list.json', 'r', encoding='utf-8') as f:
                bans = json.load(f)
            bans['bans'].append(ips[i])
            with open('cgi-bin/bd/ban-list.json', 'w', encoding='utf-8') as f:
                json.dump(bans,f)
            break
    with open('cgi-bin/bd/cookies.json', 'r', encoding='utf-8') as f:
        cookie = json.load(f)
    for i in cookie:
        if cookie[i]==ban[0]:
            cookie[i]=None
    with open('cgi-bin/bd/cookies.json', 'w', encoding='utf-8') as f:
        json.dump(cookie, f)
print('Status: 200 OK')

        
