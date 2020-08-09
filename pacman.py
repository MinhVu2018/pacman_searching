from tkinter import *
from tkinter import messagebox
import numpy as np
from Searching_Algorithm import *
from Objects import *

def random_Maze():
    n = np.random.randint(5, 30)
    m = np.random.randint(5, 30)
    maze_temp = np.random.randint(4, size=(n, m))
    for i in range (n):
        for j in range (m):
            if(i == 0 or i == n - 1 or j == 0 or j == m - 1):
                maze_temp[i][j] = 1
    lst = []
    lst.append([n,m])

    for i in range(n):
        lst.append(list(maze_temp[i]))

    p_x = 0
    p_y = 0
    while (maze_temp[p_y][p_x] != 0):
        p_x = np.random.randint(1, m - 1)
        p_y = np.random.randint(1, n - 1)
    
    lst.append([p_x, p_y])
    return lst


def handle_input():
    global lst
    # UserInput = "map3.txt"  #input("Enter input file: ")
    # f = open(UserInput, "r")

    # for v in f.readlines():
    #     v = v.strip().split(' ')
    #     v = [int(i) for i in v]
        
    #     lst.append(v)
    lst = random_Maze()


def create_maze(C):
    for i in range(n):
        for j in range(m):
            if lst[i][j] == 1: # wall
                C.create_rectangle(j*unit, i*unit, (j+1)*unit, (i+1)*unit, fill = 'blue')

            elif lst[i][j] == 2: # food
                # food.display(j*unit, i*unit, C)
                f = food(j, i, n)
                ListFood.append(f)
            elif lst[i][j] == 3: #monster
                if lv != 1:
                    g = monster("redghost (1).png", j, i, n, lv)
                    ListGhost.append(g)

    for g in ListGhost:
        g.display(C)

    for f in ListFood:
        f.display(C)

    p.display(C)

def create_data(C):
    # Convert maze to (node, prop)
    data = []

    for number in range(n*m):
        x = number // n
        y = number % n
        if lv == 1 and lst[y][x] == 3: # monster at lv1
            data.append( (number, 0) )
        else:
            data.append( (number, lst[y][x]) )

    for i in range(n*m):
        if data[i][1] == 1: # wall
            ListAdjacency.append(None)

        elif data[i][1] == 3 : # monster
            ListAdjacency.append(None)

        else:   # road or food
            temp = []
            if  ( data[i-n][1] == 0 or data[i-n][1] == 2 ):
                temp.append(data[i-n])
            if ( data[i-1][1] == 0 or data[i-1][1] == 2 ):
                temp.append(data[i-1])
            if ( data[i+1][1] == 0 or data[i+1][1] == 2 ):
                temp.append(data[i+1])
            if ( data[i+n][1] == 0 or data[i+n][1] == 2 ):
                temp.append(data[i+n])

            ListAdjacency.append(temp)

def RunAlgorithm():
    while len(ListFood):
        sort_Food()
        path = A_Star(ListAdjacency, p.index, ListFood[0].index, n)[2]
       
        p.path_move(path, C, n, top)
        
        ListFood[0].destroy(C)
        del ListFood[0]
        top.update()

def sort_Food():
    ListFood.sort(key = lambda k: abs(k.x-p.x) + abs(k.y - p.y))

def key_pressed(event):
    global p
    if event.keysym == "Escape":
        top.destroy()
        del p    
        Start(1)
    elif event.keysym == "Return": # Enter
        RunAlgorithm()
    else:
        p.key_move(event.keysym, C, n)
        top.update()

def Play():
    global top, C, p
    global unit, n, m
    global lst, ListGhost, ListAdjacency, ListFood
    top = Tk()
    unit = 25
    lst = []
    ListGhost = []
    ListAdjacency = []
    ListFood = []

    handle_input()
    # maze_size
    n = lst[0][0]
    m = lst[0][1]
    lst.pop(0)

    top.title("Pacman")
    C = Canvas(top, height = n*unit, width = m*unit, background = 'black')
    C.pack()

    # pacman position
    pacman_x = lst[-1][0]
    pacman_y = lst[-1][1]

    p = pacman("pacman.png", pacman_x, pacman_y, n)
    lst.pop(-1)

    create_maze(C)
    create_data(C)

    top.bind("<Key>", key_pressed)
    top.mainloop()

def lv1_bn():
    global lv
    lv = 1

def lv2_bn():
    global lv
    lv = 2

def lv3_bn():
    global lv
    lv = 3

def lv4_bn():
    global lv
    lv = 4

def Play_bn():
    global mode
    mode = 'p'
    control.destroy()
    Start(lv)

def Run_bn(): 
    global mode
    mode = 'r'
    control.destroy()
    Start(lv)

def Controls():
    menu.destroy()

    global control
    global mode
    control = Tk()
    img = Image.open("controls.png")
    C = Canvas(control, width = img.size[0], height = img.size[1] + 100, background = "black")

    C.pack()
    control.title("Controls")
    img = ImageTk.PhotoImage(img)
    C.create_image(0, 0, image = img, anchor = 'nw')

    button1 = Button(control, text = "lv1", anchor = W, command = lv1_bn)
    button1.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button1_window = C.create_window(20, 120, anchor=NW, window=button1)

    button2 = Button(control, text = "lv2", anchor = W, command = lv2_bn)
    button2.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button2_window = C.create_window(100, 120, anchor=NW, window=button2)

    button3 = Button(control, text = "lv3", anchor = W, command = lv3_bn)
    button3.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button3_window = C.create_window(180, 120, anchor=NW, window=button3)

    button4 = Button(control, text = "lv4", anchor = W, command = lv4_bn)
    button4.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button4_window = C.create_window(260, 120, anchor=NW, window=button4)

    button5 = Button(control, text = "Play", anchor = W, command = Play_bn)
    button5.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button5_window = C.create_window(100, 150, anchor=NW, window=button5)

    button6 = Button(control, text = "Run", anchor = W, command = Run_bn)
    button6.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button6_window = C.create_window(180, 150, anchor=NW, window=button6)

    control.mainloop()

def mouseclick(event):
    x = event.x
    y = event.y
    if 130 <= x <= 195 and 140 <= y <= 153:
        menu.destroy()
        Play()
    elif 102 <= x <= 222 and 180 <= y <= 193:
        Controls() 
    elif 113 <= x <= 207 and 218 <= y <= 233:
        messagebox.showinfo( "Credit", "Team Pacman:\n Vo Van Quoc Huy\n Vu Cong Minh\n Tu Kien Hoa\n Tu Kien Vinh")

def Start(level):
    global menu
    global lv
    lv = level
    menu = Tk()
    menu.title("Menu")
    img = Image.open("Menu.jfif")
    C = Canvas(menu, width = img.size[0], height = img.size[1])
    img = ImageTk.PhotoImage(img)
    C.create_image(0, 0, image = img, anchor = 'nw')
    
    C.bind("<Button-1>", mouseclick)
    
    C.pack()
    menu.mainloop()

Start(1)