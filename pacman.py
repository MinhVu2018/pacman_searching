from tkinter import *
from PIL import ImageTk, Image
import math
import os
import queue
import time

UserInput = "map1.txt"	#input("Enter input file: ")
lst = []
f = open(UserInput, "r")

for v in f.readlines():
	v = v.strip().split(' ')
	v = [int(i) for i in v]
	
	lst.append(v)

n = lst[0][0]
m = lst[0][1]

pacman_x = lst[-1][0]
pacman_y = lst[-1][1]
pacman_position = -1

food_position = []

lst.pop(0)

# Convert maze to (node, prop)
data = []

for number in range(n*m):
    x = number // n
    y = number % n
    if x == pacman_x and y == pacman_y:
        pacman_position = number
    if lst[y][x] == 2:
        food_position.append(number)
    data.append( (number, lst[y][x]) )

# Adjacency list
full = []

for i in range(n*m):
	if data[i][1] == 1:	# wall
		full.append(None)

	elif data[i][1] == 3: # monster
		full.append(None)

	else:	# road or food
		temp = []
		if  ( data[i-n][1] == 0 or data[i-n][1] == 2 ):
			temp.append(data[i-n])
		if ( data[i-1][1] == 0 or data[i-1][1] == 2 ):
			temp.append(data[i-1])
		if ( data[i+1][1] == 0 or data[i+1][1] == 2 ):
			temp.append(data[i+1])
		if ( data[i+n][1] == 0 or data[i+n][1] == 2 ):
			temp.append(data[i+n])

		full.append(temp)

# Pacman object
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

# Monster object
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

# Food object
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

# Breadth first search
def BFS(adjacency_list, begin, food_position):
    expand_nodes = []
    parent = []
    pathtoexit = []

    parent = []
    for i in range(len(adjacency_list)):
        parent.append(-1)
    if begin == food_position:
        return 0, expand_nodes, pathtoexit
    qu = queue.Queue()
    qu.put(begin)

    while (qu.empty() == False):
        current_n = qu.get()
        expand_nodes.append(current_n)

        for adjacency_node in adjacency_list[current_n]:
            if adjacency_node[0] not in expand_nodes:
                qu.put(adjacency_node[0])
                parent[adjacency_node[0]] = current_n
        
        if (current_n == food_position):
            while parent[current_n] != -1:
                pathtoexit.append(current_n)
                current_n = parent[current_n]
            pathtoexit.append(current_n)
            pathtoexit.reverse()
            esc_time = 0
            for l in  range(len(pathtoexit)):
                esc_time += l
            return esc_time, expand_nodes, pathtoexit
    return None, None, None
        
### Iterative deepening search
# Depth-limited search
def DLS(adjacency_list, food_pos, explored, parent, current_path, depth):
    if current_path[-1] == food_pos:
        return True
    elif depth == 0: 
        return False
    
    for adjacency_node in adjacency_list[current_path[-1]]:
        if adjacency_node[0] not in current_path:
            parent[adjacency_node[0]] = current_path[-1]
            current_path.append(adjacency_node[0])
            explored.append(adjacency_node[0])
            result = DLS(adjacency_list, food_pos, explored, parent, current_path, depth - 1)
            if result == True:
                return True
            current_path.pop()
    return False
        

# Iterative deepning search
def IDS(adjacency_list, current_position, food_position, max_depth):
    explored_ns = [] # List of explored nodes
    path_fd = [] # List of nodes on the path found

    if current_position == food_position:
        return 0, explored_ns, path_fd

    for depth in range(max_depth - 1):
        parent = [-1] * len(adjacency_list)
        explored = [current_position]
        current_path = [current_position]
        result = DLS(adjacency_list, food_position, explored, parent, current_path, depth)
        explored_ns.append(explored)
        if result == True:
            cur_node = current_path[-1]
            while parent[cur_node] != -1:
                path_fd.append(cur_node)
                cur_node = parent[cur_node]
            path_fd.append(cur_node)
            path_fd.reverse()
            esc_time = 0
            for l in explored_ns:
                esc_time += len(l)
            return esc_time, explored_ns, path_fd

    return None, None, None


### 
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


#t, explored_ns, path_found = IDS(full, pacman_position, food_position[0], n * m)
t, explored_ns, path_found = BFS(full, pacman_position, food_position[0])
path_found.pop(0)

for p in path_found:
    p_x = p // n
    p_y = p % n
    # Check right
    if p_x == pacman_x + 1 and p_y == pacman_y:
        pacman_x = p_x
        pacman_y = p_y
        pacman_position = p
        pacman.move('Right', C)
        time.sleep(0.5)
        top.update()
        
    # Check left 
    elif p_x == pacman_x - 1 and p_y == pacman_y:
        pacman_x = p_x
        pacman_y = p_y
        pacman_position = p
        pacman.move('Left', C)
        time.sleep(0.5)
        top.update()
    
    # Check up
    elif p_x == pacman_x and p_y == pacman_y - 1:
        pacman_x = p_x
        pacman_y = p_y
        pacman_position = p
        pacman.move('Up', C)
        time.sleep(0.5)
        top.update()
    
    # Check down
    elif p_x == pacman_x and p_y == pacman_y + 1:
        pacman_x = p_x
        pacman_y = p_y
        pacman_position = p
        pacman.move('Down', C)
        time.sleep(0.5)
        top.update()


#def key_pressed(event):
#	pacman.move(event.keysym, C)

#top.bind("<Key>", key_pressed)
top.mainloop()
