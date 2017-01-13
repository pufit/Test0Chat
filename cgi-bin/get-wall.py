# -*- coding: utf-8  -*-

#Начну я пожалуй коментить. Говорящие название файла

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
wall1= Wall()

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
posts = ''
click = ''
pm=''
pm1=''
if wall1.check_ban(cgi.escape(os.environ["REMOTE_ADDR"]))==True: #Проверяем ip в бан листе
    ban='<a>Ваш ip добавлен в чёрный список<a>'
    user = None
else: #Находим пользователя по куки
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    session = cookie.get("session")
    if session is not None:
        session = session.value
    user1 = wall1.find_cookie(session)
status1 = wall1.get_status(user1)[3]

with open('cgi-bin/bd/wall.json', 'r', encoding='utf-8') as f:
    wall = json.load(f)
for i in wall["posts"]:
    user = i['user']
    status = wall1.get_status(user)[2]
    text = i['text']
    text = html.escape(text)
    img = i['img']
    time = i['time']
    if (user1 is not None) and (int(status1)==9):
        click = 'oncontextmenu="return menu(1, event, ' + "'"+user+"-"+time+"'"+');"'
    pm=''
    pm1=''
    k=0

    text_lst = text.split()
    for i in range(len(text_lst)):
        if (text_lst[i][0]=="@")and(text_lst[i][-1]==','):
            if (user1 is not None) and ((text.find('@'+user1+',')!=-1) or (user==user1) or(int(status1)==9)):
                pm = 'style="background-color: #D3F393;"'
                pm1 = '<a class="pm">Личное сообщение</a>'
            else:
                k=1
        elif text_lst[i][-1]==',':
            if (user1 is not None) and (text.find(user1 + ',') != -1):
                pm = 'style="background-color: #D3F393;"'
    if k!=1:
        posts = '<div class="message1" '+click+'><a class="time">'+time+'</a><img src="'+img+'" class ="img1" height="30" width="30"><a id="nick" onclick="return pm(\''+user+'\');" href="#" class="'+status+'">'+user+'</a>'+pm1+'<a class="message">: </a><a class="message"'+pm+'>'+text+'</a><br></div>'+posts
posts = '<meta charset="UTF-8" http-equiv="cache-control" content="no-cache"><br>'+posts
print("HTTP/1.0 200 OK")
print('Content-type: text/html\n')
print(posts)

