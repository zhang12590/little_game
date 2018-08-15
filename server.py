from socket import *
from pythonmysql import *
import time
from multiprocessing import Pool, Process, Queue, Lock
import multiprocessing
import pymysql

coon = pymysql.Connect('localhost','root','123456',charset='utf8')
cur = coon.cursor()
sql_createDB = '''create database if not exists game default charset=utf8; use game;'''
sql_createRB = '''create table if not exists players(
name varchar(20),
passwd varchar(20),
money float(7,2)
)default charset=utf8;'''
cur.execute(sql_createDB)
cur.execute(sql_createRB)
coon.commit()
cur.close()
coon.close()
class Player(object):
    def __init__(self, name, passwd, conn, money=200.0):
        self.name = name
        self.passwd = passwd
        self.c = conn
        self.money = money
        self.moneychange = 0.0
        self.result = 0


def judgment(gamelist):
    pass
    L = []
    for i in gamelist:
        L.append(i.result)
    maxvalue = max(L)
    maxvaluecount = L.count(maxvalue)
    for j in gamelist:
        if j.result == maxvalue:
            j.moneychange = len(L) / maxvaluecount
        else:
            j.moneychange = 0.0


def ask(gamelist):
    for i in gamelist:
        i.c.send('A'.encode())
        data = i.c.recv(1024).decode()
        i.result = int(data)
        print(i.result)


def do_child1(q, lock):
    gamelist = []
    while True:
        try:
            if q.qsize() >= 2:
                # lock.acquire()
                while True:
                    gamelist.append(q.get())
                    if len(gamelist) == 2:
                        break
                # lock.release()
                for i in gamelist:
                    match(i)
                    i.c.send(b'Y')
                    ready = i.c.recv(1024).decode()
                    print(ready)
                    time.sleep(1)
                    i.c.send(('你还有%f的金币' % i.money).encode())
                    i.money -= 1
                ask(gamelist)
                judgment(gamelist)
                for j in gamelist:
                    update(j)
                for k in gamelist:
                    print('enter end')
                    k.c.send(b'E')
                    time.sleep(1)
                    k.c.send(('你获得%f的金币' % k.moneychange).encode())
                    time.sleep(1)
                    k.c.send(b'G')
                    data = k.c.recv(1024).decode()
                    print(data)
                    if data == 'Y':
                        # lock.acquire()
                        print('on lock')
                        q.put(k)
                        print('out lock')
                        # lock.release()
                    else:
                        k.c.send(b'Q')

                    
                gamelist.clear()
        except KeyboardInterrupt:
            break


def do_child(q, lock):
    gamelist = []
    while True:
        try:
            # lock.acquire()
            while True:
                gamelist.append(q.get())
                if len(gamelist) == 2:
                    break
            # lock.release()
            for i in gamelist:
                match(i)
                i.c.send(b'Y')
                ready = i.c.recv(1024).decode()
                print(ready)
                time.sleep(1)
                i.c.send(('你还有%f的金币' % i.money).encode())
                i.money -= 1
            ask(gamelist)
            judgment(gamelist)
            for j in gamelist:
                update(j)
            for k in gamelist:
                print('enter end')
                k.c.send(b'E')
                time.sleep(1)
                k.c.send(('你获得%f的金币' % k.moneychange).encode())
                time.sleep(1)
                k.c.send(b'G')
                data = k.c.recv(1024).decode()
                print(data)
                if data == 'Y':
                    # lock.acquire()
                    print('on lock')
                    q.put(k)
                    print('out lock')
                    # lock.release()
                else:
                    k.c.send(b'Q')

                    
            gamelist.clear()
        except KeyboardInterrupt:
            break


def do_parent():
    s = socket()
    s.setsockopt(SOCK_STREAM, SO_REUSEADDR, 1)
    s.bind(('localhost', 9999))
    s.listen(10)
    while True:
        c, addr = s.accept()
        print('connect from', addr)
        c.send(b'OK')
        while True:
            try:
                data = c.recv(1024).decode()
                if not data:
                    c.close()
                    break
                print(data)
                if data == 'L':
                    data1 = c.recv(1024).decode()
                    if not data1:
                        c.close()
                        break
                    name_passwd = data1.split(' ')
                    player = Player(name_passwd[0], name_passwd[1], c)
                    if not match(player):
                        c.send(b'N')
                        del player
                    else:
                        c.send(b'Y')
                        data2 = c.recv(1024).decode()
                        if not data2:
                            del player
                            c.close()
                            break
                        time.sleep(1)
                        c.send('wait for game start'.encode())
                        # lock.acquire()
                        q.put(player)
                        # lock.release()
                        del player
                        c.close()
                        break
                if data == 'R':
                    data1 = c.recv(1024).decode()
                    if not data1:
                        c.close()
                        break
                    name_passwd = data1.split(' ')
                    player = Player(name_passwd[0], name_passwd[1], c)
                    if not register(player):
                        c.send(b'N')
                        del player
                    else:
                        c.send(b'Y')
                        data2 = c.recv(1024).decode()
                        if not data2:
                            del player
                            c.close()
                            break
                        time.sleep(1)
                        c.send('wait for game start'.encode())
                        # lock.acquire()
                        q.put(player)
                        # lock.release()
                        del player
                        c.close()
                        break
                elif data == 'Q':
                    c.send(b'Q')
                    c.close()
                    break
            except KeyboardInterrupt:
                break
    s.close()


manager = multiprocessing.Manager()
q = manager.Queue()
lock = manager.Lock()
p = Pool()
p1 = p.apply_async(do_parent)
p2 = p.apply_async(do_child, args=(q,lock))
p3 = p.apply_async(do_child1, args=(q,lock))
p.close()
p.join()
# q = Queue()
# lock = Lock()
# p1 = Process(target=do_parent)
# p2 = Process(target=do_child)
# p3 = Process(target=do_child)
# p1.start()
# p2.start()
# p3.start()
# p1.join()
# p2.join()
# p3.join()