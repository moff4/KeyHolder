#!/usr/local/bin/python3.6
import time
import sys
import random
import json
import tkinter as tk
import tkinter.messagebox as MB

from cipher import Storage
import config as cfg


def Notify(title,text):
	MB.showinfo(title,text)

#
# Window where user write his password
#
class LockScreen:
	def __init__(self,app):
		self.parent = app

		self.frame = tk.LabelFrame(self.parent.root,borderwidth=10,bg=cfg.LockScreen_BackGroundColor,text = cfg.LockScreen_ScreenName)
		self.frame.place(width=300,height=200,x=100,y=50)

		self.__passwd_label = tk.Label(self.frame,text='Ur password?',bg=cfg.LockScreen_BackGroundColor)
		self.__passwd_label.place(height=30,width=110,x=90,y=30)	

		self.__passwd_text = tk.Entry(self.frame,bg=cfg.LockScreen_BackGroundColor,show='*')
		self.__passwd_text.bind("<Return>", self.parent.button_unlock)
		self.__passwd_text.place(height=30,width=110,x=90,y=80)	

		self.__button = tk.Button(self.frame,text=cfg.unlock_button,bg=cfg.LockScreen_BackGroundColor)
		self.__button.bind("<Button-1>", self.parent.button_unlock)
		self.__button.place(height=30,width=75,x=105,y=130)

	def get_passwd(self):
		return self.__passwd_text.get()

	def del_passwd(self):
		self.__passwd_text.delete(0,tk.END)

	def u_r_root(self):
		return self.parent.u_r_root() + 1


class MainScren:
	def __init__(self,app,parent,data,cmd):
		self.app = app
		self.parent = parent
		self.data = data
		
		self.allow_down = True

		self.frame = tk.LabelFrame(self.app.root,borderwidth=10,bg=cfg.LockScreen_BackGroundColor,text = cfg.MainScreen_ScreenName)
		self.frame.place(width=500,height=400,x=0,y=0)

		#
		# data to be added
		#
		self.__add_text = tk.Entry(self.frame,text=cfg.add_button,bg=cfg.LockScreen_BackGroundColor)
		self.__add_text.bind("<Return>", self.button_add)
		self.__add_text.place(height=30,width=280,x=10,y=330)

		scrollbar = tk.Scrollbar(self.frame)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.listbox = tk.Listbox(self.frame, yscrollcommand=scrollbar.set)
		for i in self.data:
			if type(self.data[i]) in [str,int,bool]:
				self.listbox.insert(tk.END, str(i) + ': ' + str(self.data[i]))
				self.allow_down = False
			else:
				self.listbox.insert(tk.END, str(i))

		if self.allow_down:
			self.listbox.bind("<Double-Button-1>", self.__show_data)
		else:
			self.listbox.bind("<Double-Button-1>", self.__copy_to_entry)
		#self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
		self.listbox.place(width = 450, height = 320, x = 10, y = 5)

		scrollbar.config(command=self.listbox.yview)

		self.__button = tk.Button(self.frame,bg=cfg.LockScreen_BackGroundColor)
		if cmd == 'lock':
			self.__button.configure(text=cfg.lock_button)
			self.__button.bind("<Button-1>", self.app.button_lock)
		elif cmd == 'up':
			self.__button.configure(text=cfg.lock_button_up)
			self.__button.bind("<Button-1>", self.button_up)
		self.__button.place(height=30,width=75,x=380,y=330)

		#
		# Button to add new data
		# 
		self.__add_button = tk.Button(self.frame,text=cfg.add_button,bg=cfg.LockScreen_BackGroundColor)
		self.__add_button.bind("<Button-1>", self.button_add)
		self.__add_button.place(height=30,width=75,x=300,y=330)

		#print(self.u_r_root())

	def button_add(self,x):
		st = self.__add_text.get()
		self.__add_text.delete(0,tk.END)
		#print('button_add: ',st)
		if st in self.data:
			Notify('Error','This field already exists')
		else:
			try:
				_type = type(self.data[list(self.data.keys())[0]])
			except:
				if self.u_r_root() == 3:
					_type = dict
				else:
					_type = str
			if _type == dict:
				self.data[st] = dict()
				self.listbox.insert(tk.END, st)
			elif _type in [int,float,str,bool,type(None)]:
				try:
					st1 = st.split(':')
					if len(st1)<2:
						Notify('Error','Msg should be like this: <key> : <value>')
						return
					key = st1[0]
					value = st1[1]
					for i in st1[2:]:
						value+=':'+i
					if key in self.data:
						self.listbox.delete(tk.ACTIVE,tk.ACTIVE)
					self.data[key]=value
					self.listbox.insert(tk.END, st)
				except:
					Notify('Error','Msg should be like this: <key> : <value>')
					return

	def __copy_to_entry(self,x):
		self.__add_text.delete(0,tk.END) 
		self.__add_text.insert(0,x.widget.get(tk.ACTIVE))

	#
	# draw new frame upper then previous
	#
	def __show_data(self,x):
		smth = self.data[x.widget.get(tk.ACTIVE)]
		if type(smth) in [dict]:
			self.screen = MainScren(self.app,self,smth,'up')
		else:
			#print(smth)
			pass

	def button_up(self,x):
		self.frame.destroy()

	def u_r_root(self):
		return self.parent.u_r_root() + 1

class App:
	def __init__(self):
		self.data = None
		self.passwd = None


		self.root = tk.Tk(screenName=cfg.ScreenName)
		self.root.configure(background=cfg.MainBackgroundColor)
		self.root.geometry('%sx%s+%s+%s'%(str(cfg.width),str(cfg.height),str(cfg.left),str(cfg.top)))
		self.screen = LockScreen(self);

		# exit buttom
		exit_button = tk.Button(self.root,text=cfg.exit_button,bg=cfg.MainBackgroundColor,command = sys.exit)
		exit_button.place(width=75,height=30,x=395,y=405)

		# help button
		help_button = tk.Button(self.root,text=cfg.help_button,bg=cfg.MainBackgroundColor)
		help_button.bind('<Button-1>',self.button_help)
		help_button.place(width=75,height=30,x=315,y=405)

		# short description
		tk.Label(self.root,text=cfg.description	,bg=cfg.MainBackgroundColor).place(width=330,height=15,x=80,y=270)

		#author
		tk.Label(self.root,text=cfg.auther		,bg=cfg.MainBackgroundColor).place(width=330,height=15,x=80,y=290)

		# version
		tk.Label(self.root,text=cfg.version		,bg=cfg.MainBackgroundColor).place(width=150,height=15,x=30,y=405)


	def run(self):
		self.root.mainloop()

	def u_r_root(self):
		return 1

	def button_unlock(self,x):
		self.passwd = self.screen.get_passwd()
		self.screen.del_passwd()
		boo = True
		try:
			stg = Storage(cfg.data_file)
			self.data = stg.load(self.passwd)
		except Exception as e:
			Notify('Error!','Got unexpected error!\n:(')
			boo = False

		if boo:
			self.screen.frame.destroy()
			self.screen = MainScren(self,self,self.data,'lock')

	def button_lock(self,x):
		if self.passwd == None or self.data == None:
			Notify('Error','Nothing to save')
		else:
			stg = Storage(cfg.data_file)
			stg.dump(self.passwd,self.data)
			Notify('Success','Data saved')
			sys.exit(0)

	def button_help(self,x):
		Notify(cfg.help_button,cfg.help_msg)

def main(argv):
	App().run()

if __name__ == '__main__':
	main(sys.argv)