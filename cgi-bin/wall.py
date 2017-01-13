#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
rand = str(random.randint(10000, 99999))
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) #Строчка, значение которой я не понимаю, но нужна для кодировки
from _wall import Wall
wall = Wall()
#Много лишних переменных. Нужно их потом убрать
reg=''
re='http-equiv="cache-control" content="no-store"'
exits=''
ex=''
ban=''

form = cgi.FieldStorage()
action = form.getfirst("action", "")

if wall.check_ban(html.escape(os.environ["REMOTE_ADDR"]))==True: #Проверяем ip в бан листе
    ban='<a>Ваш ip добавлен в чёрный список<a>'
    user = None
else: #Находим пользователя по куки
    cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    session = cookie.get("session")
    if session is not None:
        session = session.value
    user = wall.find_cookie(session)

if action == "login": #Заходим
    login = form.getfirst("login", "")
    login = html.escape(login)
    password = form.getfirst("password", "")
    password = html.escape(password)
    if wall.find(login, password)==True:
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))
        #re ='''HTTP-EQUIV="REFRESH" CONTENT="1; URL=wall.py"'''
        user = wall.find_cookie(cookie)
    elif wall.find(login, password)=='Ban':
        reg='Этот пользователь заблокирован'
    else:
        reg='Неверный логин или пароль'
elif action =="Exit": #Выходим
    print('''Set-cookie: session="" ''')
    #re ='''HTTP-EQUIV="REFRESH" CONTENT="1; URL=wall.py"'''
    user = None

#Наш любимый js
script='''
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
    <script>
jQuery(document).ready(function(){
    jQuery.ajaxSetup({cache: false});
    $('button.smiles').click(function() {
        var text = $( this ).text();
        $('#text').val($('#text').val()+text);
        return false;
    });
    $('#text').on('keydown', function( e ) {
        if( e.keyCode === 13 ) {
            e.preventDefault();
            $('#Submit').click();
        }
    });
    $('#form').submit(function(event){
        $.post("send-message.py", {text:$("#text").val()});
        document.getElementById('form').reset();
        jQuery.get("get-wall.py", function(data){
            jQuery("#block2chat").html(data);
        });
        return false;
    });
    jQuery.get("get-session.py",onResponse);
    function onResponse(data){
        jQuery("#in2").html(data);
    }
    jQuery.get("get-wall.py", function(data){
        jQuery("#block2chat").html(data);
    });
    setInterval(function() {
            jQuery.get("get-wall.py", function(data){
                jQuery("#block2chat").html(data);
            });
            jQuery.get("get-session.py",onResponse);
                function onResponse(data){
                jQuery("#in2").html(data);
    }
    }, 2500); 
});        
function defPosition(event) {
      var x = y = 0;
      if (document.attachEvent != null) {
            x = window.event.clientX + (document.documentElement.scrollLeft ? document.documentElement.scrollLeft : document.body.scrollLeft);
            y = window.event.clientY + (document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop);
      } else if (!document.attachEvent && document.addEventListener) { 
            x = event.clientX + window.scrollX;
            y = event.clientY + window.scrollY;
      } else {
      }
      return {x:x, y:y};
}
function pm(name){
    if( $('#text').val().indexOf(name+', ')<0){
        $('#text').val(name+', ' + $('#text').val());
    }
    return false;
}
function menu(type, evt, n) {
    evt = evt || window.event;
    evt.cancelBubble = true;
    var menu = document.getElementById("contextMenuId");
    var html = "";
    switch (type) {
        case (1) :
            html = "Меню";
            html += "<br><a href='"+n+"' id='delete'>Удалить сообщение</a>";
            html += "<br><a href='"+n+"' id='ban'>Забанить</a>";
        break;
        default :
            // Nothing
        break;
    }
    if (html) {
        menu.innerHTML = html;
        menu.style.top = defPosition(evt).y + "px";
        menu.style.left = defPosition(evt).x + "px";
        menu.style.display = "";
        var link;
        var link1;
        link = document.getElementById('delete');
        link1 = document.getElementById('ban');
        link.onclick = function() {
            var del;
            del = this.getAttribute('href');
                jQuery.get("delete-message.py", {delete:del});
                jQuery.get("get-wall.py", function(data){
                    jQuery("#block2chat").html(data);
                });
            return false;
        }
        link1.onclick = function() {
            var del;
            del = this.getAttribute('href');
               jQuery.get("ban.py", {ban:del});
            return false;
        }
    }
    return false;
}
function addHandler(object, event, handler, useCapture) {
    if (object.addEventListener) {
        object.addEventListener(event, handler, useCapture ? useCapture : false);
    } else if (object.attachEvent) {
        object.attachEvent('on' + event, handler);
    } else alert("Add handler is not supported");
}
addHandler(document, "contextmenu", function() {
    document.getElementById("contextMenuId").style.display = "none";
});
addHandler(document, "click", function() {
    document.getElementById("contextMenuId").style.display = "none";
});

    </script>  
</script>
<link rel="stylesheet" href="/assets/main.css">
'''
#Фигня, нужно будет потом убрать
style='''
    background: url(/{pathimgs}) repeat scroll transparent;
    font-weight: bold;
    color:{colors};
'''
qwert = wall.get_status(user)
style=style.format(pathimgs = qwert[0], colors = qwert[1])
style='<style>.status{'+style+'</style>'
pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="UTF-8" {res} >
<title>Тест</title>
{scripts}
{styles}
</head>
<body>
{bans}
<div id="contextMenuId" style="position:absolute; top:0; left:0; border:1px solid #666; background-color:#CCC; display:none; z-index: 99999; float:left;"></div>
<div class="counter">
    <a>Онлайн:</a>
    <p class="number" id="in2"></p>
</div>
<div class="block1logo">
        test0chat
</div>
{lcs}
    {publ}
<div class="block2">
        {publish}
    <div class="block2chat" id="block2chat">
            Ошибка загрузки чата!
    </div>
</div>
{exits}
</body>
</html>
'''
if user is not None:
    pub = '''
    <div class="block2send">
        <form id="form" method="post" class="form">
            <div class="block2text">
                <textarea name="text" id="text" placeholder="Напишите сообщение..." class="textform" autocomplete="off"></textarea>
                <input type="button" class="smile" tabindex="1">
                <div class="sub-menu">
                    <button class="smiles" id="smiles" type="button">😀</button><button class="smiles" id="smiles" type="button">😁</button><button class="smiles" id="smiles" type="button">😂</button><br>
                    <button class="smiles" id="smiles" type="button">😢</button><button class="smiles" id="smiles" type="button">😑</button><button class="smiles" id="smiles" type="button">😇</button><br>
                    <button class="smiles" id="smiles" type="button">😍</button><button class="smiles" id="smiles" type="button">😆</button><button class="smiles" id="smiles" type="button">😈</button><br>
                    <button class="smiles" id="smiles" type="button">😎</button><button class="smiles" id="smiles" type="button">😐</button><button class="smiles" id="smiles" type="button">😡</button><br>
                    <button class="smiles" id="smiles" type="button">😘</button><button class="smiles" id="smiles" type="button">😱</button><button class="smiles" id="smiles" type="button">😬</button><br>
                </div>
            </div>
            <div class="block2button">
                <input type="submit" id="Submit" name="submit" value="Отправить">
            </div>
        </form>
    </div>
    '''
    lc = '''
    <div class="lc">
    <a class="text1">Добро пожаловать <a class="status" style="position: relative; font-size: 25px">{Users}</a></a>
    <img src="{imgs}" class ="img" height="60" width="60">
    <div class="text3">
        <br>
        <a>Ваш статус:<span class="status" style="position: relative; left: 15px;">{status}</span></a><br>
        <a style="color:#373737" href="lc.py">Личный кабинет</a>
        <form class="exit" action="/cgi-bin/wall.py" method="post">
            <input type="hidden" name="action" value="Exit">
            <input type="submit" value="Выход" name="Exit">
        </form>
    </div>
    </div>
    '''
    pubs=''
    try:
        open('users/'+user+'/'+user+'.jpg', 'r')
        img = '/users/'+user+'/'+user+'.jpg?_='+rand
    except:
        img = '/users/default.jpg?_='+rand
    lc = lc.format(status=qwert[2], imgs=img, Users=user)
else:
    pub = ''
    lc = ''
    pubs='''
<div class="login">
    <a class="logintext">Войдите или </a> <a href="reg.py">зарегистрируйтесь!</a>
    <form action="/cgi-bin/wall.py" method="post">
        <input type="text" name="login" placeholder="Логин">
        <input type="password" placeholder="Пароль"name="password">
        <input type="hidden" name="action" value="login">
        <input type="submit" value="Войти">
    </form>
    <a class="logintext">{regs}</a>
</div>
'''
    pubs=pubs.format(regs=reg)
print("HTTP/1.0 200 OK")
print('Content-type: text/html\n')
print(pattern.format(publish=pub, res=re, publ=pubs, exits=ex, scripts=script, bans=ban, styles=style, lcs=lc))

