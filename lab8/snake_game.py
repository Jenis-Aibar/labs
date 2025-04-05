from random import randint
import pygame
import sys
import time

pygame.init ()
pygame.mixer.init()

apple_sound = pygame.mixer.Sound("labs\\lab8\\assets\\sound\\snake_apple.mp3")
apple_sound.play 
death_count = 0
max_point = 0
mass_list = [5, 10, 15] # Список размеров яблока
apple_time = 3 # Время для большого яблока

def generate_apple (snake_body): # Генерация случайных яблок c разным весом
    mass_index = randint (0, 2)
    while True:
        apple_pos = (randint (1, 23) * 20, randint (6, 29) * 20)
        if apple_pos not in snake_body:
            return (apple_pos, mass_list [mass_index])
def collide_apple (apple_pos, cell_size, snake_pos): # Проверка задел ли игрок яблоку
    if apple_pos [0] - cell_size / 4 <= snake_pos [0] + cell_size / 2 <= apple_pos [0] + cell_size / 4:
        if apple_pos [1] - cell_size / 4 <= snake_pos [1] + cell_size / 2 <= apple_pos [1] + cell_size / 4:
            return True
    return False
def collide_snake (snake_pos, map_01): # Проверяет по матрице было ли столкновение об себя
    convert_snake_pos = ((snake_pos [1] - 110) // 20, (snake_pos [0] - 10) // 20)
    if map_01 [convert_snake_pos[0]][convert_snake_pos[1]]:
        return True
    return False

def start ():
    global death_count, max_point # Неменяемые при смерти данные

    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    grey = (128, 128, 128)

    width, heigth = 500, 700
    wall_sizeX = 10
    cell_size = 20
    fps = 10
    flag = False
    level_type = "easy"
    font = pygame.font.Font(None, 50)
    scorepoint = 0

    map_01 = []

    for i in range (26):
        map_01.append ([0] * 26)

    snake_pos = [50, 10]
    snake_body = [[50, 10], [30, 10]]
    apple_size = cell_size / 2
    apple_pos = (randint (1, 23) * 20, randint (6, 29) * 20) # Спавн яблок в границах игровой карты

    direction = "RIGHT"
    change_to = direction
    running = True

    screen = pygame.display.set_mode ((width, heigth))
    pygame.display.set_caption ("Snake Pro")

    clock = pygame.time.Clock ()
    while running:
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
        direction = change_to
        if direction == "UP":
            snake_pos [1] -= cell_size
        elif direction == "DOWN":
            snake_pos [1] += cell_size
        elif direction == "LEFT":
            snake_pos [0] -= cell_size
        elif direction == "RIGHT":
            snake_pos [0] += cell_size
        
        if snake_pos[0] < 10:
            snake_pos[0] = 10 + 480 - cell_size
        elif snake_pos[0] >= 10 + 480:
            snake_pos[0] = 10
        elif snake_pos[1] < 110:
            snake_pos[1] = 110 + 480 - cell_size
        elif snake_pos[1] >= 110 + 480:
            snake_pos[1] = 110

        snake_body.insert (0, list (snake_pos))

        if collide_apple (apple_pos, cell_size, snake_pos):
            apple_sound.play ()
            snake_body.insert (0, list (apple_pos)) # Добавляем 1 блок к длине змей
            scorepoint += apple_size / 10 * 2 + 1
            apple_pos, apple_size = generate_apple (snake_body)

            if (apple_size == 20):
                flag = True
                start_time = time.time() # Запускаем таймер (жизнь яблока)
        else:
            map_01 [(snake_body [-1][1] - 110) // 20][(snake_body [-1][0] - 10) // 20] = 0 # Матрица хранит где находится части тела змей
            snake_body.pop()

        if flag:
            if time.time() - start_time > apple_time: # Проверка жизни яблока
                apple_pos, apple_size = generate_apple (snake_body)
                flag = False
        
        # Уровень сложности
        if len (snake_body) - 2 >= 20:
            level_type = "hard"
            fps = 20
        elif len (snake_body) - 2 >= 10:
            level_type = "normal"
            fps = 15

        # Проверка столкновение змей об себя
        if collide_snake (snake_pos, map_01):
            death_count += 1
            max_point = max (max_point, scorepoint)
            return True

        screen.fill (black)
        pygame.draw.rect (screen, grey,(8, 108, 484, 484)) # Серая граница
        pygame.draw.rect (screen, black, (10, 110, 480, 480)) # Пустота внутри серой границы
        for block in snake_body:
            pygame.draw.rect (screen, green, pygame.Rect (block [0] + 1, block [1] + 1, cell_size - 1, cell_size - 1)) # Части змей
            map_01 [(block [1] - 110) // 20][(block [0] - 10) // 20] = 1
        pygame.draw.circle (screen, red, apple_pos, apple_size) # Яблоко

        # Фоновые прямоугольники для текста
        pygame.draw.rect (screen, grey, (8, 592 + 10, 220, 45))  
        pygame.draw.rect (screen, grey, (8, 592 + 45 + 15, 220, 45))
        pygame.draw.rect (screen, grey, (492 - 220, 590 + 10, 220, 45))
        pygame.draw.rect (screen, grey, (492 - 220, 590 + 45 + 15, 220, 45)) #490 590

        # Надписи о очках, уровня сложности, рекордах, смертей
        score = font.render(f"Score:   {scorepoint}", True, white)
        screen.blit(score, (8 + 10, 602 + 7))
        level_text = font.render(f"Level:  {level_type}", True, green)
        screen.blit(level_text, (8 + 10, 592 + 45 + 15 + 7))
        deaths = font.render(f"Death:   {death_count}", True, red)
        screen.blit(deaths, (492 - 220 + 10, 590 + 10 + 7))
        best = font.render(f"Best:   {max_point}", True, white)
        screen.blit(best, (492 - 220 + 10, 590 + 45 + 15 + 7))

        pygame.display.flip ()
        clock.tick (fps)
    return False


while True: # Повторяет до тех пор пока функция не вернет лож

    if not start ():
        break
pygame.quit ()
sys.exit ()
