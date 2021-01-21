# game

import random
import pygame

# TODO: collision w/ virus

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 720
HEIGHT = 1000
TITLE = "<You're title here>"
NUM_VIRUS = 75

class Virus(pygame.sprite.Sprite):
    def __init__(self):
        # call the superclass constructor
        super().__init__()

        # Image (is a Surface)
        self.image = pygame.Surface((35,20))
        self.image.fill((170,250,250)) # light blue

        # Rect (is Rectangle) (x, y, width, height)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Use charmander as player
        self.image = pygame.image.load("./images/wipe.png")
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()

    def update(self):
        """Move the player with the mouse"""
        self.rect.center = pygame.mouse.get_pos()

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Sprite Groups
    all_sprites = pygame.sprite.RenderUpdates()
    virus_group = pygame.sprite.Group()

    #  --- player
    player = Player()
    all_sprites.add(player)

    # Virus creation
    for i in range(NUM_VIRUS):
        virus = Virus()
        # Spawn inside visible screen
        virus.rect.x = random.randrange(WIDTH - virus.rect.width)
        virus.rect.y = random.randrange(HEIGHT - virus.rect.height)
        all_sprites.add(virus)
        virus_group.add(virus)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC
        all_sprites.update()

        # ----- DRAW
        screen.fill(BLACK)
        dirty_rectangles = all_sprites.draw(screen)

        # ----- UPDATE
        # update only dirty rectangles
        pygame.display.update(dirty_rectangles)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()