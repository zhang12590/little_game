from multiprocessing import Pool
import multiprocessing
from socket import *


def fun1():
    s = socket()
    s.bind(('127.0.0.1', 8888))
    s.setsockopt(SOCK_STREAM, SO_REUSEADDR, 1)
    s.listen(10)
    while True:
        try:
            c, addr = s.accept()
            print('connect from', addr)
            lock.acquire()
            q.put(c)
            lock.release()
        except KeyboardInterrupt:
            break
    s.close()


def fun2():
    list1 = []
    while True:
        try:
            if q.qsize() >= 2:
                lock.acquire()
                while True:
                    list1.append(q.get())
                    if len(list1) == 2:
                        break
                lock.release()
                for i in list1:
                    i.send(b'OK')
                    data = i.recv(1024).decode()
                    if data == 'Y':
                        lock.acquire()
                        q.put(i)
                        lock.release()
                    elif data == 'N':
                        i.close()
                list1.clear()
        except KeyboardInterrupt:
            break


manager = multiprocessing.Manager()
q = manager.Queue()
lock = manager.Lock()
p = Pool()
p1 = p.apply_async(fun1)
p2 = p.apply_async(fun2)
p3 = p.apply_async(fun2)
p.close()
p.join()
