import threading as th
import tkinter
import random



root = tkinter.Tk()
root.geometry('500x500+500+500')
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
    image = tkinter.PhotoImage(file=gifs[i])
    photos.append(image)
    i += 1
global cur_select
cur_select = 0
label = tkinter.Label(root, text="--",image=photos[cur_select])

label.pack()
def onTimer():
    # print("定时器函数已经调用!")
    global timer_id  # 声明timer_id 为全局变量
    timer_id = label.after(30, onTimer)  # 让定时器重复启动
    global cur_select
    # 生成1~6随机数中的一个,改变全局的cur_select
    cur_select = random.randint(0, 5)
    label.config(image=photos[cur_select])
onTimer()


def onStopTimer():
    label.after_cancel(timer_id)
    print("定时器已取消!")

def fun():
    root.destroy()

timer = th.Timer(2, onStopTimer)
timer.start()
btn = tkinter.Button(root, text='OK', command=fun)
btn.pack()
root.mainloop()
# choose_img()
# print('your point is', cur_select + 1)