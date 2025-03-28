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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spark 2025")

player_rect = pygame.Rect(30, 30, 30, 30)
enemy_rect = pygame.Rect(40, 40, 40, 40)

'''
This is the class for an enemy in the game
'''
class Opp():
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y 
        self.image = pygame.image.load('images/placeholder-player.png')
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        screen.blit(self.image, self.rect)
        pygame.display.flip()



class Player():
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y 
        self.image = pygame.image.load('images/placeholder-player.png')
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.moving = True

    def update(self):
        if self.moving:
            dx = 0
            dy = 0
            
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 10
            if key[pygame.K_RIGHT]:
                dx += 10
            if key[pygame.K_DOWN]:
                dy += 10
            if key[pygame.K_UP]:
                    dy -= 10

            self.rect.x += dx
            self.rect.y += dy

            screen.blit(self.image, self.rect)
            
            pygame.display.flip()
    



def gameLoop():
    is_running = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    player = Player(300, 200, player_rect) 
    enemy = Opp(100, 100, enemy_rect)



    while is_running:

        screen.fill(WHITE)
        clock.tick(FPS)
        
        if player.rect.colliderect(enemy.rect) :
            player.moving = False

        for event in pygame.event.get():

            player.update()
            enemy.update()
            
            if event.type == pygame.QUIT:
                is_running = False
                print("done")
                break

gameLoop()
