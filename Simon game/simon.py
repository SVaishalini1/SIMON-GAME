import pygame,sys,random,time

from pygame.locals import *



WINDOWWIDTH = 600
WINDOWHEIGHT = 600

FPS = 30
BUTTONSIZE= 200
GAP =10 

FLASHDELAY = 100
TIMEOUT =5


# DECIDE THE COLORS LATER 

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(155,0,0)
PURPLE=(217,96,222)
YELLOW=(249, 248, 113)
PINK=(255, 95, 181)
ORANGE=(255, 164, 104)


XMARIGN=(WINDOWWIDTH - 2*BUTTONSIZE)/2
YMARIGN=(WINDOWHEIGHT - 2*BUTTONSIZE)/2




# Need to keep sounds 


def main():
    global DISPLAYSURF,PURPLERECT,ORANGERECT,YELLOWRECT,PINKRECT,CLOCK,BEEP1,BEEP2,BEEP3,BEEP4
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Simon game")
    CLOCK= pygame.time.Clock()

    BEEP1=pygame.mixer.Sound('beep1.ogg.mp3')
    # BEEP2=pygame.mixer.Sound('beep2.ogg')
    # BEEP3=pygame.mixer.Sound('beep3.ogg')
    # BEEP4=pygame.mixer.Sound('beep4.ogg')

    PURPLERECT=pygame.Rect(XMARIGN - GAP, YMARIGN - GAP ,BUTTONSIZE,BUTTONSIZE)
    PINKRECT=pygame.Rect(XMARIGN+BUTTONSIZE + GAP,YMARIGN - GAP,BUTTONSIZE,BUTTONSIZE)
    YELLOWRECT=pygame.Rect(XMARIGN - GAP,YMARIGN + BUTTONSIZE + GAP,BUTTONSIZE,BUTTONSIZE)
    ORANGERECT=pygame.Rect(XMARIGN + BUTTONSIZE + GAP,YMARIGN + BUTTONSIZE + GAP,BUTTONSIZE,BUTTONSIZE)

    FONT=pygame.font.Font("freesansbold.ttf",20)

    pattern=[]
    currentStep=0
    waitingorInput=False
    score=0
    lasttimeClick=0

    while True:
        SCORESURF=FONT.render("score : "+ str(score),False,BLACK)
        SCORERECT=SCORESURF.get_rect()
        SCORERECT.topleft=(WINDOWWIDTH-100,25)

        clickedButton=None
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(SCORESURF,SCORERECT)
        
        drawButtons()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                clickedButton = getButtonClicked(event.pos[0],event.pos[1])
        if not waitingorInput:
            pygame.display.update()
            pygame.time.wait(2000)
            pattern.append(random.choice((PURPLE,PINK,ORANGE,YELLOW)))
        else:
            if clickedButton and pattern[currentStep] == clickedButton:
                flashbuttonAnimation(clickedButton)
                lastTimeClick= time.time()
                currentStep+=1
                if currentStep == len(pattern):
                    currentStep=0
                    score+=1
                    waitingorInput=False
            elif (clickedButton and pattern[currentStep]!= clickedButton) or (time.time()-lastTimeClick > TIMEOUT and currentStep!=0):
                gameOverAnimation()
                currentStep=0
                pattern =[]
                score=0
                waitingorInput=False
                pygame.time.wait(5000)

                
        

            for button in pattern :
                flashbuttonAnimation(button)
                pygame.time.delay(FLASHDELAY)
            waitingorInput=True

        pygame.display.update()
        CLOCK.tick(FPS)



def drawButtons():
    pygame.draw.rect(DISPLAYSURF,PURPLE,PURPLERECT)
    pygame.draw.rect(DISPLAYSURF,PINK,PINKRECT)
    pygame.draw.rect(DISPLAYSURF,YELLOW,YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF,ORANGE,ORANGERECT)



def getButtonClicked(left,top):
    if PURPLERECT.collidepoint(left,top):
        return PURPLE
    if PINKRECT.collidepoint(left,top):
        return PINK
    if YELLOWRECT.collidepoint(left,top):
        return YELLOW
    if ORANGERECT.collidepoint(left,top):
        return ORANGE
      

def flashbuttonAnimation(color,animationSpeed=50):
    if color== PURPLE:
        rect=PURPLERECT
        flashColor=WHITE
        sound=BEEP1
    if color== PINK:
        rect=PINKRECT
        flashColor=WHITE
        sound=BEEP1
    if color== YELLOW:
        rect=YELLOWRECT
        flashColor=WHITE
        sound=BEEP1

    if color== ORANGE:
        rect=ORANGERECT
        flashColor=WHITE
        sound=BEEP1

    sound.play()
    originalSurf= DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE,BUTTONSIZE))
    flashSurf=flashSurf.convert_alpha()
    r,g,b=flashColor

    for start,end,step in ((0,255,1),(255,0,-1)):
        for alpha in range(start,end,animationSpeed * step):
            flashSurf.fill((r,g,b,alpha))
            DISPLAYSURF.blit(flashSurf,rect.topleft)
            pygame.display.update()
            CLOCK.tick(FPS)

    DISPLAYSURF.blit(originalSurf,(0,0))

def gameOverAnimation(color=RED,animationSpeed=50):
    originalSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    flashSurf=flashSurf.convert_alpha()
    r,g,b=color

    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()

    for i in range(3):
        for start , end, step in ((0,255,1),(255,0,-1)):
            for alpha in range(start,end,step * animationSpeed):
                flashSurf.fill((r,g,b,alpha))
                DISPLAYSURF.blit(originalSurf,(0,0))
                DISPLAYSURF.blit(flashSurf,(0,0))
                drawButtons()
                pygame.display.update()
                CLOCK.tick(FPS)




main()