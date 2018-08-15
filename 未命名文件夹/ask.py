def ask(gamelist):
    for i in gamelist:
        i.c.send('A'.encode())
        data = i.c.recv(1024).decode()
        i.result = int(data)
        print(i.result)
