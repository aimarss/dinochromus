import pygame
import os
size = width, height = 800, 600
pygame.init()
pygame.display.set_caption('Dinochromus')
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
fps = 60
coords = x_pos, y_pos = 400, 310
isJump = False
JumpCount = 10

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

    def render(self):
        size = self.cell_size
        for i in range(40, self.height):
            for j in range(self.width):
                    pygame.draw.rect(screen, (0, 255, 0), (self.left + size * j, self.top + size * i, size, size))
                    pygame.draw.rect(screen, (0, 0, 0), (self.left + size * j, self.top + size * i, size, size), 1)


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, v):
        super().__init__(all_sprites)
        self.image = load_image("cactus.png")
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = 310
        self.v = v

    def update(self):
        self.rect.x -= self.v * 1/60


class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__(all_sprites)
        self.image = load_image("dinochromus.png")
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def dead(self):
        global velocity
        global running
        print('you are dead')
        velocity = 0
        running = False


velocity = 8
all_sprites = pygame.sprite.Group()
board = Board(80, 60)
dino = Dino(x_pos)
time = 0
screen.fill((255, 255, 255))
board.render()
lst_cactus = []
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isJump = True
                for JumpCount in range(-10, 10):
                    dino.rect.y -= (JumpCount**2)/2

    if time >= 120:
        lst_cactus.append(Cactus(width, velocity))
        velocity += time / 12
        time = 0
    for cactus in lst_cactus:
        if pygame.sprite.collide_mask(dino, cactus):
            dino.dead()
        cactus.update()
    all_sprites.draw(screen)
    screen.blit(dino.image, (dino.rect.x, dino.rect.y))
    board.render()
    pygame.display.update()
    time += 1
    clock.tick(fps)
