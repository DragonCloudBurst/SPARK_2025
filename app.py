import pygame
import map

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 30

WHITE = (255, 255, 255)
DARK_GREY = (30, 30, 30)

score = 0

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
    12: pygame.image.load("images/walls/patient_room.png")
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
    def __init__(self, x, y, rect, image, player):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.dy = 0

    # referenced from here: https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame
    def move_towards_player(self, player, walls):
        dirvect = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                      player.rect.centery - self.rect.centery)
        if dirvect.length() > 0:
            dirvect.normalize()
            dirvect.scale_to_length(2)
    
            #Aided Heavily from the Google AI feature
            line = (self.rect.centerx, self.rect.centery,
                    player.rect.centerx, player.rect.centery)
            wall_in_sight = False
            for wall in walls:
                if wall.rect.clipline(line):
                    wall_in_sight = True
                    break

            # Collision Detection and Movement
            if not wall_in_sight:
                self.dx = dirvect.x
                self.dy = dirvect.y

                new_rect = self.rect.copy()
                new_rect.x += self.dx
                new_rect.y += self.dy

                collision = False
                for wall in walls:
                    if new_rect.colliderect(wall.rect):
                        collision = True
                        break

                if not collision:
                    self.rect.x += self.dx
                    self.rect.y += self.dy
            else:
                pass

    def update(self, player, walls):
        screen.blit(self.image, self.rect)
        self.move_towards_player(player, walls)

'''
Class for collectable pills
'''
class Pill():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('images/pills/pill_1pt.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collected = False

    def draw(self):
        if not self.collected:
            screen.blit(self.image, self.rect)
    def collect(self):
        self.collected = True

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

def gameLoop():
    global score
    is_running = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    player = Player(550, 30, player_rect)
    enemies = [
        Opp(200, 120, enemy_rect, pygame.image.load('images/germs/germ_1.png'), player),
        Opp(400, 150, enemy_rect, pygame.image.load('images/germs/germ_2.png'), player),
        Opp(25, 300, enemy_rect, pygame.image.load('images/germs/germ_3.png'), player)
    ]
    perc = Pill(450, 70)
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
        screen.fill(DARK_GREY)
        clock.tick(FPS)

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player.moving = False
                pygame.mixer.music.stop()
                death_sound.play()
                pygame.time.wait(2000)
                is_running = False
                print("Aww Man")
                print(f"Final Score: {score}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                print("done")
                break

        player.update(walls)
        for enemy in enemies:
            enemy.update(player, walls)
            #enemy wall collision detection.      
            new_enemy_rect = enemy.rect.copy()
            new_enemy_rect.x += enemy.dx
            new_enemy_rect.y += enemy.dy

            enemy_collision = False
            enemy_collision_wall = None

            for wall in walls:
                if new_enemy_rect.colliderect(wall.rect):
                    enemy_collision = True
                    enemy_collision_wall = wall
                    break
            if enemy_collision and enemy_collision_wall: 
                enemy.rect.x -= enemy.dx
                enemy.rect.y -= enemy.dy

        perc.draw()

        if player.rect.colliderect(perc.rect) and not perc.collected:
            perc.collect()
            score += 1
            print("+1")

        for wall in walls:
            wall.update()

        pygame.display.flip()

gameLoop()