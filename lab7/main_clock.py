import pygame as p
from button import Button
import datetime

red = (255, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
black = (0, 0, 0)

p.init ()

size = (500, 500)
center = (250, 250)
screen = p.display.set_mode (size)
clock = p.time.Clock ()

button = Button (size [0] - 100, 0, 100, 50, text = "Pause")
image = p.image.load("C:\\Users\\Admin\\AppData\\Roaming\\git\\labs\\lab7\\assets\\mickeyclock.jpeg")
image = p.transform.scale(image, (600, 600))

p.mixer.music.load("C:\\Users\\Admin\\AppData\\Roaming\\git\\labs\\lab7\\assets\\sound.wav")
p.mixer.music.play()

def draw_seconds (surface, second):
    hand_length = size [0] * 0.35
    angle = second * 6
    end_x = center [0] + hand_length * p.math.Vector2 (0, -1).rotate (angle).x
    end_y = center [1] + hand_length * p.math.Vector2 (0, -1).rotate (angle).y
    p.draw.line (surface, grey, center, (end_x, end_y), 5)

def draw_minutes (surface, minute):
    hand_length = size [0] * 0.30
    angle = minute * 6
    end_x = center [0] + hand_length * p.math.Vector2 (0, -1).rotate (angle).x
    end_y = center [1] + hand_length * p.math.Vector2 (0, -1).rotate (angle).y
    p.draw.line (surface, black, center, (end_x, end_y), 5)

def draw_hours (surface, hour):
    hand_length = size [0] * 0.20
    angle = hour * 6
    end_x = center [0] + hand_length * p.math.Vector2 (0, -1).rotate (angle).x
    end_y = center [1] + hand_length * p.math.Vector2 (0, -1).rotate (angle).y
    p.draw.line (surface, red, center, (end_x, end_y), 5)

def main ():
    running = True
    pause_ = True
    tmp = [0, 0, 0]

    while (running):
        screen.fill (white)
        screen.blit(image, (-50, -50))
        now = datetime.datetime.now ()
        
        if pause_ != False:
            draw_seconds (screen, now.second)
            draw_minutes (screen, now.minute)
            draw_hours (screen, now.hour)
            p.mixer.music.unpause ()
            tmp = (now.second, now.minute, now.hour)
        else:
            draw_seconds (screen, tmp [0])
            draw_minutes (screen, tmp [1])
            draw_hours (screen, tmp [2])
            p.mixer.music.pause ()
        button.draw(screen)
        p.display.flip ()
        clock.tick (1)

        for event in p.event.get ():
            if event.type == p.QUIT:
                running = False
            if button.is_clicked(event):
                if pause_:
                    pause_ = False
                    button.text = 'PAUSE'
                else:
                    pause_ = True
                    button.text = 'UNPAUSE'
    p.quit ()

main ()
