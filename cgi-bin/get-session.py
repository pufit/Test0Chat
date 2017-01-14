# -*- coding: utf-8  -*-
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
wall = Wall()

users = []
g = {}
online = ''
onlst = []
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
        session = session.value
user = wall.find_cookie(session)

ip = os.environ["REMOTE_ADDR"]
with open('cgi-bin/bd/sessions-online.json', 'r', encoding='utf-8') as f:
        online_users = json.load(f)
b = online_users.copy()
for i in online_users:
        if (time.time()-float(online_users[i])) > 5:
                b.pop(i)
        online_users = b.copy()
if user is not None:
        b = {user:str(time.time())}
        online_users.update(b)
        with open('cgi-bin/bd/sessions-online.json', 'w', encoding='utf-8') as f:
            json.dump(online_users, f)
for i in online_users:
        users.append(i)

for user in users:
    status = wall.get_status(user)[3]
    try:
        g[status].append(user)
        g[status].sort()
    except:
        g[status]=[user]
for i in sorted(g):
        for j in range(len(g[i])):
                onlst.append(g[i][j])
for i in range(len(onlst)):
        user = onlst[i]
        status = wall.get_status(user)[2]
        online = '<span class="'+status+'" style="position: relative; bottom: 10px; font-weight: bold;">'+user+'</span><br>'+online

print('Status: 200 OK')
print('Content-Type: text/html')
print('')
print(online)
