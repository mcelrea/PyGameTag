import pygame #needed to import the pygame framework

#problem: pygame only tests rectangle collision, players are circles
#solution: create hidden rectangle that follows player, check that rectangle for collision


#initializes all the modules required for PyGame
pygame.init()
clock = pygame.time.Clock()

#launch a window of the desired size, screen equals a Surface which is an object
#we can perform graphical operations on. Think of a Surface as a blank piece of paper
screen = pygame.display.set_mode((1200, 900))

#variable to control the game loop, keeps our code running until we flip it to True
done = False

#player attributes (x, y, color, speed, it, reversed, score, up, down, left, right)
redPlayer = [100, 100, (255,0,0), 5, False, False, 0, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
bluePlayer = [300, 300, (0,0,255), 5, False, False, 0, pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l]
greenPlayer = [600, 600, (0,255,0), 5, False, False, 0, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

#create the maps
map1Background = [pygame.Rect(0, 0, 400, 900),
                  pygame.Rect(0, 0, 1200, 300),
                  pygame.Rect(800, 0, 400, 900),
                  pygame.Rect(0, 650, 1200, 400)]
map1Walls = [pygame.Rect(400, 300, 170, 35),
             pygame.Rect(400, 300, 35, 170),
             pygame.Rect(650, 300, 150, 35),
             pygame.Rect(765, 300, 35, 170),
             pygame.Rect(765, 550, 35, 100),
             pygame.Rect(400, 620, 400, 35),
             pygame.Rect(400, 550, 35, 100)]

def drawMap(mapBack, mapWalls):
    #draw map background
    for i in range(0,len(mapBack),1):
        pygame.draw.rect(screen, (0,0,0), mapBack[i], 0)

    #draw map walls
    for i in range(0,len(mapWalls),1):
        pygame.draw.rect(screen, (255,0,255), mapWalls[i], 0)


def checkForInput(player):
    oldx = player[0]
    oldy = player[1]

    pressed = pygame.key.get_pressed()
    #check for up key being pressed
    if pressed[player[7]]:
        player[1] -= 7
    # check for down key being pressed
    if pressed[player[8]]:
        player[1] += 7
    #check for left key being pressed
    if pressed[player[9]]:
        player[0] -= 7
    #check for right key being pressed
    if pressed[player[10]]:
        player[0] += 7

    #check for collision with walls
    collision = checkForCollision(player,map1Walls)
    if collision == True:
        player[0] = oldx
        player[1] = oldy

    #keep players on screen
    playerOffScreen = isPlayerOffScreen(player)
    if playerOffScreen == True:
        player[0] = oldx
        player[1] = oldy

def isPlayerOffScreen(player):
    if player[0] < 17:
        return True
    if player[0] > 1200-17:
        return True
    if player[1] < 17:
        return True
    if player[1] > 900-17:
        return True

    #if it hasn't gone off the screen
    return False

def checkForCollision(player, mapWalls):
    hitBox = pygame.Rect(player[0] - 17, player[1] - 17, 34, 34)
    for i in range(0, len(mapWalls), 1):
        if hitBox.colliderect(mapWalls[i]):
            return True #there was a collision

    #if we go through all the walls, and no collision
    return False

def drawPlayer(player):
    pygame.draw.circle(screen,
                       player[2],
                       (player[0], player[1]),
                       17)
    #pygame.draw.rect(screen,(255,255,255), pygame.Rect(player[0]-17, player[1]-17,34,34), 1)

#continually run the game loop until done is switch to True
while not done:

    #set the game to 60 FPS
    clock.tick(60)

    #loop through and empty the event queue, key presses, button clicks, etc.
    for event in pygame.event.get():

        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            done = True

    #check for user input
    checkForInput(redPlayer)
    checkForInput(bluePlayer)
    checkForInput(greenPlayer)

    #draw all the graphics
    drawMap(map1Background, map1Walls)
    drawPlayer(redPlayer)
    drawPlayer(greenPlayer)
    drawPlayer(bluePlayer)

    #Show any graphical updates you have made to the screen
    pygame.display.flip()