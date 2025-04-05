import pygame
import os

pygame.init()

WIDTH, HEIGHT = 500, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Музыкальный плеер 🎵")

MUSIC_FOLDER = r"labs\\lab7\\assets"
songs = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

if not songs:
    raise FileNotFoundError("Нет музыкальных файлов в папке 'Music'")

current_song = 0
is_playing = True

pygame.mixer.init()

def play_song():
    """Воспроизведение текущего трека."""
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, songs[current_song]))
    pygame.mixer.music.play()

play_song()  # Запускаем первый трек

IMAGE_PATH = r"labs\\lab7\\assets\\i.webp"
if os.path.exists(IMAGE_PATH):
    background = pygame.image.load(IMAGE_PATH)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
else:
    print(f"Файл {IMAGE_PATH} не найден!")

button_images = {
    "play": pygame.image.load(r"labs\\lab7\\assets\\play.png"),
    "pause": pygame.image.load(r"labs\\lab7\\assets\\pause.png"),
    "next": pygame.image.load(r"labs\\lab7\\assets\\next.png"),
    "prev": pygame.image.load(r"labs\\lab7\\assets\\back.png"),
}

for key in button_images:
    button_images[key] = pygame.transform.scale(button_images[key], (80, 80))

button_positions = {
    "prev": (100, 320),
    "play_pause": (210, 320),
    "next": (320, 320),
}

running = True
while running:
    screen.fill((30, 30, 30))

    if 'background' in locals():
        screen.blit(background, (0, 0))

    screen.blit(button_images["prev"], button_positions["prev"])
    screen.blit(button_images["next"], button_positions["next"])

    # Отображаем Play или Pause в зависимости от состояния
    if is_playing:
        screen.blit(button_images["pause"], button_positions["play_pause"])
    else:
        screen.blit(button_images["play"], button_positions["play_pause"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Управление клавиатурой:  P - Play/Pause, N - Next, B - Previous
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if is_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                is_playing = not is_playing
            elif event.key == pygame.K_n:
                current_song = (current_song + 1) % len(songs)
                play_song()
                is_playing = True
            elif event.key == pygame.K_b:
                current_song = (current_song - 1) % len(songs)
                play_song()
                is_playing = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for key, pos in button_positions.items():
                btn_x, btn_y = pos
                if btn_x <= x <= btn_x + 80 and btn_y <= y <= btn_y + 80:
                    if key == "play_pause":
                        if is_playing:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        is_playing = not is_playing
                    elif key == "next":
                        current_song = (current_song + 1) % len(songs)
                        play_song()
                        is_playing = True
                    elif key == "prev":
                        current_song = (current_song - 1) % len(songs)
                        play_song()
                        is_playing = True

    pygame.display.flip()

pygame.quit()
