import pygame
import map

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 30

WHITE = (255, 255, 255)


pygame.init()
pygame.mixer.init()

death_sound = pygame.mixer.Sound('music/SparkFlatline.mp3')
pygame.mixer.music.load('music/Spark25.mp3')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

player_rect = pygame.Rect(30, 30, 30, 30)
enemy_rect = pygame.Rect(40, 40, 40, 40)
perc_rect = pygame.Rect(30, 30, 30, 30)

wall_images = {
    6: pygame.image.load("images/walls/wall_corner_bottomleft.png"),
    7: pygame.image.load("images/walls/wall_corner_bottomright.png"),
    8: pygame.image.load("images/walls/wall_corner_topleft.png"),
    9: pygame.image.load("images/walls/wall_corner_topright.png"),
    10: pygame.image.load("images/walls/wall_hori.png"),
    11: pygame.image.load("images/walls/wall_vert.png"),
}

'''
Class for Walls
'''
class Wall():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)

'''
Class for enemies
'''
class Opp():
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/germs/germ_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        screen.blit(self.image, self.rect)

'''
Class for players
'''
class Player():
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/player_doctor.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.moving = True
        self.dx = 0
        self.dy = 0

    def update(self, walls):
        if self.moving:
            self.dx = 0
            self.dy = 0

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.dx = -2
            if key[pygame.K_RIGHT]:
                self.dx = 2
            if key[pygame.K_UP]:
                self.dy = -2
            if key[pygame.K_DOWN]:
                self.dy = 2

            new_rect = self.rect.copy()
            new_rect.x += self.dx
            new_rect.y += self.dy

            collision = False
            collision_wall = None
            for wall in walls:
                if new_rect.colliderect(wall.rect):
                    collision = True
                    collision_wall = wall
                    break

            if not collision:
                self.rect = new_rect
            else:
                if self.dx > 0 and self.rect.right > collision_wall.rect.left and self.rect.left < collision_wall.rect.left:
                    self.dx = 0
                if self.dx < 0 and self.rect.left < collision_wall.rect.right and self.rect.right > collision_wall.rect.right:
                    self.dx = 0
                if self.dy > 0 and self.rect.bottom > collision_wall.rect.top and self.rect.top < collision_wall.rect.top:
                    self.dy = 0
                if self.dy < 0 and self.rect.top < collision_wall.rect.bottom and self.rect.bottom > collision_wall.rect.bottom:
                    self.dx = 0
                    self.dy = 0

            self.rect.x += self.dx
            self.rect.y += self.dy

            screen.blit(self.image, self.rect)

class Pills():
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/pills/pill_1pt.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        screen.blit(self.image, self.rect)


def gameLoop():
    is_running = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    player = Player(300, 200, player_rect)
    enemy = Opp(100, 100, enemy_rect)
    perc = Pills(100, 100, perc_rect)
    pygame.mixer.music.play(-1)

    cell_size = 16
    walls = []

    for row_index, row in enumerate(map.map_tiles):
        for col_index, tile in enumerate(row):
            if tile in wall_images:
                image = wall_images[tile]
                wall = Wall(col_index * cell_size, row_index * cell_size, image)
                walls.append(wall)

    while is_running:
        screen.fill(WHITE)
        clock.tick(FPS)

        if player.rect.colliderect(enemy.rect):
            player.moving = False
            pygame.mixer.music.stop()
            death_sound.play()
            pygame.time.wait(3000)
            is_running = False
            print("Aww Man")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                print("done")
                break

        player.update(walls)
        enemy.update()
        for wall in walls:
            wall.update()
        pygame.display.flip()

gameLoop()