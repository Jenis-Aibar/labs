import pygame 
import time
import math
from button import Button
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.display.set_caption("MICKEY MOUSE CLOCK") 

left = pygame.image.load(r"C:\\Users\\Admin\\AppData\\Roaming\\git\\labs\\lab7\\assets\\leftarm.png")
right = pygame.image.load(r"C:\\Users\\Admin\\AppData\\Roaming\\git\\labs\\lab7\\assets\\rightarm.png")
main = pygame.transform.scale(pygame.image.load(r"C:\\Users\\Admin\\AppData\\Roaming\\git\\labs\\lab7\\assets\\clock.png"), (800, 600))

pygame.mixer.music.load("C:\\Users\\Admin\\AppData\\Roaming\\git\\labs\\lab7\\assets\\sound.wav")
pygame.mixer.music.play()

button = Button (800 - 100, 0, 100, 50, text = "Pause")
running = True
ping = 0
pause = False
start_time = time.time ()   
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if button.is_clicked (event):
            pause = not pause
            if pause:
                pygame.mixer.music.stop ()
                button.text = "RESUME"
                pause_start = time.time()
            else:
                pygame.mixer.music.play()
                button.text = "PAUSE"
                ping += time.time() - pause_start
    if not pause:
        elapsed = time.time() - start_time - ping
        t = time.localtime(start_time + elapsed)
        minute = t.tm_min
        second = t.tm_sec
        
        minute_angle = minute * 6    + (second / 60) * 6  #қазіргі минут * 360 градус / 60 минут + қазіргі секундты қосамыз 
        second_angle = second * 6  
        
        screen.blit(main, (0,0))  #основаға суретті орналастыру
        
        rotated_rightarm = pygame.transform.rotate(pygame.transform.scale(right, (800, 600)), -minute_angle) #оң қол минутты орналастыру
        rightarmrect = rotated_rightarm.get_rect(center=(800 // 2 - 30, 600 // 2 - 15))
        screen.blit(rotated_rightarm, rightarmrect)

        rotated_leftarm = pygame.transform.rotate(pygame.transform.scale(left, (40.95, 682.5)), -second_angle) #сол қол секундты орналастыру
        leftarmrect = rotated_leftarm.get_rect(center=(800 // 2 + 20, 600 // 2 - 18))
        screen.blit(rotated_leftarm, leftarmrect)
    
    button.draw(screen)
    pygame.display.flip() 
    clock.tick(60) 
    
pygame.quit()