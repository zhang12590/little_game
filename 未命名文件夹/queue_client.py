from socket import *

s = socket()
s.connect(('127.0.0.1', 8888))
while True:
    try:
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)
        msg = input('....')
        if msg == 'Y':
            s.send(msg.encode())
        elif msg == 'N':
            s.send(msg.encode())
            break
    except KeyboardInterrupt:
        break

s.close()
