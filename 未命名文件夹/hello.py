import tkinter as tk 





def login(s):
	# 创建一个新窗口用来登录
	login_root = tk.Tk()
	login_root.title('登录窗口')
	label1 = tk.Label(login_root, text='帐号')
	label1.grid(row=0, column=0)
	entry1 = tk.Entry(login_root)
	entry1.grid(row=0, column=1)
	label2 = tk.Label(login_root, text='密码')
	label2.grid(row=1, column=0)
	entry2 = tk.Entry(login_root)
	entry2.grid(row=1, column=1)
	def on_but():
		name = entry1.get()
		passwd = entry2.get()
		s.send((name+' '+passwd).encode())
		login_root.destroy()
	but = tk.Button(login_root, text='登录', command=on_but)
	but.grid(row=2, column=0, columnspan=2)
	root.destroy()
	login_root.mainloop()



def register(s):
	register_root = tk.Tk()
	register_root.title('登录窗口')
	label1 = tk.Label(register_root, text='帐号')
	label1.grid(row=0, column=0)
	entry1 = tk.Entry(register_root)
	entry1.grid(row=0, column=1)
	label2 = tk.Label(register_root, text='密码')
	label2.grid(row=1, column=0)
	entry2 = tk.Entry(register_root)
	entry2.grid(row=1, column=1)
	def on_but():
		name = entry1.get()
		passwd = entry2.get()
		print(name,passwd)
		register_root.destroy()
	but = tk.Button(register_root, text='注册', command=on_but)
	but.grid(row=2, column=0, columnspan=2)
	root.destroy()
	register_root.mainloop()
	


def quit(s):
	s.send(b'Q')
	root.destroy()

def main():
	global root
	root = tk.Tk()
	root.title('请选择')

	btn1 = tk.Button(root, text='注册', command=lambda:register(s))
	btn1.pack(padx=50, pady=10)
	btn2 = tk.Button(root, text='登录', command=lambda:login(s))
	btn2.pack(padx=50, pady=10)
	btn3 = tk.Button(root, text='退出', command=lambda:quit(s))
	btn3.pack(padx=50, pady=10)
	root.mainloop()


if __name__ == '__main__':
	main()