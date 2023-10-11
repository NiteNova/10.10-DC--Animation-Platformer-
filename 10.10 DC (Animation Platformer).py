import pygame
import random
from pygame.math import Vector2
from pygame.rect import Rect


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)


# pygame init:
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Animation Platformer")

Link = pygame.image.load('link.png') #load your spritesheet
Link.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)


# definitions:      
class platform():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos 

    def draw(self):
        pygame.draw.rect(screen, (100, 50, 100), (self.xpos, self.ypos, 80, 30))
    
    def move(self, delta):
        pass

class MovingBlock(platform):
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.startX = self.xpos
        self.startY = self.ypos
        self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, (200, 50, 100), (self.xpos, self.ypos, 80, 30))

    def move(self, delta):
        if self.direction == 1:
            if self.xpos < self.startX:
                self.direction*= -1
            else:
                self.xpos-=100 * delta
        else:
            if self.xpos > self.startX+200:
                self.direction *= -1
            else:
                self.xpos+=100 * delta


def main():
    # game setup:
    clock = pygame.time.Clock()


    Link = pygame.image.load('link.png') #load your spritesheet
    Link.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)    

    xpos = 500 #xpos of player
    ypos = 200 #ypos of player
    vx = 0 #x velocity of player
    vy = 0
    isOnGround = False

    LEFT = 0
    RIGHT = 1
    UP = 2
    keys = [False, False, False, False]
    

    amt_platform = []
    for i in range(2):
        amt_platform.append(platform(random.randrange(50, 700), random.randrange(50, 700)))
        amt_platform.append(MovingBlock(random.randrange(50, 500), random.randrange(50, 500)))

    #animation variables variables
    frameWidth = 16
    frameHeight = 24
    RowNum = 0 #for left animation, this will need to change for other animations
    frameNum = 0
    ticker = 0
    flipped = False

    # main loop:
    running = True
    while running:
        delta = clock.tick(FRAMERATE) / 1000

        # input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: #keyboard input
                if event.key == pygame.K_LEFT:
                    keys[LEFT]=True
                elif event.key == pygame.K_RIGHT:
                    keys[RIGHT]=True
                elif event.key == pygame.K_UP:
                    keys[UP]=True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys[LEFT]=False
                elif event.key == pygame.K_RIGHT:
                    keys[RIGHT]=False
                elif event.key == pygame.K_UP:
                    keys[UP]=False

        

        #PLAYER LEFT MOVEMENT
        if keys[LEFT]==True:
            vx=-4
            flipped = False
        #PLAYER RIGHT MOVEMENT
        elif keys[RIGHT] == True:
            vx = 4
            flipped = True
        #turn off velocity when stop movement
        else:
            vx = 0
        #PLAYER JUMP MOVEMENT
        if keys[UP] == True and isOnGround == True: #only jump when on the ground
            vy = -20
            isOnGround = False
        if ypos > 752:
            isOnGround = True
            vy = 0
            ypos = 752
        #GRAVITY
        if isOnGround == False:
            vy += .8

        #Update Position
        xpos += vx
        ypos += vy

        #PLATFORM EFFECTS------------------------------------------------------------
        for i in range(len(amt_platform)):
            amt_platform[i].move(delta)

        #ANIMATION-------------------------------------------------------------------
        
        # Update Animation Information
        # Only animate when in motion

        #VERTICAL ANIMATION
        if vy > 0: #DOWN ANIMATION
            RowNum = 0
            ticker += 1
            if ticker % 10 == 0:
                frameNum += 1
            if frameNum > 7:
                frameNum = 0
        elif vy < 0: #UP ANIMATION
            RowNum = 1
            ticker+=1
            if ticker%10==0: 
                frameNum+=1
            if frameNum>7: 
                frameNum = 0

        #HORIZONTAL ANIMATION <----->
        if vx < 0: #LEFT ANIMATION
            RowNum = 2
            ticker+=1
            if ticker%10==0: 
                frameNum+=1
            if frameNum>7: 
                frameNum = 0
        elif vx > 0: #RIGHT ANIMATION
            RowNum = 2
            ticker += 1
            if ticker % 10 == 0:
                frameNum += 1
            if frameNum > 7:
                frameNum = 0
        


        # draw:
        screen.fill("#000000")
        
        screen.fill((0,0,0)) #wipe screen so it doesn't smear
        scale = pygame.transform.scale_by(Link.subsurface((frameWidth+16)*frameNum + 16, RowNum*(frameHeight+8) + 24, frameWidth, frameHeight), 2)
        flip = pygame.transform.flip(scale, flip_x = True, flip_y = False)
        if flipped == True:
            draw = flip
        else:
            draw = scale
        screen.blit(draw, (xpos, ypos))

        for i in range(len(amt_platform)):
            amt_platform[i].draw()

         
        pygame.display.flip()

if __name__ == "__main__":
    main()