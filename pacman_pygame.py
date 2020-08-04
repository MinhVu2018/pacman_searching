import pygame

def drawPacman(screen, x, y):
    pacmanImg = pygame.image.load("pacman.png")
    screen.blit(pacmanImg, (x, y))
    
def drawBlueMonster(screen, x, y):
    bluemonsterImg = pygame.image.load("blueghost.png")
    screen.blit(bluemonsterImg, (x, y))
    
def drawRedMonster(screen, x, y):
    redmonsterImg = pygame.image.load("redghost.png")
    screen.blit(redmonsterImg, (x, y))

def drawDot(screen, x, y):
    dotImg = pygame.image.load("dot.png")
    screen.blit(dotImg, (x, y))

def main():
    UserInput = "pacmanmaze.txt"	#input("Enter input file: ")
    lst = []
    f = open(UserInput, "r")

    for v in f.readlines():
        v = v.strip().split(' ')
        v = [int(i) for i in v]
        lst.append(v)
    
    #Get row and column of maze and Pacman's position
    maze_row = lst[0][0]
    maze_col = lst[0][1]
    
    pacman_row = lst[-1][0]
    pacman_col = lst[-1][1]
    
    lst.pop(0)
    
    ## Init pygame
    width = 1000
    height = 800
    tile_size = 32
    
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    
    pygame.init()
    screen = pygame.display.set_mode((width, height), 0, 32) #pygame.display.set_mode(resolution=(w,h), flags=0, depth=32)
    
    pygame.display.set_icon(pygame.image.load("pacmanlogo32.png"))
    pygame.display.set_caption("Pacman Search")
    screen.fill(BLACK) # White screen
    
    check_redg = 0
    
    for i in range(maze_row):
        for j in range(maze_col):
            if lst[i][j] == 1:
                pygame.draw.rect(screen, BLUE, (j * tile_size, i * tile_size, tile_size, tile_size))
            elif (i , j) == (pacman_row, pacman_col):
                drawPacman(screen, j * tile_size, i * tile_size)
            elif lst[i][j] == 3:
                if check_redg == 0:
                    drawRedMonster(screen, j * tile_size, i * tile_size)
                    check_redg = 1
                else:
                    drawBlueMonster(screen, j * tile_size, i * tile_size)
                    check_redg = 0
            else:
                drawDot(screen, j * tile_size, i * tile_size)
                
   
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()