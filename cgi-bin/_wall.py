#!c:\Python34\python.exe
# -*- coding: utf-8 -*-

import json
import random
import time
import sys
import os
import shutil
import hashlib
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
class Wall:
    USERS = 'bd/users.json'
    WALL = 'bd/wall.json'
    COOKIES = 'bd/cookies.json'
    IP = 'bd/ip.json'
    BANIP = 'bd/ban-list.json'
    SAVEDIR = '../users/'
    PEX = 'bd/permissions.json'
    PUSERS = 'bd/perusers.json'
    ID = 'bd/id.json'
    SESSIONS = 'bd/sessions-online.json'
    
    def __init__(self):
        try:
            with open(self.USERS, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.USERS, 'w', encoding='utf-8') as f:
                json.dump({}, f)

        try:
            with open(self.WALL, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.WALL, 'w', encoding='utf-8') as f:
                json.dump({"posts": []}, f)

        try:
            with open(self.COOKIES, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.COOKIES, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def register(self, user, password, ip):
        ban = ['!','@','#','$','%','^','&','*','(',')','~','`',',','.','/',' ','-','+','=']
        for i in range(len(ban)):
            if user.find(ban[i])!=-1:
                return False
        if self.find(user):
            return False
        with open(self.IP, 'r', encoding='utf-8') as f:
            ips = json.load(f)
        if list(ips.values()).count(ip)!=0:
            return False
        ips[user] = ip
        with open(self.IP, 'w', encoding='utf-8') as f:
            json.dump(ips, f)
        
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        users[user] = hashlib.md5(password.encode()).hexdigest()
        with open(self.USERS, 'w', encoding='utf-8') as f:
            json.dump(users, f)
        os.chdir('../')
        os.makedirs('users/'+user)
        shutil.copy('users/default.jpg','users/'+user+'/'+user+'.jpg')
        os.chdir('cgi-bin')
        return True

    def check_ban(self, ip):
        with open(self.BANIP, 'r', encoding='utf-8') as f:
            bans=json.load(f)
        if bans['bans'].count(ip)!=0:
            return True
    
    def set_cookie(self, user):
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        cookie = str(time.time()) + str(random.randrange(10**14))
        cookies[cookie] = user
        with open(self.COOKIES, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
        return cookie

    def find_cookie(self, cookie):
        with open(self.COOKIES, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        return cookies.get(cookie)

    def find(self, user, password=None):
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if user in users and (password is None or hashlib.md5(password.encode()).hexdigest() == users[user]):
            with open(self.BANIP, 'r', encoding='utf-8') as f:
                bans=json.load(f)
            with open(self.IP, 'r', encoding='utf-8') as f:
                ips = json.load(f)
            if list(bans.values())[0].count(ips[user])==0:
                return True
            else:
                return 'Ban'
        return False

    def save_file(self, fileitem, user):
        upload_dir = self.SAVEDIR+user
        try:
            os.makedirs(upload_dir)
        except:
            pass
        outpath = os.path.join(upload_dir, user+'.jpg')
        with open(outpath, 'wb') as fout:
            #shutil.copyfileobj(fileitem.file, fout)
            while 1:
                chunk = fileitem.file.read(100000)
                if not chunk: break
                fout.write(chunk)
            fout.close()
        im = Image.open(outpath)
        x,y = im.size
        z=min(x,y)
        z2=z/2
        x1=x/2-z2
        y1=y/2-z2
        x2=x1+z
        y2=y1+z
        im=im.crop((x1,y1,x2,y2))
        size=60,60
        im.thumbnail(size, Image.NEAREST)
        quality=100
        im.save(outpath, quality=quality)
        
    def publish(self, user, text):
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        img = '/users/'+user+'/'+user+'.jpg'
        #Немного индусского кода
        ms = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        if len(str(int(time.ctime()[8]+time.ctime()[9])))==1:
            d = '0'+time.ctime()[9]
        else:
            d = time.ctime()[8]+time.ctime()[9]
        for i in range(len(ms)):
            if ms[i] in time.ctime():
                    m = str(i+1)
        if len(m)==1:
            m='0'+m
        date = d+'.'+m+'.'+time.ctime().split()[4]+' '+time.ctime().split()[3]
        #Код индуса закончен
        wall['posts'].append({'user': user, 'text': text, 'img': img, 'time':date})
        with open(self.WALL, 'w', encoding='utf-8') as f:
            json.dump(wall, f)

    def get_status(self, user):
        with open(self.PEX, 'r', encoding='utf-8') as f:
            pex = json.load(f)
        with open(self.PUSERS, 'r', encoding='utf-8') as f:
            pusers = json.load(f)
        if user in pusers:
            if pusers[user] in pex:
                img = pex[pusers[user]][0]
                color = pex[pusers[user]][1]
                status = pex[pusers[user]][2]
                ids = pex[pusers[user]][3]
            else:
                img = pex['user'][0]
                color = pex['user'][1]
                status = pex['user'][2]
                ids = pex['user'][3]
        else:
            img = pex['user'][0]
            color = pex['user'][1]
            status = pex['user'][2]
            ids = pex['user'][3]
        a = [img, color, status, ids]
        return a
        
    def html_list(self):
        with open(self.WALL, 'r', encoding='utf-8') as f:
            wall = json.load(f)
        posts = []
        for post in wall['posts']:
            content = post['time']+'  '+post['user'] + ' : ' + post['text']
            posts.append(content)
        return posts

    def del_message(self, delete, status):
        if int(status) == 9:
            with open(self.WALL, 'r', encoding='utf-8') as f:
                wall = json.load(f)
            for i in range(len(wall["posts"])):
                if (delete[0] == wall["posts"][i]['user']) and (delete[1] == wall["posts"][i]['time']):
                    wall["posts"].pop(i)
                    break
            with open(self.WALL, 'w', encoding='utf-8') as f:
                json.dump(wall, f)

    def get_ban(self, ban, status):
        if int(status) == 9:
            with open(self.IP, 'r', encoding='utf-8') as f:
                ips = json.load(f)
            for i in ips:
                if i == ban[0]:
                    with open(self.BANIP, 'r', encoding='utf-8') as f:
                        bans = json.load(f)
                    bans['bans'].append(ips[i])
                    with open(self.BANIP, 'w', encoding='utf-8') as f:
                        json.dump(bans, f)
                    break
            with open(self.COOKIES, 'r', encoding='utf-8') as f:
                cookie = json.load(f)
            for i in cookie:
                if cookie[i] == ban[0]:
                    cookie[i] = None
            with open(self.COOKIES, 'w', encoding='utf-8') as f:
                json.dump(cookie, f)