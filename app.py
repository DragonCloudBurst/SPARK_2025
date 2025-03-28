import pygame

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

class Player():
    def __init__(self, x, y, rect):
        self.x = x
        self.y = y
        self.rect = rect

    def update(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
           self.x -= 5
        if key[pygame.K_RIGHT]:
           self.x += 5

        self.rect = pygame.draw.rect(screen, RED, player_rect)
        screen.blit(screen, self.rect)
        
        pygame.display.flip()
    

def gameLoop():
    is_running = True
    clock = pygame.time.Clock()
    clock.tick(FPS)

    player = Player(300, 200, player_rect)

    while is_running:

        screen.fill(BLACK)
        pygame.display.flip()
        clock.tick(FPS)
        

        for event in pygame.event.get():

            player.update()

            if event.type == pygame.QUIT:
                is_running = False
                print("done")
                break

        pygame.display.flip()

gameLoop()
