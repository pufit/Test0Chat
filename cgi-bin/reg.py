import cgi
import html
import http.cookies
import os
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from _wall import Wall
wall = Wall()
re=''
er=''
k=0
pattern='''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8" {res}>
    <title>Регистрация</title>
    <link rel="stylesheet" href="/assets/reg.css">
</head>
<body>
<div class="block1">
    <form action="reg.py"  method="post">
        <div class="reg1">
            <h1 class="reg">Регистрация</h1>
            <input type="text" name="login" class="login" autocomplete="off" placeholder="Введите логин..." required pattern="^[a-zA-Z0-9_]+$">
            <input type="password" name="password" class="password" autocomplete="off" placeholder="Введите пароль..." required pattern="^[a-zA-Z0-9]+$">
            <input type="password" name="repassword" class="repassword" autocomplete="off" placeholder="Повторите пароль..." required>
        </div>
        <h2 class="error"></h2>
        <div class="checkbox">
            <input type="checkbox" name="checkbox" required><a class="textcheckbox">С <a href="#openModal">правилами</a> проекта согласен</a>
        <div id="openModal" class="modalDialog">
            <div>
                <a href="#close" title="Закрыть" class="close">X</a>
                <h2>Правила<h2>
                <ul class="pravila">
                    <li>Администратор всегда прав!</li>
                    <li>Администрация вправе изменять правила без предупреждения!</li>
                    <li>Ненормативная лексика запрещена!</li>
                    <li>Мультиаккаунты запрещены!</li>
                    <li>Любые попытки взлома запрещены!</li>
                    <li>Уважайте других участников! Любые оскорбления запрещены!</li>
                </ul>
            </div>
        </div>
        </div>
        <div class="reg2">
            <input type="hidden" name="action" value="login">
            <input type="submit">
        </div>
    </form>
</div>
</body>
</html>
'''


form = cgi.FieldStorage()
password = form.getfirst("password", "")
password = html.escape(password)
login = form.getfirst("login", "")
login = html.escape(login)
repassword = form.getfirst("repassword", "")
repassword = html.escape(repassword)
checkbox = form.getfirst("checkbox", "")
if (password==repassword) and((password!='') and (login!='')) and (checkbox!=''):
    if wall.register(login, password, cgi.escape(os.environ["REMOTE_ADDR"]))==True:
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))
        k=1
if k==1:
    re='''HTTP-EQUIV="REFRESH" CONTENT="1; URL=wall.py"'''
print('Content-type: text/html\n')
print(pattern.format(res=re))
