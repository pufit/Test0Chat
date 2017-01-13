#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import cgi
import cgitb
import html
import http.cookies
import os
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from _wall import Wall
wall = Wall()
file=''
user=''
random = random.randint(10000, 99999)
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value 
    user = wall.find_cookie(session)
    try:
        form = cgi.FieldStorage()
        fileitem = form['filename']
        wall.save_file(fileitem, user)
        file='Загрузка прошла успешно'
    except:
        pass
    try:
        open('users/'+user+'/'+user+'.jpg', 'r')
        avatar = '/users/'+user+'/'+user+'.jpg'
    except:
        avatar = '/users/default.jpg'
    a = '''
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" />
  <title>Личный кабинет</title>
  <link rel="stylesheet" href="/assets/lc.css">
 </head>
 <body>
<div class="block2">
    <div class="name">
    <h2>{users}<img src="{avatars}?id={randoms}" class ="img" height="60" width="60" > </h2>
    </div>
    <div class="form">
        <form enctype="multipart/form-data"
            action="lc.py" method="post">
            <p>File: <input type="file" name="filename" accept="image/*"></p>
            <p><input type="submit" value="Upload"></p>
        </form>
    </div>
    {files}
</div>
 </body>
</html>
'''
else:
    a='''
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" />
  <title>Загрузка файла</title>
 </head>
 <body>
 {users}
<h1>Требуется авторизация!</h1>
</body>
</html>
'''
print("HTTP/1.0 200 OK")
print('Content-type: text/html\n')
print(a.format(files=file, users=user, avatars = avatar, randoms=random))
