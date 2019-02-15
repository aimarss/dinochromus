import pygame
import os
import sys

clock = pygame.time.Clock()
fps = 60


def play_music(name):
    fullname = os.path.join('data', name)
    try:
        pygame.mixer.music.load(fullname)
        pygame.mixer_music.play()

    except pygame.error as message:
        print('Cannot load music:', name)
        raise SystemExit(message)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def scoreupdate(score, screen):
    score = round(score, 1)
    printedscore = str(score)
    font = pygame.font.Font('data/font/PressStart2P.ttf', 20)
    text = font.render(printedscore, 0,  (0, 0, 0))
    text_x = 50
    text_y = 50
    screen.blit(text, (text_x, text_y))


def high_score(screen):
    scores = []
    f = open("data/score.dat", "r")
    lastscore = f.read()
    f.close()
    scores.append(lastscore)
    for i in range(len(scores)):
        if scores[i] >= scores[0]:
            highscore = scores[i]
    font = pygame.font.Font('data/font/PressStart2P.ttf', 20)
    text = font.render('High: ' + highscore, 0, (255, 0, 0))
    text_x = 560
    text_y = 110
    screen.blit(text, (text_x, text_y))


def terminate():
    pygame.quit()
    sys.exit()
