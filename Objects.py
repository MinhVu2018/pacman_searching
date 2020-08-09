from PIL import ImageTk, Image
import time
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
        self.speed = 0.5
        
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

    def path_move(self, path, C, n, tkinter):

        for i in path:

            if i == self.index + n:  # right
                self.key_move("Right", C, n)
                time.sleep(self.speed)
                tkinter.update()
            elif i == self.index - n:  # left
                self.key_move("Left", C, n)
                time.sleep(self.speed)
                tkinter.update()
            elif i == self.index - 1:  # up
                self.key_move("Up", C, n)
                time.sleep(self.speed)
                tkinter.update()
            elif i == self.index + 1:  # down
                self.key_move("Down", C, n)
                time.sleep(self.speed)
                tkinter.update()
            # else is == 

# Monster object
class monster(object):
    def __init__(self, imgpath, x, y, n, lv):
        temp = Image.open(imgpath)
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)
        #self.img = ImageTk.PhotoImage(Image.open(imgpath))
        self.x = x
        self.y = y
        self.index = x*n + y
        self.pic = None
        self.lv = lv
    def display(self, C):
        C.delete(self.pic)
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

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
