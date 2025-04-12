#Imports
import pygame, sys
from pygame.locals import *
import random, time
 
#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED_ENEMY = 5
SPEED_COIN = 3
SCORE = 0
COINS = 0
LEVEL = "easy"
N = 10

COIN_TYPES = [(20, 20, 1), (30, 30, 2), (40, 40, 4)]

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("labs\lab8\\assets\sprites\\bg.jpg")
background = pygame.transform.scale (background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("labs\lab8\\assets\sprites\\red.png").convert_alpha ()
        self.image = pygame.transform.scale (self.image,  (45, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED_ENEMY)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.create ()

      def create(self):
        self.image = pygame.image.load("labs\lab8\\assets\sprites\\coin.png").convert_alpha ()
        self.current_type = random.randint(0, 2)
        self.image = pygame.transform.scale(self.image, COIN_TYPES[self.current_type][:2])
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

      def move(self):
        global COINS
        self.rect.move_ip(0, SPEED_COIN)
        
        if (self.rect.top > 600):
            self.create ()
        if pygame.sprite.collide_rect(P1, self):
            pygame.mixer.Sound('labs\\lab8\\assets\\sound\\money3.mp3').play()
            COINS += COIN_TYPES[self.current_type][2]
            self.create ()
            self.rect.top = 0
    
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("labs\lab8\\assets\sprites\\blue.png").convert_alpha ()
        self.image = pygame.transform.scale (self.image, (45, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin ()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED_ENEMY += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    coins = font_small.render(str(COINS), True, YELLOW)
    level = font_small.render(str(LEVEL), True, GREEN)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coins, (SCREEN_WIDTH - 30,10))
    DISPLAYSURF.blit(level, (SCREEN_WIDTH // 2 + 105,10))
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('labs\lab8\\assets\sound\crash.mp3').play()   
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()
    if COINS > N:
        LEVEL = "hard"
        SPEED_ENEMY += 2
        N = 999999  
        
    pygame.display.update()
    FramePerSec.tick(FPS)