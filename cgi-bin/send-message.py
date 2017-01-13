import os
import cgi
import json
import html
import http.cookies
from _wall import Wall
wall= Wall()
storage = cgi.FieldStorage()
text = storage.getvalue('text')
#ids = storage.getvalue('ids')
if wall.check_ban(cgi.escape(os.environ["REMOTE_ADDR"]))==True: #Проверяем ip в бан листе
    ban='<a>Ваш ip добавлен в чёрный список<a>'
    user = None
else: #Находим пользователя по куки
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    session = cookie.get("session")
    if session is not None:
        session = session.value
    user = wall.find_cookie(session)
if (user is not None) and (text is not None):
    wall.publish(user, text)
print('Status: 200 OK')
print('Content-Type: text/plain')
print('')
