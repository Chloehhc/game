# Virus Game
# Date: January 2021
# Block A1
# Author: Chloe Hsieh

# Game Instructions:
# You are in control of the hand (holding the wipe). Your goal is to wipe away all of the viruses on the screen to win!
# Unfortunately, there are infected hands roaming around! If you hit three of these hands, the game ends and you lose.
# However, each roll of toilet paper gives you an extra life!

import random
import pygame

# --- CONSTANTS ---
# Screen
GREEN = (64,77,0)
WIDTH = 1430
HEIGHT = 830

TITLE = "Virus Wipe"

# Initial Amounts
NUM_VIRUS = 50
NUM_HAND = 11
NUM_PAPER = 2

# Virus (what you are trying to wipe away in the game)
class Virus(pygame.sprite.Sprite):
    def __init__(self):
        # call the superclass constructor
        super().__init__()

        # Virus Image
        self.image = pygame.image.load("./images/cvirus.png")
        self.image = pygame.transform.scale(self.image, (53, 58))

        self.rect = self.image.get_rect()

        # Velocity of virus
        self.x_vel = 6
        self.y_vel = 6

    def update(self):
        # Move the virus
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Keep virus in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.y_vel *= -1

# Hand (enemy in game)
class Hand(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Scissor Image
        self.image = pygame.image.load("./images/hand.png")
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect()

        # Hand Velocity
        self.x_vel = 8

    def update(self):
        # Move Hands horizontally
        self.rect.x += self.x_vel

        # Keep hands in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1

# Paper (gives extra life in game)
class Paper(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/paper.png")
        self.image = pygame.transform.scale(self.image, (40, 66))

        self.rect = self.image.get_rect()

        self.x_vel = 7
        self.y_vel = 7

    def update(self):
        # Move paper
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Keep paper in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.y_vel *= -1

# (User controlled)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Use hand holding wipe as player
        self.image = pygame.image.load("./images/wipe.png")
        self.image = pygame.transform.scale(self.image, (90, 90))

        self.rect = self.image.get_rect()

    def update(self):
        # Control player with mouse
        self.rect.center = pygame.mouse.get_pos()

def main():
    pygame.init()

    # SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    score = 0
    hit_count = 0

    # Sprite Groups
    all_sprites = pygame.sprite.RenderUpdates()
    virus_group = pygame.sprite.Group()
    hand_group = pygame.sprite.Group()
    paper_group = pygame.sprite.Group()

    # Player creation
    player = Player()
    all_sprites.add(player)

    # Virus creation
    for i in range(NUM_VIRUS):
        virus = Virus()
        # Spawn inside visible screen
        virus.rect.x = random.randrange(WIDTH - virus.rect.width)
        virus.rect.y = random.randrange(HEIGHT - virus.rect.height)

        # Add virus to sprite groups
        all_sprites.add(virus)
        virus_group.add(virus)

    # Hand creation
    for i in range(NUM_HAND):
        hand = Hand()
        # Spawn inside visible screen
        hand.rect.x = random.randrange(WIDTH - hand.rect.width)
        hand.rect.y = random.randrange(HEIGHT - hand.rect.height)

        # Add scissor to sprite groups
        all_sprites.add(hand)
        hand_group.add(hand)

    # Paper creation
    for i in range(NUM_PAPER):
        paper = Paper()
        # Spawn inside visible screen
        paper.rect.x = random.randrange(WIDTH - paper.rect.width)
        paper.rect.y = random.randrange(HEIGHT - paper.rect.height)

        # Add paper to sprite groups
        all_sprites.add(paper)
        paper_group.add(paper)

    # MAIN LOOP
    while not done:
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # LOGIC
        all_sprites.update()

        # Player collides with virus
        virus_collected = pygame.sprite.spritecollide(player, virus_group, True)
        for virus in virus_collected:
            # add 1 to score for each virus collected
            score += 1

        # Player collides with hand
        hand_hit = pygame.sprite.spritecollide(player, hand_group, True)
        for hand in hand_hit:
            # add 1 to hit count each time user hits hand
            hit_count += 1

        # Player collides with paper
        paper_collected = pygame.sprite.spritecollide(player, paper_group, True)
        for paper in paper_collected:
            # gives 1 extra life to player each time player collects player by -1 from hit count
            hit_count -= 1

        # DRAW
        # Background
        screen.fill(GREEN)

        dirty_rectangles = all_sprites.draw(screen)

        # ----- UPDATE
        # update only dirty rectangles
        pygame.display.update(dirty_rectangles)
        clock.tick(60)

        # Player Wins
        # End game if all viruses have been wiped away.
        if score == NUM_VIRUS:
            print("Congratulations, you won!")
            break

        # Player Loses
        # If hit count is equal to 3, end the game.
        elif hit_count == 3:
            print("Oh no... you lost!")
            break

    print("Thanks for playing!")
    pygame.quit()

if __name__ == "__main__":
    main()