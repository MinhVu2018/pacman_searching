from PIL import ImageTk, Image, ImageOps
from Searching_Algorithm import*
import time, random
unit = 25
# Pacman object
class pacman(object):
    def __init__(self, imgpath, x, y, n):
        temp = Image.open(imgpath)
        img2 = temp.resize((25, 25), Image.ANTIALIAS)

        self.right = img2
        self.down = img2.rotate(270)
        self.left = img2.rotate(180)
        self.up = img2.rotate(90)

        self.img = ImageTk.PhotoImage(img2)
        self.x = x
        self.y = y
        self.index = x*n + y
        self.pic = None
        self.visited = [(self.index, -1)]   #(current, parent)

    def check_tile(self, tile):
        for t in self.visited:
            if tile == t[0]:
                return True
        return False

    def find_parent_tile(self, tile):
        for t in self.visited:
            if tile == t[0]:
                return t[1]
        return None

    def display(self, C):
        C.delete(self.pic)

        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def key_move(self, keysym, C, n):
        if keysym == "Right":
            self.x += 1
            self.index += n
            self.img = ImageTk.PhotoImage(self.right)
        elif keysym == "Left":
            self.x -= 1
            self.index -= n
            self.img = ImageTk.PhotoImage(self.left)
        elif keysym == "Up":
            self.y -= 1
            self.index -= 1
            self.img = ImageTk.PhotoImage(self.up)
        elif keysym == "Down":
            self.y += 1
            self.index += 1
            self.img = ImageTk.PhotoImage(self.down)

        self.display(C)

    def path_move(self, tile, C, n):
        if tile == self.index + n:  # right
            self.key_move("Right", C, n)

        elif tile == self.index - n:  # left
            self.key_move("Left", C, n)

        elif tile == self.index - 1:  # up
            self.key_move("Up", C, n)

        elif tile == self.index + 1:  # down
            self.key_move("Down", C, n)

    def runnnn(self, C, n, ListAdjacency, ghost):
        ListEvade = []
        for i in range(len(ListAdjacency[self.index])):
            tile = ListAdjacency[self.index][i][0]
            if get_manhattan_heuristic(tile, ghost.index, n) == 1:
                ListEvade.append(tile)
        
        if len(ListEvade) != 0:
            random_evade = ListEvade[random.randint(0, len(ListEvade) - 1)]
            self.path_move(random_evade, C, n)
        else:
            return

    # def predict_move(self, ListAdjacency):
    #     i = random.randint(0, len(ListAdjacency[self.index]) - 1)
    #     return ListAdjacency[self.index][i][0]

# Monster object
class monster(object):
    def __init__(self, imgpath, x, y, n, t):
        print("type", t)
        temp = Image.open(imgpath)
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)
        #self.img = ImageTk.PhotoImage(Image.open(imgpath))
        up_img = Image.open("redghost_up.png")
        img2_up = up_img.resize((25, 25), Image.ANTIALIAS)
        
        down_img = Image.open("redghost_down.png")
        img2_down = down_img.resize((25, 25), Image.ANTIALIAS)
        
        self.right = img2
        self.down = img2_down
        self.left = ImageOps.mirror(img2) # Flip by horizontal
        self.up = img2_up
        self.type = t

        self.status = 0 
        self.count1 = 0
        self.count2 = 0
        self.x = x
        self.y = y
        self.index = x*n + y
        self.pic = None

        self.MoveList = []
        
    def display(self, C):
        C.delete(self.pic)
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def move(self, direction, C, n):
        if direction == "Right":
            self.x += 1
            self.index += n
            self.img = ImageTk.PhotoImage(self.right)
        elif direction == "Left":
            self.x -= 1
            self.index -= n
            self.img = ImageTk.PhotoImage(self.left)
        elif direction == "Up":
            self.y -= 1
            self.index -= 1
            self.img = ImageTk.PhotoImage(self.up)
        elif direction == "Down":
            self.y += 1
            self.index += 1
            self.img = ImageTk.PhotoImage(self.down)
        
        self.display(C)
        
    def move_around_initpos(self, C, n):
        random_move = random.choice(self.MoveList)
        
        if random_move == self.index + n:  # right
            self.move("Right", C, n)
        elif random_move == self.index - n:  # left
            self.move("Left", C, n)
        elif random_move == self.index - 1:  # up
            self.move("Up", C, n)
        elif random_move == self.index + 1:  # down
            self.move("Down", C, n)
        else: 
            random_move = self.index

        # return random_move
    
    def ghost_random_move(self, lst, C, n):
        random_list = []
        up_distance = -1
        down_distance = -1
        left_distance = -1
        right_distance = -1
        
        if lst[self.y - 1][self.x] != 1:
            up_distance = 0
            random_list.append(up_distance)
        if lst[self.y + 1][self.x] != 1:
            down_distance = 1
            random_list.append(down_distance)
        if lst[self.y][self.x - 1] != 1:
            left_distance = 2
            random_list.append(left_distance)
        if lst[self.y][self.x + 1] != 1:
            right_distance = 3
            random_list.append(right_distance)
        
        random_choose = random.choice(random_list)
        if random_choose == up_distance:
            self.move("Up", C, n)
        elif random_choose == down_distance:
            self.move("Down", C, n)
        elif random_choose == left_distance:
            self.move("Left", C, n)
        elif random_choose == right_distance:
            self.move("Right", C, n)
        return 
    
    def chase_pacman(self, lst, pacman_index, C, n):
        dist_list = []
        up_dist = -9999
        down_dist = -9999
        left_dist = -9999
        right_dist = -9999
        if lst[self.y - 1][self.x] != 1:    
            up_dist = get_manhattan_heuristic(self.index - 1, pacman_index, n)
            dist_list.append(up_dist)
            
        if lst[self.y + 1][self.x] != 1:
            down_dist = get_manhattan_heuristic(self.index + 1, pacman_index, n)
            dist_list.append(down_dist)
            
        if lst[self.y][self.x - 1] != 1:
            left_dist = get_manhattan_heuristic(self.index - n, pacman_index, n)
            dist_list.append(left_dist)
            
        if lst[self.y][self.x + 1] != 1:
            right_dist = get_manhattan_heuristic(self.index + n, pacman_index, n)
            dist_list.append(right_dist)
        
        min_dist = min(dist_list)
        if min_dist == up_dist:
            self.move("Up", C, n)
        elif min_dist == down_dist:
            self.move("Down", C, n)
        elif min_dist == left_dist:
            self.move("Left", C, n)
        elif min_dist == right_dist:
            self.move("Right", C, n)

    def chase(self, lst, pacman_index, ListAdjacency,  C, n):
        if self.type == 0:  #type 0
            if self.count1 < 3:
                self.chase_pacman(lst, pacman_index, C, n)
                self.count1 += 1
            
            elif self.count1 == 3 and self.count2 < 5:
                self.ghost_random_move(lst, C, n)
                self.count2 += 1
            
            elif self.count1 == 3 and self.count2 == 5:
                self.count1 = 0
                self.count2 = 0
                
        elif self.type == 1:    #type 1
            h = get_manhattan_heuristic(self.index, pacman_index, n)
            if h > 5:
                self.chase_pacman(lst, pacman_index, C, n)
            elif h <= 5:
                self.ghost_random_move(lst, C, n)
        
        # elif self.type == 2:    #type 2
        #     if self.count1 < 3:
        #         self.chase_pacman(lst, pacman.predict_move(ListAdjacency), C, n)
        #         self.count1 += 1
            
        #     elif self.count1 == 3 and self.count2 < 5:
        #         self.ghost_random_move(lst, C, n)
        #         self.count2 += 1
            
        #     elif self.count1 == 3 and self.count2 == 5:
        #         self.count1 = 0
        #         self.count2 = 0
        
        # elif self.type == 3:    #type 3
        #     if self.count1 < 10:
        #         if lst[self.y - 1][self.x] != 1:
        #             self.move("Up", C, n)
        #             self.count1 += 1
                    
        #     elif self.count1 < 20 and self.count1 >= 10:
        #         if lst[self.y][self.x + n] != 1:
        #             self.move("Right", C, n)
        #             self.count1 += 1
                    
        #     elif self.count1 < 30 and self.count1 >= 20:
        #         if lst[self.y + 1][self.x] != 1:
        #             self.move("Down", C, n)
        #             self.count1 += 1
            
        #     elif self.count1 < 40 and self.count1 >= 30:
        #         if lst[self.y][self.x - n] != 1:
        #             self.move("Left", C, n)
                    
        #     if self.count1 == 40:
        #         self.count1 = 0
                      
# Food object
class food(object):
    def __init__(self, x, y, n):

        # temp = Image.open(imgpath)
        # img2 = temp.resize((25, 25), Image.ANTIALIAS)
        # self.img = ImageTk.PhotoImage(img2)
        self.x = x
        self.y = y
        self.index = x*n + y

    def display(self, C):
        self.img = C.create_oval(self.x * unit + 5, self.y * unit + 5, self.x * unit + 25 - 5, self.y * unit + 25 - 5, fill = 'white')

    def destroy(self, C):
        C.delete(self.img)

    def uneatable(self, C):
        C.create_line(self.x*unit, y*unit, (self.x+1)*unit, (self.y+1)*unit, fill = "red")