from tkinter import *
from tkinter import messagebox
import copy
import numpy as np
from Searching_Algorithm import *
from Objects import *

# global lst, ListGhost, ListAdjacency, ListFood

def random_Maze():
    n = np.random.randint(5, 30)
    m = np.random.randint(5, 30)
    maze_temp = np.random.randint(3, size=(n, m))
    for i in range (n):
        for j in range (m):
            if(i == 0 or i == n - 1 or j == 0 or j == m - 1):
                maze_temp[i][j] = 1
    for i in range(np.random.randint(2,5)):
        g_x = 0
        g_y = 0
        while (maze_temp[g_y][g_x] != 0):
            g_x = np.random.randint(1, m - 1)
            g_y = np.random.randint(1, n - 1)
        maze_temp[g_y][g_x] = 3

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
    global input_map

    if input_map == "random":
    	lst = random_Maze()
    	return

    UserInput = input_map + ".txt"  #input("Enter input file: ")
    f = open(UserInput, "r")

    for v in f.readlines():
       v = v.strip().split(' ')
       v = [int(i) for i in v]
        
       lst.append(v)

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
                    t = random.randint(0,1) # 2 types
                    g = monster("redghost (1).png", j, i, n, t)
                    ListGhost.append(g)

    for g in ListGhost:
        g.display(C)

    for f in ListFood:
        f.display(C)

    p.display(C)

def create_data(C):
    # Convert maze to (node, prop)
    global data

    for number in range(n*m):
        x = number // n
        y = number % n
        if lst[y][x] == 3: # monster position
            if lv == 2:
            	data.append( (number, 1) ) 
            else:
            	data.append( (number, 0) )
        else:
            data.append( (number, lst[y][x]) )

    for i in range(n*m):
        if data[i][1] == 1: # wall
            ListAdjacency.append(None)

        else:   # road or food
            temp = []
            if  ( data[i-n][1] != 1 ):
                temp.append(data[i-n])
            if ( data[i-1][1] != 1 ):
                temp.append(data[i-1])
            if ( data[i+1][1] != 1 ):
                temp.append(data[i+1])
            if ( data[i+n][1] != 1 ):
                temp.append(data[i+n])

            temp.sort(key = lambda k:k[0])
            ListAdjacency.append(temp)

    for g in ListGhost:
        Adjacent_Pos = [g.index - n, g.index + n, g.index - n - 1, g.index - n + 1, g.index - 1, g.index + 1, g.index + n - 1, g.index + n + 1, g.index]
        MoveableFromInitLocation = []
        
        for i in Adjacent_Pos:
            x = i // n
            y = i % n
            if (x >= 0 and y >= 0) and (x <= m - 1 and y <= n - 1):
                if lst[y][x] != 1:  # not wall
                    MoveableFromInitLocation.append(i)
                    
        MoveableFromInitLocation.append(g.index)
                    
        g.MoveList = MoveableFromInitLocation.copy()

def display_score():
    global label_id
    C.delete(label_id)
    label_id = C.create_text(m*unit + 5*unit, n*unit/2, fill = "#f2ba0e", text = str(score), font=('Arial',20,'bold'))

def sort_Food():
    ListFood.sort(key = lambda k: np.sqrt((k.x - p.x)**2 + (k.y - p.y)**2))

def nearest_food_tactic1():
    global score
    global searching_time, len_path

    while len(ListFood) > 0:
        sort_Food()
        
        #time_temp, frontier, path = BFS(ListAdjacency, p.index, ListFood[0].index)
        #time_temp, frontier, path = DFS(ListAdjacency, p.index, ListFood[0].index)
        time_temp, frontier, path, cost = A_Star(ListAdjacency, p.index, ListFood[0].index, n)
        searching_time += int(time_temp)
        len_path += len(path)

        if len(path) == 0 or len(path) > 20: # cannot found 
            ListFood.remove(ListFood[0])          

        else:
			# if lv == 3:
			# 	for g in ListGhost:
			# 		g.ghost_random_move(lst, C, n)
			# 		if get_manhattan_heuristic(p.index, g.index, n) <= 2:
			# 			p.runnnn(C, n, ListAdjacency, g)
			# 			break

			# if lv == 4:
			# 	for g in ListGhost:
			# 		g.chase(lst, p.index, ListAdjacency,  C, n)
			# 		if get_manhattan_heuristic(p.index, g.index, n) <= 2:
			# 			p.runnnn(C, n, ListAdjacency, g)
			# 			break

            p.path_move(path[1], C, n)
            score -= 1
            display_score()
            for food_index in range(len(ListFood)):
                if ListFood[food_index].index == p.index:
                    score += 20
                    display_score()
                    ListFood[food_index].destroy(C)
                    del ListFood[food_index]
                    break
            time.sleep(0.05)
            top.update()

def nearest_food_tactic2():
    global score
    while len(ListFood) > 0:
        sort_Food()
        ListFood_currentState = ListFood
        
        path = A_Star(ListAdjacency, p.index, ListFood_currentState[0].index, n)[2]
        
        while len(path) == 0:
            ListFood_currentState.remove(ListFood_currentState[0])
            if len(ListFood_currentState) == 0:
                break
            path = A_Star(ListAdjacency, p.index, ListFood_currentState[0].index, n)[2]
        
        if len(ListFood_currentState) >= 4:
            min_index = 0
            for i in range(1, 4):
                pth = A_Star(ListAdjacency, p.index, ListFood_currentState[i].index, n)[2]
                if len(pth) != 0 and len(pth) < len(path):
                    path = pth
                    min_index = i
                    
            if min_index != 0:
                swap(ListFood_currentState[0], ListFood_currentState[min_index])
                    
        #if len(path) == 0:
         #   ListFood.remove(ListFood[0])
          #  if len(ListFood) == 0:
           #     break
           # path = A_Star(ListAdjacency, p.index, ListFood[0].index, n)[2]
        
        # flag = False
        while len(path) > 0:
            # if lv == 3:
            #     for g in ListGhost:
            #         g.ghost_random_move(lst, C, n)

            #         if get_manhattan_heuristic(p.index, g.index, n) <= 2:
            #             p.runnnn(C, n, ListAdjacency, g)
            #             for food_index in range(len(ListFood)):
            #                 if ListFood[food_index].index == p.index:
            #                     score += 20
            #                     display_score()
            #                     ListFood[food_index].destroy(C)
            #                     del ListFood[food_index]
            #                     break
            #             flag = True
            #             break
                    
            # if flag == True:
            #     break
            
            p.path_move(path[0], C, n)
            path.remove(path[0])
            score -= 1
            display_score()
            
            for food_index in range(len(ListFood)):
                if ListFood[food_index].index == p.index:
                    score += 20
                    display_score()
                    ListFood[food_index].destroy(C)
                    del ListFood[food_index]
                    break

            #sort_Food()
            #if len(ListFood) == 0:
             #   break
            #path = A_Star(ListAdjacency, p.index, ListFood[0].index, n)[2]

            time.sleep(0.05)
            top.update()

def highest_cost_tactic():
    global score
    while len(ListFood):
        ListCost = []
        ListPath = []
        for f in ListFood:
            algo = reverse_A_Star(ListAdjacency, p.index, f.index, n, ListGhost, ListFood)
            ListCost.append(algo[3])
            ListPath.append(algo[2])

        while ListPath[0] == []:
            del ListPath[0]
            del ListCost[0]
            if len(ListPath) == 0:
                return

        index_max = np.argmax(ListCost)

        if ListFood[index_max] == 0:    # all is 0
            return

        path = ListPath[index_max]
        # flag = False
        while len(path) > 0:
            # if lv == 3:
            #     for g in ListGhost:
            #         g.ghost_random_move(lst, C, n)

            #         if get_manhattan_heuristic(p.index, g.index, n) <= 2:
            #             p.runnnn(C, n, ListAdjacency, g)
            #             flag = True
            #             break    

            # if flag == True:
            #     break
            p.path_move(path[0], C, n)
            path.remove(path[0])
            score -= 1
            display_score()
            
            for food_index in range(len(ListFood)):
                if ListFood[food_index].index == p.index:
                    score += 20
                    display_score()
                    ListFood[food_index].destroy(C)
                    del ListFood[food_index]
                    break

            time.sleep(0.05)
            top.update()

def nearest_ghost():
    ListGhost.sort(key = lambda k: np.sqrt((k.x - p.x)**2 + (k.y - p.y)**2))
    return ListGhost[0]

def check_ghost_1(tile):
    g = nearest_ghost()
    for i in ListAdjacency[g.index]:
        if i[0] == tile:
            return True
    return False

def check_ghost_2(tile):
    g = nearest_ghost()
    if g.index == tile:
        return True
    for i in ListAdjacency[g.index]:
        if i[0] == tile:
            return True
    return False

def move_ghost():
    for g in ListGhost:
        if lv == 3:
            g.move_around_initpos(C, n)
        elif lv == 4:
            g.chase(lst, p.index, ListAdjacency, C, n)

        top.update()
        if g.index == p.index:
            return False
    return True

def blind_check_tactic():
    global score
    # print("DFS check all map")

    stack = [p.index]
    while len(stack):
        count = 0
        pre = p.index
        for i in ListAdjacency[p.index]:
            # print(1)
            if not p.check_tile(i[0]):# and not check_ghost(i[0]):

                if check_ghost_1(i[0]): # wait 1 step
                    if not move_ghost():
                        return

                    time.sleep(1)
                    top.update()
                    time.sleep(1)

                if not check_ghost_2(i[0]):
                    p.visited.append( (i[0],p.index) )
                    stack.append(i[0])
                    p.path_move(i[0], C, n)
                    score -= 1
                    display_score()

                    for food_index in range(len(ListFood)):
                        if ListFood[food_index].index == p.index:
                            score += 20
                            display_score()
                            ListFood[food_index].destroy(C)
                            del ListFood[food_index]
                            break

                    if not move_ghost():
                        return

                    time.sleep(0.2)
                    top.update()
                    break
                else:
                    count += 1
            else:
                count += 1

        if count == len(ListAdjacency[pre]):
            parent_tile = p.find_parent_tile(stack.pop(-1))

            if check_ghost_1(parent_tile):
                if not move_ghost():
                    return

                time.sleep(1)
                top.update()       
                time.sleep(1)     

            if not check_ghost_2(parent_tile):
                p.path_move(parent_tile, C, n)
                score -= 1
                display_score()
                if not move_ghost():
                    return
                time.sleep(0.2)
                top.update()

def RunAlgorithm():
    global searching_time, len_path
    searching_time = 0
    len_path = 0
    if lv <= 2:
        nearest_food_tactic1()
        # highest_cost_tactic()
    else:
        blind_check_tactic()

    C.create_text(m*unit/2 + 5*unit , n*unit/2, fill = "white", text = "END", font=('Arial',30,'bold'))
    print("searching_time", searching_time)
    print("Sum len paths", len_path)

def Play_vs_Com():
	print("not yet")

def key_pressed(event):
	global p

	if event.keysym == "Escape":
		top.destroy()
		del p    
		Start(1, "map1")
	elif event.keysym == "Return": # Enter
		RunAlgorithm()
	else:
		p.key_move(event.keysym, C, n)
		top.update()

def Play():
    global top, C, p
    global unit, n, m
    global lst, ListGhost, ListAdjacency, ListFood, data
    global label_id, score
    top = Tk()
    unit = 25
    lst = []
    ListGhost = []
    ListAdjacency = []
    ListFood = []
    data = []
    score = 0

    handle_input()
    # maze_size
    n = lst[0][0]
    m = lst[0][1]
    lst.pop(0)

    top.title("Pacman")
    C = Canvas(top, height = n*unit, width = m*unit + 10*unit, background = 'black')
    C.create_text(m*unit + 3*unit, n*unit/2 - 2*unit, fill = "#f61818", text = "S", font=('Arial',20,'bold'))
    C.create_text(m*unit + 4*unit, n*unit/2 - 2*unit, fill = "#1a98f6", text = "C", font=('Arial',20,'bold'))
    C.create_text(m*unit + 5*unit, n*unit/2 - 2*unit, fill = "#e3f00c", text = "O", font=('Arial',20,'bold'))
    C.create_text(m*unit + 6*unit, n*unit/2 - 2*unit, fill = "#1ce70a", text = "R", font=('Arial',20,'bold'))
    C.create_text(m*unit + 7*unit, n*unit/2 - 2*unit, fill = "#f2ba0e", text = "E", font=('Arial',20,'bold'))
    C.create_text(m*unit + 5*unit, n*unit/2 + 2*unit, fill = "white", text = "Press ENTER to play", font=('System', 10, 'bold'))
    C.create_text(m*unit + 5*unit, n*unit/2 + 3*unit, fill = "white", text = "Press ESC to return to menu", font=('System', 10, 'bold'))
    label_id = C.create_text(m*unit + 5*unit, n*unit/2, fill = "#f2ba0e", text = str(score), font=('Arial',20,'bold'))
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

def Play_bn(textbox):
    global mode
    mode = 'p'

    input_map = textbox.get("1.0", "end-1c")
    control.destroy()
    Start(lv, input_map)

def Run_bn(textbox): 
    global mode
    mode = 'r'

    input_map = textbox.get("1.0", "end-1c")

    control.destroy()
    Start(lv, input_map)

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

    textbox = Text(control, height = 1, width = 10)
    textbox.pack()

    button5 = Button(control, text = "Play", anchor = W, command = lambda: Play_bn(textbox))
    button5.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
    button5_window = C.create_window(100, 150, anchor=NW, window=button5)

    button6 = Button(control, text = "Run", anchor = W, command = lambda: Run_bn(textbox))
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

def key_start(event):
	if event.keysym == "Return":
		menu.destroy()
		Play()

def Start(level, maze):
	global menu
	global lv
	global input_map
	input_map = maze
	lv = level
	menu = Tk()
	menu.title("Menu")
	img = Image.open("Menu.jfif")
	C = Canvas(menu, width = img.size[0], height = img.size[1])
	img = ImageTk.PhotoImage(img)
	C.create_image(0, 0, image = img, anchor = 'nw')

	menu.bind("<Key>", key_start)
	C.bind("<Button-1>", mouseclick)
	C.pack()
	menu.mainloop()

Start(1, "map1")