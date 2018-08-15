from socket import *
import threading as th
import tkinter as tk
import random
import time

s = socket()
s.connect(('localhost', 9999))
while True:
    data = s.recv(1024).decode()
    if not data:
        break
    print(data)
    if data == 'OK' or data == 'N':
        root = tk.Tk()
        root.title('请选择')
        root.geometry('300x300+400+400')


        def login():
            s.send(b'L')
            root1 = tk.Tk()
            root1.geometry('300x300+400+400')
            label1 = tk.Label(root1, text='帐号')
            label1.grid(row=0, column=0)
            entry1 = tk.Entry(root1)
            entry1.grid(row=0, column=1)
            label2 = tk.Label(root1, text='密码')
            label2.grid(row=1, column=0)
            entry2 = tk.Entry(root1, show='*')
            entry2.grid(row=1, column=1)

            def on_but():
                name = entry1.get()
                passwd = entry2.get()
                s.send((name + ' ' + passwd).encode())
                root1.destroy()
                root.destroy()

            but = tk.Button(root1, text='登录', command=on_but)
            but.grid(row=2, column=0, columnspan=2)
            root1.mainloop()


        def register():
            s.send(b'R')
            root1 = tk.Tk()
            root1.geometry('300x300+400+400')
            label1 = tk.Label(root1, text='帐号')
            label1.grid(row=0, column=0)
            entry1 = tk.Entry(root1)
            entry1.grid(row=0, column=1)
            label2 = tk.Label(root1, text='密码')
            label2.grid(row=1, column=0)
            entry2 = tk.Entry(root1, show='*')
            entry2.grid(row=1, column=1)

            def on_but():
                name = entry1.get()
                passwd = entry2.get()
                s.send((name + ' ' + passwd).encode())
                root1.destroy()
                root.destroy()

            but = tk.Button(root1, text='注册', command=on_but)
            but.grid(row=2, column=0, columnspan=2)
            root1.mainloop()


        def q():
            s.send(b'Q')
            root.destroy()


        but1 = tk.Button(root, text='登录', command=lambda: login())
        but1.pack(padx=50)
        but2 = tk.Button(root, text='注册', command=lambda: register())
        but2.pack(padx=50)
        but3 = tk.Button(root, text='退出', command=lambda: q())
        but3.pack(padx=50)
        root.mainloop()
    elif data == 'Y':
        s.send(b'ready')
        time.sleep(0.1)
        data2 = s.recv(1024).decode()
        root4 = tk.Tk()
        root4.geometry('300x300+400+400')
        label3 = tk.Label(root4, text=data2)
        label3.pack()


        def fun1():
            root4.destroy()


        but6 = tk.Button(root4, text='确定', command=fun1)
        but6.pack(padx=50)
        root4.mainloop()
    elif data == 'E':
        time.sleep(0.1)
        data1 = s.recv(1024).decode()
        root3 = tk.Tk()
        root3.geometry('300x300+400+400')
        label1 = tk.Label(root3, text=info)
        label1.pack()
        label2 = tk.Label(root3, text=data1)
        label2.pack()


        def fun():
            root3.destroy()


        but5 = tk.Button(root3, text='游戏结束', command=lambda: fun())
        but5.pack(padx=50)
        root3.mainloop()
    elif data == 'Q':
        break
    elif data == 'A':
        root2 = tk.Tk()
        root2.geometry('300x300+400+400')
        label4 = tk.Label(root2, text='按OK掷点')
        label4.pack()


        def run():
            root2.destroy()
            root = tk.Tk()
            root.geometry('600x600+400+400')
            gifs = ["img/one.gif",
                    "img/two.gif",
                    "img/three.gif",
                    "img/four.gif",
                    "img/five.gif",
                    "img/six.gif"
                    ]

            photos = []
            i = 0
            while i < len(gifs):
                image = tk.PhotoImage(file=gifs[i])
                photos.append(image)
                i += 1
            global cur_select
            cur_select = 0
            label = tk.Label(root, text="--", image=photos[cur_select])
            label.pack()

            def onTimer():
                global timer_id
                timer_id = label.after(30, onTimer)  # 让定时器重复启动
                global cur_select
                # 生成1~6随机数中的一个,改变全局的cur_select
                cur_select = random.randint(0, 5)
                label.config(image=photos[cur_select])

            onTimer()

            def onStopTimer():
                label.after_cancel(timer_id)
                print("定时器已取消!")
                try:
                    label.after_cancel(timer_id)
                except Exception:
                    pass

            def fun():
                num = cur_select + 1
                s.send(str(num).encode())
                global info
                info = '你的点数是%d' % num
                root.destroy()

            timer = th.Timer(1.5, onStopTimer)
            timer.start()
            btn = tk.Button(root, text='OK', command=fun)
            btn.pack()
            root.mainloop()


        but4 = tk.Button(root2, text='OK', command=lambda: run())
        but4.pack(padx=50)
        root2.mainloop()
    elif data == 'G':
        root = tk.Tk()
        root.geometry('400x400+400+400')
        label1 = tk.Label(root, text='是否继续游戏')
        label1.pack()


        def fun1():
            s.send(b'Y')
            root.destroy()


        def fun2():
            s.send(b'N')
            root.destroy()


        btn1 = tk.Button(root, text='是', command=fun1)
        btn1.pack()
        btn2 = tk.Button(root, text='否', command=fun2)
        btn2.pack()
        root.mainloop()

s.close()
