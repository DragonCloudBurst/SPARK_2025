import pygame

# referencing preexisting code from my team in class: https://github.com/DragonCloudBurst/Team-3-SENG-1005-Project/blob/main/main.py

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
pygame.mixer.init()

death_sound = pygame.mixer.Sound('music/SparkFlatline.mp3')
pygame.mixer.music.load('music/Spark25.mp3')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


player_rect = pygame.Rect(30, 30, 30, 30)
enemy_rect = pygame.Rect(40, 40, 40, 40)

class Wall():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        pygame.draw.rect(screen, BLACK, self.rect)

'''
This is the class for an enemy in the game
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

top_wall = Wall(0, 0, SCREEN_WIDTH, 10)
left_wall = Wall(0, 0, 10, SCREEN_HEIGHT)
bottom_wall = Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
right_wall = Wall(SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT)
walls = [top_wall, bottom_wall, left_wall, right_wall]

'''
This is a player class
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

    def update(self):
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
            pygame.display.flip()

def gameLoop():
    is_running = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    player = Player(300, 200, player_rect)
    enemy = Opp(100, 100, enemy_rect)
    pygame.mixer.music.play(-1)

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

        player.update()
        enemy.update()
        for wall in walls:
            wall.update()
        pygame.display.flip()

gameLoop()