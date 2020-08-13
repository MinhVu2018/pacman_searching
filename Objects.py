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
        while True:
            i = random.randint(0, len(ListAdjacency[self.index]) - 1)
            tile = ListAdjacency[self.index][i][0]
            if get_manhattan_heuristic(tile, ghost.index, n) >= 2:
                self.path_move(tile, C, n)
                return

    def predict_move(self, ListAdjacency):
        i = random.randint(0, len(ListAdjacency[self.index]) - 1)
        return ListAdjacency[self.index][i][0]

# Monster object
class monster(object):
    def __init__(self, imgpath, x, y, n, t):
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

        # type = status0 -> status1 -> status0 ... 
        # use 1 count var ok ????????
        # type 0: 3 chase -> 5 rand -> 3chase ...
        # type 1: heur > 5 then chase -> heur <= 5 rand -> ...  
        # type 2: type0 but can predict pacman position (use pacman.predict_move())
        # type 3: 10 up -> 10 right -> 10 down -> 10 left

        self.status = 0 
        self.count = 0
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

    def chase_pacman(self, lst, pacman, C, n):
        dist_list = []
        up_dist = -9999
        down_dist = -9999
        left_dist = -9999
        right_dist = -9999
        if lst[self.y - 1][self.x] != 1:    
            up_dist = get_manhattan_heuristic(self.index - 1, pacman.index, n)
            dist_list.append(up_dist)
            
        if lst[self.y + 1][self.x] != 1:
            down_dist = get_manhattan_heuristic(self.index + 1, pacman.index, n)
            dist_list.append(down_dist)
            
        if lst[self.y][self.x - 1] != 1:
            left_dist = get_manhattan_heuristic(self.index - n, pacman.index, n)
            dist_list.append(left_dist)
            
        if lst[self.y][self.x + 1] != 1:
            right_dist = get_manhattan_heuristic(self.index + n, pacman.index, n)
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
