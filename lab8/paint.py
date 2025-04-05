import pygame
import math
import time

active_figures = []
nonactive_figures = []
points = [] # Фигуры кистя
tmp = (0, 0) # Последняя сохраненная позиция курсора внутри окна

def fix_position (position, start_pos, radius): # Следит за курсором и не дает рисовать вне окна
    if radius:
        if position [1] < 100 + radius:
            position = (position [0], 100 + radius)
        elif position [0] < radius:
            position = ( radius, position [1])
        elif position [1] > 480 - radius:
            position = (position [0], 480 - radius)
        elif position [0] > 640 - radius:
            position = (640 - radius, position [1])
    elif start_pos is not None:
        if position [1] <= 0:
            position = (position [0], 0)
        if position [0] <= 0:
            position = ( 0, position [1])
        if position [1] >= 480:
            position = (position [0], 480)
        if position [0] >= 640:
            position = (640, position [1])
    tmp = position
    return position
def clear_global_data (): # Удаляет все запланированные к рисовке фигуры

    global active_figures, points
    active_figures = []
    points = []
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    

    canvas = pygame.Surface((640, 480)) # Для оптимизаций, я не хотел чтобы фигуры хранились в одной переменной, а канвас работает по другому, он рисует все фигуры как 'один слой'
    canvas.fill((255, 255, 255))
    radius = 15 # Толщина кистя и ластика
    x = 0
    y = 0

    mode = (0, 0, 255)
    
    drawing = False 
    start_pos = None
    tool = "brush"
    
    buttons = [ # Все кнопки в меню окна
            {"label": "rect", "pos": (10, 10), "size": (60, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},
            {"label": "brush", "pos": (80, 10), "size": (60, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},
            {"label": "circle", "pos": (150, 10), "size": (60, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},
            
            {"label": "square", "pos": (10, 45), "size": (60, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},
            {"label": "right triangle", "pos": (80, 45), "size": (130, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},
            {"label": "equilateral triangle", "pos": (215, 45), "size": (150, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},
            {"label": "rombus", "pos": (370, 45), "size": (75, 30), "color": (128, 128, 128), "fontcolor": (0, 0, 0)},

            {"label": "red", "pos": (220, 10), "size": (60, 30), "color": (255, 0, 0), "fontcolor": (0, 0, 0)},
            {"label": "green", "pos": (290, 10), "size": (60, 30), "color": (0, 255, 0), "fontcolor": (0, 0, 0)},
            {"label": "blue", "pos": (360, 10), "size": (60, 30), "color": (0, 0, 255), "fontcolor": (0, 0, 0)},
            {"label": "erase", "pos": (450, 10), "size": (60, 30), "color": (0, 0, 0), "fontcolor": (255, 255, 255)},
            {"label": "clear", "pos": (515, 10), "size": (60, 30), "color": (0, 0, 0), "fontcolor": (255, 255, 255)},
            {"label": "+", "pos": (450, 45), "size": (30, 30), "color": (0, 0, 0), "fontcolor": (255, 255, 255)},
            {"label": "-", "pos": (485, 45), "size": (30, 30), "color": (0, 0, 0), "fontcolor": (255, 255, 255)}
        ]

    while True:
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                if event.key == pygame.K_r:
                    mode = (255, 0, 0)
                elif event.key == pygame.K_g:
                    mode = (0, 255, 0)
                elif event.key == pygame.K_b:
                    mode = (0, 0, 255)
                
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    radius = min(200, radius + 1)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONDOWN: # Если не кисть, то первый клик установливает центральную точку, затем вторая фиксирует по этим двум точкам фигуру
                position = event.pos
                if 100 < position[1]: # Было ли нажатие внутри меню
                    if event.button == 1:
                        if tool == "brush":
                            drawing = True
                        elif tool == "rect" and start_pos is None:
                            start_pos = event.pos
                            drawing = True
                        elif tool == "rect" and start_pos is not None:
                            current_shape = (start_pos, event.pos, mode)
                            active_figures.append(current_shape)
                            start_pos = None
                            drawing = False
                        elif tool == "circle" and start_pos is None:
                            start_pos = event.pos
                            drawing = True
                        elif tool == "circle" and start_pos is not None:
                            current_circle = (start_pos, event.pos, mode, "circle")
                            active_figures.append(current_circle)
                            start_pos = None
                            drawing = False
                        elif tool == "square":
                            if start_pos is None:
                                start_pos = event.pos
                                drawing = True
                            else:
                                current_square = (event.pos, mode, "square", start_pos)
                                active_figures.append(current_square)
                                start_pos = None
                                drawing = False
                        elif tool == "right triangle":
                            if start_pos is None:
                                start_pos = event.pos
                                drawing = True
                            else:
                                try:
                                    position = fix_position (event.pos, start_pos, 0)
                                except:
                                    position = tmp
                                position = (position, mode, "right triangle", start_pos)
                                nonactive_figures.append (position)
                                start_pos = None
                                drawing = False
                        elif tool == "equilateral triangle":
                            if start_pos is None:
                                start_pos = event.pos
                                drawing = True
                            else:
                                try:
                                    position = fix_position (event.pos, start_pos, 0)
                                except:
                                    position = tmp
                                position = (position, mode, "equilateral triangle", start_pos)
                                nonactive_figures.append (position)
                                start_pos = None
                                drawing = False
                        elif tool == "rombus":
                            if start_pos is None:
                                start_pos = event.pos
                                drawing = True
                            else:
                                try:
                                    position = fix_position (event.pos, start_pos, 0)
                                except:
                                    position = tmp
                                position = (position, mode, "rombus", start_pos)
                                nonactive_figures.append (position)
                                start_pos = None
                                drawing = False

                
                else: # Нажата ли один из кнопок
                    for button in buttons:
                        if button["pos"][0] <= position[0] <= button["pos"][0] + button["size"][0] and \
                           button["pos"][1] <= position[1] <= button["pos"][1] + button["size"][1]:
                            start_pos = None
                            if button["label"] == "rect":
                                tool = 'rect'
                            elif button["label"] == "brush":
                                tool = 'brush'
                            elif button["label"] == "circle":
                                tool = 'circle'
                            elif button["label"] == "square":
                                tool = 'square'
                            elif button["label"] == "right triangle":
                                tool = 'right triangle'
                            elif button["label"] == "equilateral triangle":
                                tool = 'equilateral triangle'
                            elif button["label"] == "rombus":
                                tool = 'rombus'
                            elif button["label"] == "red":
                                mode = (255, 0, 0)
                            elif button["label"] == "blue":
                                mode = (0, 0, 255)
                            elif button["label"] == "green":
                                mode = (0, 255, 0)
                            elif button["label"] == "erase":
                                mode = (255, 255, 255)
                                tool = "brush"
                            elif button["label"] == "clear":
                                canvas.fill((255, 255, 255))
                                clear_global_data ()
                            elif button["label"] == "+":
                                radius += 5
                            elif button["label"] == "-":
                                radius -= 5
            if event.type == pygame.MOUSEBUTTONUP: # Пока не подняли кнопку ЛКМ и если кисть то продолжаем рисовать
                if event.button == 1:
                    if tool == "brush":
                        drawing = False
                        points.clear ()
            
            if event.type == pygame.MOUSEMOTION and drawing:
                position = fix_position (event.pos, start_pos, radius)
                if tool == "brush":
                    position = (position, mode)
                    points.append(position)

            if drawing and tool != "brush":
                try:
                    position = fix_position (event.pos, start_pos, 0)
                except:
                    position = tmp
                if tool == "rect":
                    position = (position, mode)
                    nonactive_figures.append(position)
                if tool == "circle":
                    position = (position, mode, "circle")
                    nonactive_figures.append (position)
                if tool == "square":
                    position = (position, mode, "square")
                    nonactive_figures.append (position)
                if tool == "right triangle":
                    position = (position, mode, "right triangle")
                    nonactive_figures.append (position)
                if tool == "equilateral triangle":
                    position = (position, mode, "equilateral triangle")
                    nonactive_figures.append (position)
                if tool == "rombus":
                    position = (position, mode, "rombus")
                    nonactive_figures.append (position)

        screen.fill((255, 255, 255))
        i = 0
        while i < len(points) - 1: # Сглаживание между позициями мышки, и отправка кругов в active_figures
            drawLineBetween(canvas, i, points[i][0], points[i + 1][0], radius, points[i][1])
            i += 1

        for block in active_figures: # Проверяем какую фигуру надо рисовать
            if len (block) == 3: 
                width = block[1][0] - block[0][0]
                height = block[1][1] - block[0][1]
                pygame.draw.rect(canvas, block[2], pygame.Rect(block[0][0], block[0][1], width, height))
            elif block [2] == "square":
                start_pos_ = block [3]
                r = math.sqrt (pow (start_pos_ [0] - block [0][0], 2) + pow (start_pos_ [1] - block [0][1], 2))
                pygame.draw.rect (canvas, block [1], pygame.Rect (start_pos_ [0] - r, start_pos_ [1] - r, 2 * r, 2 * r))
            elif block [3] == "brush_process":
                pygame.draw.circle (canvas, block [1], block [0], block [2])
            else:
                r = math.sqrt (pow (block [1][0] - block [0][0], 2) + pow (block [1][1] - block [0][1], 2))
                pygame.draw.circle(canvas, block [2], block [0], r)
        if drawing:
            for block in nonactive_figures: # Планируется к рисовке
                if len (block) == 2:
                    width = block[0][0] - start_pos[0]
                    height = block[0][1] - start_pos[1]
                    pygame.draw.rect(canvas, block[1], pygame.Rect(start_pos[0], start_pos[1], width, height))
                elif block [2] == "square":
                    r = math.sqrt (pow (start_pos [0] - block [0][0], 2) + pow (start_pos [1] - block [0][1], 2))
                    pygame.draw.rect (canvas, block [1], pygame.Rect (start_pos [0] - r, start_pos [1] - r, 2 * r, 2 * r))
                elif block [2] == "right triangle":
                    r = math.dist(start_pos, block [0])
                    p1 = start_pos
                    p2 = (start_pos [0], block [0][1])
                    p3 = block [0]
                    pygame.draw.polygon(canvas, block [1], (p1, p2, p3))
                elif block [2] == "equilateral triangle":
                    r = math.dist(start_pos, block [0])
                    x, y = start_pos
                    p1 = (x, y - r)
                    p2 = (x - r * math.sin(math.pi / 3), y + r / 2) 
                    p3 = (x + r * math.sin(math.pi / 3), y + r / 2)
                    pygame.draw.polygon(canvas, block [1], (p1, p2, p3))
                elif block [2] == "rombus":
                    r = math.dist (start_pos, block [0])
                    cx, cy = start_pos
                    top = (cx, cy - r)
                    bottom = (cx, cy + r)
                    left = (cx - r, cy)
                    right = (cx + r, cy)
                    pygame.draw.polygon(canvas, block [1], [top, right, bottom, left])
                else:
                    r = math.sqrt (pow (start_pos [0] - block [0][0], 2) + pow (start_pos [1] - block [0][1], 2))
                    pygame.draw.circle(canvas, block [1],  start_pos, r)
        else:
            nonactive_figures.clear ()
        active_figures.clear () # Чистка фигур, поскольку они уже на канвасе
        try:
            nonactive_figures.pop()
        except:
            pass
        # Меню кнопок
        pygame.draw.rect(canvas, (110, 110, 110), pygame.Rect(0, 0, 640, 100))
        for button in buttons:
            pygame.draw.rect(canvas, button["color"], pygame.Rect(button["pos"], button["size"]))
            font = pygame.font.SysFont("Arial", 20)
            text_surface = font.render(button["label"], True, button["fontcolor"])
            canvas.blit(text_surface, (button["pos"][0] + 10, button["pos"][1] + 5))
        screen.blit(canvas, (0, 0 ))
        pygame.display.flip()
        
        clock.tick(60)
def drawLineBetween(screen, index, start, end, width, color): # Сглаживание
    global active_figures
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        #pygame.draw.circle(screen, (color), (x, y), width)
        active_figures.append (((x, y), color, width, "brush_process"))

main()
