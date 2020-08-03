from tkinter import *
from PIL import ImageTk, Image
import math
import os

UserInput = "pacmanmaze.txt"	#input("Enter input file: ")
lst = []
f = open(UserInput, "r")

for v in f.readlines():
	v = v.strip().split(' ')
	v = [int(i) for i in v]
	
	lst.append(v)

n = lst[0][0]
m = lst[0][1]
lst.pop(0)

class pacman(object):
	def __init__(self, imgpath):
		self.img = Image.open(imgpath)
		self.img = self.img.resize((25, 25),  Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(self.img)
		self.x = 30
		self.y = 30
		self.pic = None

	def display(self, x, y, C):
		C.delete(self.pic)
		self.x = x
		self.y = y
		self.pic = C.create_image(x, y, image = self.img, anchor = 'nw')

	def destroy(self, C):
		xtemp = self.x + 30
		ytemp = self.y + 10
		C.create_rectangle(xtemp, ytemp, xtemp+10, ytemp+10, outline = C["background"])
		C.create_line(xtemp+5, ytemp+10, xtemp+5, ytemp+30,fill =C["background"])

		#arms
		C.create_line(xtemp+5, ytemp+10, xtemp, ytemp + 30, fill = C["background"])
		C.create_line(xtemp+5, ytemp+10, xtemp+10, ytemp+30, fill =C["background"])
		#legs
		C.create_line(xtemp+5, ytemp+30, xtemp, ytemp+30, fill = C["background"])
		C.create_line(xtemp+5, ytemp+30, xtemp+10, ytemp+30, fill = C["background"])

	def move(self, keysym, C):
		x = self.x
		y = self.y

		if keysym == 'Right':
			self.display(x+25, y, C)
		elif keysym == 'Left':
			self.display(x-25, y, C)
		elif keysym == 'Up':
			self.display(x, y-25, C)
		elif keysym == 'Down':
			self.display(x, y+25, C)
		elif keysym == 'Escape':
			self.display(x+25, y+25, C)

class monster(object):
	def __init__(self, imgpath):
		temp = Image.open(imgpath)
		img2 = temp.resize((30, 30), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(img2)
		#self.img = ImageTk.PhotoImage(Image.open(imgpath))
		self.x = 0
		self.x = 0
		self.y = 0
	def display(self, x, y, C):
		self.x = x
		self.y = y
		C.create_image(x, y, image = self.img, anchor = 'nw')

class food(object):
	def __init__(self, imgpath):
		temp = Image.open(imgpath)
		img2 = temp.resize((30, 30), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(img2)
		self.x = 0
		self.y = 0
	def display(self, x, y, C):
		self.x = x
		self.y = y
		C.create_image(x, y, image = self.img, anchor = 'nw')

# class App(Tk):
# 	def __init__(self):
# 		super(App, self).__init__()
# 		self.title('Pacman')

# 		self.top = Label(self)
# 		self.top.pack()	
# 		self.C = Canvas(self.top, height = n*25, width = m*25, background = 'black')
# 		self.C.pack()
# 		self.ghost = monster("redghost.jpg")
# 		self.food = food("banana.jpg")
# 		self.pacman = pacman("pacman.jpg")

# 		self.create_maze(lst, n)

# 	def create_maze(self, lst, n):
# 		for i in range(n):
# 			for j in range(m):
# 				if lst[i][j] == 1:
# 					self.C.create_rectangle(j*25, i*25, (j+1)*25, (i+1)*25, fill = 'blue')
# 				elif lst[i][j] == 2:
# 					self.food.display(j*25, i*25, self.C)
# 				elif lst[i][j] == 3:
# 					self.ghost.display(j*25, i*25, self.C)

# 		self.pacman.display(lst[-1][0] *25, lst[-1][1] * 25, self.C)

# 	def key_pressed(self, event):
# 		print("o")
# 		self.pacman.move(event.keysym, self.C)

# 	def Play(self):
# 		self.create_maze(lst,n)
# 		print("H")
# 		#self.after(300, self.Play)	#1000 milisec, after(parent, ms, function = None, *args)

# 	def run(self):
# 		self.top.bind("<Key>", self.key_pressed)
# 		self.mainloop()
	


# maze = App()
# maze.Play()
# maze.run()

top = Tk()
C = Canvas(top, height = n*25, width = m*25, background = 'black')
C.pack()
ghost = monster("redghost (1).png")
pacman = pacman("pacman.png")

def create_maze(lst, n):
	for i in range(n):
		for j in range(m):
			if lst[i][j] == 1:
				C.create_rectangle(j*25, i*25, (j+1)*25, (i+1)*25, fill = 'blue')
			elif lst[i][j] == 2:
				# food.display(j*25, i*25, C)
				C.create_oval(j*25 + 5, i*25 + 5, (j+1)*25 - 5, (i+1)*25 - 5, fill = 'white')
			elif lst[i][j] == 3:
				ghost.display(j*25, i*25, C)
	pacman.display(lst[-1][0] *25, lst[-1][1] * 25, C)

create_maze(lst, n)

def key_pressed(event):
	pacman.move(event.keysym, C)

top.bind("<Key>", key_pressed)
top.mainloop()
