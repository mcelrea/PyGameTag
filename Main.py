import pygame #needed to import the pygame framework
import random

#problem: pygame only tests rectangle collision, players are circles
#solution: create hidden rectangle that follows player, check that rectangle for collision


#initializes all the modules required for PyGame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
scoreFont = pygame.font.SysFont('Comic Sans MS', 20)
gameOverFont = pygame.font.SysFont('Comic Sans MS', 160)
gameStatus = "playing"

#launch a window of the desired size, screen equals a Surface which is an object
#we can perform graphical operations on. Think of a Surface as a blank piece of paper
screen = pygame.display.set_mode((1200, 900))

#variable to control the game loop, keeps our code running until we flip it to True
done = False

#speed powerup variables
speedPowerX = 0
speedPowerY = 0
speedOnScreenTime = 5000
speedOnScreenDelay = 5000
speedNextTimeOnScreen = 5000
speedPowerAlive = False
speedBoostAffectTime = 5000

#reverse powerup variables
reversePowerX = 0
reversePowerY = 0
reverseOnScreenTime = 5000
reverseOnScreenDelay = 5000
reverseNextTimeOnScreen = 5000
reversePowerAlive = False
reverseBoostAffectTime = 5000

tagDelay = 1000 #1000 = 1 second
nextTagAllowed = 1000

#                   0  1    2      3     4    5        6      7   8     9      10    11         12              13                14                 15
#player attributes (x, y, color, speed, it, reversed, score, up, down, left, right, score, hasSpeedPowerUP, timeGotSpeed, hasReversedControls, timeGotReversed)
redPlayer = [100, 100, (255,0,0), 7, False, False, 0, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, 0, False, 0, False, 0]
bluePlayer = [100, 800, (0,0,255), 7, False, False, 0, pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l, 0, False, 0, False, 0]
greenPlayer = [1050, 400, (0,255,0), 7, False, False, 0, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, 0, False, 0, False, 0]

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

def updateReversePowerUp():
    global reversePowerAlive
    global reversePowerX
    global reversePowerY
    global reverseNextTimeOnScreen
    redHitBox = pygame.Rect(redPlayer[0] - 17, redPlayer[1] - 17, 34, 34)
    blueHitBox = pygame.Rect(bluePlayer[0] - 17, bluePlayer[1] - 17, 34, 34)
    greenHitBox = pygame.Rect(greenPlayer[0] - 17, greenPlayer[1] - 17, 34, 34)
    reverseHitBox = pygame.Rect(reversePowerX, reversePowerY, 25, 25)
    if reversePowerAlive == False:
        if pygame.time.get_ticks() > reverseNextTimeOnScreen:
            reversePowerAlive = True
            reversePowerX = random.randint(0, 1150)
            reversePowerY = random.randint(0, 850)
    if reversePowerAlive == True:
        if greenHitBox.colliderect(reverseHitBox):
            redPlayer[14] = True #set that the player has a reverse boost
            redPlayer[15] = pygame.time.get_ticks() #time stamp when the player go the reverse boost
            bluePlayer[14] = True  # set that the player has a reverse boost
            bluePlayer[15] = pygame.time.get_ticks()  # time stamp when the player go the reverse boost
            reversePowerAlive = False
            reverseNextTimeOnScreen = pygame.time.get_ticks() + reverseOnScreenDelay
        elif blueHitBox.colliderect(reverseHitBox):
            redPlayer[14] = True #set that the player has a reverse boost
            redPlayer[15] = pygame.time.get_ticks() #time stamp when the player go the reverse boost
            greenPlayer[14] = True  # set that the player has a reverse boost
            greenPlayer[15] = pygame.time.get_ticks()  # time stamp when the player go the reverse boost
            reversePowerAlive = False
            reverseNextTimeOnScreen = pygame.time.get_ticks() + reverseOnScreenDelay
        elif redHitBox.colliderect(reverseHitBox):
            bluePlayer[14] = True #set that the player has a reverse boost
            bluePlayer[15] = pygame.time.get_ticks() #time stamp when the player go the reverse boost
            greenPlayer[14] = True  # set that the player has a reverse boost
            greenPlayer[15] = pygame.time.get_ticks()  # time stamp when the player go the reverse boost
            reversePowerAlive = False
            reverseNextTimeOnScreen = pygame.time.get_ticks() + reverseOnScreenDelay
        if pygame.time.get_ticks() > reverseNextTimeOnScreen+reverseOnScreenTime:
            reversePowerAlive = False
            reverseNextTimeOnScreen = pygame.time.get_ticks() + reverseOnScreenDelay

def drawReversePowerUp():
    if reversePowerAlive == True:
        pygame.draw.rect(screen, (50,255,100),
                         pygame.Rect(reversePowerX,reversePowerY,25,25))

def updateSpeedPowerUp():
    global speedPowerAlive
    global speedPowerX
    global speedPowerY
    global speedNextTimeOnScreen
    redHitBox = pygame.Rect(redPlayer[0] - 17, redPlayer[1] - 17, 34, 34)
    blueHitBox = pygame.Rect(bluePlayer[0] - 17, bluePlayer[1] - 17, 34, 34)
    greenHitBox = pygame.Rect(greenPlayer[0] - 17, greenPlayer[1] - 17, 34, 34)
    speedHitBox = pygame.Rect(speedPowerX, speedPowerY, 25, 25)
    if speedPowerAlive == False:
        if pygame.time.get_ticks() > speedNextTimeOnScreen:
            speedPowerAlive = True
            speedPowerX = random.randint(0, 1150)
            speedPowerY = random.randint(0, 850)
    if speedPowerAlive == True:
        if greenHitBox.colliderect(speedHitBox):
            greenPlayer[3] = 10 #set the increase the speed
            greenPlayer[12] = True #set that the player has a speed boost
            greenPlayer[13] = pygame.time.get_ticks() #time stamp when the player go the speed boost
            speedPowerAlive = False
            speedNextTimeOnScreen = pygame.time.get_ticks() + speedOnScreenDelay
        elif blueHitBox.colliderect(speedHitBox):
            bluePlayer[3] = 10 #set the increase the speed
            bluePlayer[12] = True #set that the player has a speed boost
            bluePlayer[13] = pygame.time.get_ticks() #time stamp when the player go the speed boost
            speedPowerAlive = False
            speedNextTimeOnScreen = pygame.time.get_ticks() + speedOnScreenDelay
        elif redHitBox.colliderect(speedHitBox):
            redPlayer[3] = 10 #set the increase the speed
            redPlayer[12] = True #set that the player has a speed boost
            redPlayer[13] = pygame.time.get_ticks() #time stamp when the player go the speed boost
            speedPowerAlive = False
            speedNextTimeOnScreen = pygame.time.get_ticks() + speedOnScreenDelay
        if pygame.time.get_ticks() > speedNextTimeOnScreen+speedOnScreenTime:
            speedPowerAlive = False
            speedNextTimeOnScreen = pygame.time.get_ticks() + speedOnScreenDelay

def drawSpeedPowerUp():
    if speedPowerAlive == True:
        pygame.draw.rect(screen, (255,255,0),
                         pygame.Rect(speedPowerX,speedPowerY,25,25))

# Create Task: Algorithm within an Algorithm
def checkForInput(player):
    oldx = player[0]
    oldy = player[1]

    pressed = pygame.key.get_pressed()
    if player[14] == False: #if they should move correctly
        #check for up key being pressed
        if pressed[player[7]]:
            player[1] -= player[3]
        # check for down key being pressed
        if pressed[player[8]]:
            player[1] += player[3]
        #check for left key being pressed
        if pressed[player[9]]:
            player[0] -= player[3]
        #check for right key being pressed
        if pressed[player[10]]:
            player[0] += player[3]
    else:
        # check for up key being pressed
        if pressed[player[7]]:
            player[1] += player[3]
        # check for down key being pressed
        if pressed[player[8]]:
            player[1] -= player[3]
        # check for left key being pressed
        if pressed[player[9]]:
            player[0] += player[3]
        # check for right key being pressed
        if pressed[player[10]]:
            player[0] -= player[3]

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


def updatePlayer(player):
    if player[12] == True: #if they have the speed boost
        if pygame.time.get_ticks() > player[13] + speedBoostAffectTime:
            player[12] = False #player no longer has speed boost
            player[3] = 7
    if player[14] == True: #if they have reversed controls
        if pygame.time.get_ticks() > player[15] + reverseBoostAffectTime:
            player[14] = False #player no longer has speed boost

def checkForTag():
    global nextTagAllowed
    if pygame.time.get_ticks() > nextTagAllowed:
        redHitBox = pygame.Rect(redPlayer[0] - 17, redPlayer[1] - 17, 34, 34)
        blueHitBox = pygame.Rect(bluePlayer[0] - 17, bluePlayer[1] - 17, 34, 34)
        greenHitBox = pygame.Rect(greenPlayer[0] - 17, greenPlayer[1] - 17, 34, 34)
        if redPlayer[4] == True:
            if redHitBox.colliderect(blueHitBox):
                bluePlayer[4] = True
                redPlayer[4] = False
                nextTagAllowed = pygame.time.get_ticks() + tagDelay
            elif redHitBox.colliderect(greenHitBox):
                greenPlayer[4] = True
                redPlayer[4] = False
                nextTagAllowed = pygame.time.get_ticks() + tagDelay
        elif bluePlayer[4] == True:
            if blueHitBox.colliderect(redHitBox):
                redPlayer[4] = True
                bluePlayer[4] = False
                nextTagAllowed = pygame.time.get_ticks() + tagDelay
            elif blueHitBox.colliderect(greenHitBox):
                greenPlayer[4] = True
                bluePlayer[4] = False
                nextTagAllowed = pygame.time.get_ticks() + tagDelay
        elif greenPlayer[4] == True:
            if greenHitBox.colliderect(blueHitBox):
                bluePlayer[4] = True
                greenPlayer[4] = False
                nextTagAllowed = pygame.time.get_ticks() + tagDelay
            elif greenHitBox.colliderect(redHitBox):
                redPlayer[4] = True
                greenPlayer[4] = False
                nextTagAllowed = pygame.time.get_ticks() + tagDelay




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
    if player[4] == False:
        pygame.draw.circle(screen,
                           player[2],
                           (player[0], player[1]),
                           17)
    else:
        pygame.draw.circle(screen,
                           (255,255,255),
                           (player[0], player[1]),
                           17)
    #pygame.draw.rect(screen,(255,255,255), pygame.Rect(player[0]-17, player[1]-17,34,34), 1)

def chooseIt():
    #randomly decide who is it BEFORE the game starts
    whoIsIt = random.randint(0,2) #0,1,2
    if whoIsIt == 0:
        redPlayer[4] = True
    elif whoIsIt == 1:
        greenPlayer[4] = True
    elif whoIsIt == 2:
        bluePlayer[4] = True

def updateScore():
    if redPlayer[4] == True:
        redPlayer[11] += 1
    elif greenPlayer[4] == True:
        greenPlayer[11] += 1
    elif bluePlayer[4] == True:
        bluePlayer[11] += 1

def drawScore():
    textSurface = scoreFont.render("Red Score: " + str(redPlayer[11]),
                                   False,
                                   (255,0,0))
    screen.blit(textSurface, (10, 10))

    textSurface = scoreFont.render("Green Score: " + str(greenPlayer[11]),
                                   False,
                                   (0, 255, 0))
    screen.blit(textSurface, (580, 10))

    textSurface = scoreFont.render("Blue Score: " + str(bluePlayer[11]),
                                   False,
                                   (0, 0, 255))
    screen.blit(textSurface, (1000, 10))

chooseIt()
#continually run the game loop until done is switch to True
while not done:

    #set the game to 60 FPS
    clock.tick(60)

    #loop through and empty the event queue, key presses, button clicks, etc.
    for event in pygame.event.get():

        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameStatus == "gameOver":
                    redPlayer[11] = 0
                    redPlayer[0] = 100
                    redPlayer[1] = 100
                    redPlayer[4] = False
                    bluePlayer[11] = 0
                    bluePlayer[0] = 100
                    bluePlayer[1] = 800
                    bluePlayer[4] = False
                    greenPlayer[11] = 0
                    greenPlayer[0] = 1050
                    greenPlayer[1] = 400
                    greenPlayer[4] = False
                    redPlayer[3] = 7
                    redPlayer[12] = False
                    bluePlayer[3] = 7
                    bluePlayer[12] = False
                    greenPlayer[3] = 7
                    greenPlayer[12] = False
                    chooseIt()
                    gameStatus = "playing"

    if gameStatus == "playing":
        #check for user input
        checkForInput(redPlayer)
        checkForInput(bluePlayer)
        checkForInput(greenPlayer)

        checkForTag()
        updateScore()
        updateSpeedPowerUp()
        updateReversePowerUp()
        updatePlayer(redPlayer)
        updatePlayer(bluePlayer)
        updatePlayer(greenPlayer)

        #draw all the graphics
        drawMap(map1Background, map1Walls)
        drawSpeedPowerUp()
        drawReversePowerUp()
        drawPlayer(redPlayer)
        drawPlayer(greenPlayer)
        drawPlayer(bluePlayer)
        drawScore()

        if redPlayer[11] >= 3000 or bluePlayer[11] >= 3000 or greenPlayer[11] >= 3000:
            gameStatus = "gameOver"

    if gameStatus == "gameOver":
        if redPlayer[11] < bluePlayer[11] and redPlayer[11] < greenPlayer[11]:
            textSurface = gameOverFont.render("Red Player Wins",
                                           False,
                                           (255, 0, 0))
            screen.blit(textSurface, (100, 100))
        elif bluePlayer[11] < redPlayer[11] and bluePlayer[11] < greenPlayer[11]:
            textSurface = gameOverFont.render("Blue Player Wins",
                                           False,
                                           (0, 0, 255))
            screen.blit(textSurface, (100, 100))
        elif greenPlayer[11] < redPlayer[11] and greenPlayer[11] < bluePlayer[11]:
            textSurface = gameOverFont.render("Green Player Wins",
                                           False,
                                           (0, 255, 0))
            screen.blit(textSurface, (100, 100))

    #Show any graphical updates you have made to the screen
    pygame.display.flip()