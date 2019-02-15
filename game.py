import pygame
import random
from functions import load_image, play_music, terminate, scoreupdate, high_score
velocity = 500
bvelocity = 700
all_sprites = pygame.sprite.Group()
size = width, height = 800, 600
pygame.init()
pygame.display.set_caption('Dinochromus')
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
fps = 60
coords = x_pos, y_pos = 15, 310
isJump = False
JumpCount = 10
start_group = pygame.sprite.Group()
dead_group = pygame.sprite.Group()
main_group = pygame.sprite.Group()
level_group = pygame.sprite.Group()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 10

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, color):
        size = self.cell_size
        for i in range(40, self.height):
            for j in range(self.width):
                    pygame.draw.rect(screen, color, (self.left + size * j, self.top + size * i, size, size))
                    pygame.draw.rect(screen, (0, 0, 0), (self.left + size * j, self.top + size * i, size, size), 1)


class Bird(pygame.sprite.Sprite):
    def __init__(self, x_pos, v, number):
        super().__init__(main_group, all_sprites)
        self.image = load_image('bird' + str(number) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(x_pos + 150, x_pos + 200)
        self.rect.y = random.randint(270, 300)
        self.v = v

    def update(self):
        self.rect.x -= self.v / 90

    def dead(self, list):
        for bird in list:
            bird.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, v, number, name):
        super().__init__(main_group, all_sprites)
        self.image = load_image(name + str(number) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 310
        self.v = v

    def update(self):
        self.rect.x -= self.v / 60

    def dead(self, list):
        for cactus in list:
            cactus.kill()


class Dino(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(main_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def dead(self):
        self.kill()


class start_buttons(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(start_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("red"))
        font = pygame.font.Font('data/font/PressStart2P.ttf', 30)
        text = font.render(title, 1, (0, 0, 0))
        text_x = 35
        text_y = 10
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class level_buttons(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(level_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("red"))
        font = pygame.font.Font('data/font/PressStart2P.ttf', 30)
        text = font.render(title, 1, (0, 0, 0))
        text_x = 35
        text_y = 10
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class dead_buttons(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(dead_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("red"))
        font = pygame.font.Font('data/font/PressStart2P.ttf', 30)
        text = font.render(title, 1, (0, 0, 0))
        text_x = 60
        text_y = 10
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


def game(velocity, bvelocity, color, isJump, JumpCount, running, name):
    play_music('soundtrack.mp3')
    pygame.mixer.music.set_volume(0.5)
    board = Board(80, 60)
    dino = Dino(load_image("dinos2.png"), 2, 1, x_pos, y_pos)
    time = 0
    score = int(time)
    screen.fill((255, 255, 255))
    board.render(color)
    lst_cactus = []
    lst_bird = []
    scorelist = []
    dead = False
    while running:
        birdchoose = random.randint(1, 2)
        cactuschoose = random.randint(1, 3)
        screen.fill((255, 255, 255))
        high_score(screen)
        scoreupdate(score, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE and not isJump) or (event.key == pygame.K_UP and not isJump):
                        isJump = True
                        JumpCount = -10
        if isJump:
            if JumpCount <= 10:
                dino.rect.y += int(JumpCount*5/3)
            elif JumpCount >= -10:
                isJump = False
            JumpCount += 1/2
        if time >= 10:
            if cactuschoose == 1:
                lst_cactus.append(Cactus(width, velocity, cactuschoose, name))
            elif cactuschoose == 2:
                lst_cactus.append(Cactus(width, velocity, cactuschoose, name))
            elif cactuschoose == 3:
                lst_cactus.append(Cactus(width, velocity, cactuschoose, name))
            if score >= 30:
                    if birdchoose == 1:
                        lst_bird.append(Bird(width, bvelocity, birdchoose))
                    if birdchoose == 2:
                        lst_bird.append(Bird(width, bvelocity, birdchoose))
                    bvelocity += 45
            velocity += 75
            time = 0
        if not isJump and not dead:
            dino.update()
        for cactus in lst_cactus:
            if pygame.sprite.collide_mask(dino, cactus):
                pygame.mixer.music.stop()
                i = 0
                cactus.dead(lst_cactus)
                dino.dead()
                while lst_cactus != lst_bird and i < len(lst_bird):
                    lst_bird[i].dead(lst_bird)
                    i += 1
                f = open("data/score.dat", "w")
                f.write(str(highscore))
                f.close()
                dead_screen(name)
                dead = True
            if not dead:
                cactus.update()
        for bird in lst_bird:
            if pygame.sprite.collide_mask(dino, bird):
                pygame.mixer.music.stop()
                dino.dead()
                bird.dead(lst_bird)
                n = 0
                while lst_bird != lst_cactus and n < len(lst_cactus):
                    lst_cactus[n].dead(lst_cactus)
                    n += 1
                f = open("data/score.dat", "w")
                f.write(str(highscore))
                f.close()
                dead_screen(name)
                dead = True
            if not dead:
                bird.update()
        if not dead:
            main_group.draw(screen)
            screen.blit(dino.image, (dino.rect.x, dino.rect.y))
            board.render(color)
            pygame.display.update()
        scorelist.append(score)
        highscore = max(scorelist)
        time += 0.1
        score += 0.1
        clock.tick(30)


def dead_screen(name):
    outro_text = ["Menu", 'Press SPACE to restart']
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('gameover.png'), (900, 700))
    screen.blit(fon, (-50, -150))
    font = pygame.font.Font('data/font/PressStart2P.ttf', 25)
    text = font.render(outro_text[1], 1, (100, 255, 100))
    text_x = 170
    text_y = 480
    screen.blit(text, (text_x, text_y))
    restart_button = dead_buttons(250, 50, outro_text[0], 270, 370)
    play_music('dead.mp3')
    high_score(screen)
    dead_group.draw(screen)
    pygame.display.flip()
    if name == 'cactus':
        color = (255, 219, 88)
    elif name == 'tree':
        color = (0, 255, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.check_click(event.pos):
                    start_screen()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed():
                    if event.key == pygame.K_SPACE:
                        game(velocity, bvelocity, color, isJump, JumpCount, running, name)

        pygame.display.flip()
        clock.tick(fps)


def start_screen():
    intro_text = ["DINO", "CHROM", 'US',
                  "Пустыня", 'Лес',
                  "Играть", "Выход"]
    screen.fill((255, 255, 255))
    tick = load_image('tick.png')
    fon = pygame.transform.scale(load_image('fon.png'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('data/font/PressStart2P.ttf', 50)
    text = font.render(intro_text[0], 1, (0, 255, 0))
    text_x = 120
    text_y = 50
    screen.blit(text, (text_x, text_y))
    text1 = font.render(intro_text[1], 1, (255, 0, 0))
    text_x = 320
    text_y = 50
    screen.blit(text1, (text_x, text_y))
    text2 = font.render(intro_text[2], 1, (255, 255, 0))
    text_x = 570
    text_y = 50
    screen.blit(text2, (text_x, text_y))
    high_score(screen)
    map1_button = start_buttons(250, 50, intro_text[3], 250, 360)
    map2_button = start_buttons(250, 50, intro_text[4], 250, 420)
    play_button = start_buttons(250, 50, intro_text[5], 250, 300)
    exit_button = start_buttons(250, 50, intro_text[6], 250, 480)
    start_group.draw(screen)
    pygame.display.flip()
    color = (255, 219, 88)
    name = "cactus"
    tickno = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.check_click(event.pos):
                    terminate()
                if map1_button.check_click(event.pos):
                    color = (255, 219, 88)
                    name = 'cactus'
                    if not tickno:
                        screen.blit(tick, (180, 360))
                        tickno = False
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), (180, 420, 64, 50))
                        screen.blit(tick, (180, 360))
                if map2_button.check_click(event.pos):
                    color = (0, 255, 0)
                    name = 'tree'
                    if not tickno:
                        screen.blit(tick, (180, 420))
                        tickno = False
                    else:
                        pygame.draw.rect(screen, (255, 255, 255), (180, 360, 64, 50))
                        screen.blit(tick, (180, 420))
                if play_button.check_click(event.pos):
                    game(velocity, bvelocity, color, isJump, JumpCount, running, name)
        pygame.display.flip()
        clock.tick(fps)


start_screen()






