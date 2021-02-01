# KEYBOARD WIPE GAME

# Date: January 21, 2021
# Block: A1
# Author: Chloe Hsieh

# GAME INSTRUCTIONS ---------------------------------------------------------------------------------------------
# Programming class has concluded and it's time to wipe down your keyboard.
# You're in control of a hand holding a wipe.
# Your goal is to wipe away all the viruses; they are confined to the keyboard!
# Unfortunately, infected hands are roaming around both on and outside of the keyboard!
# Each time you come in contact with an infected hand, you lose a life; you initially have three lives.
# However, collecting one toilet paper roll equates to gaining one life; keep an eye out, they can move anywhere!
# ----------------------------------------------------------------------------------------------------------------

import random
import pygame

# CONSTANTS
# Screen
WIDTH = 1500
HEIGHT = 800

# Keyboard (in the background) Dimensions
KEYBOARD_RIGHT = 1440
KEYBOARD_LEFT = 60
KEYBOARD_TOP = 670
KEYBOARD_BOTTOM = 120

TITLE = "KEYBOARD WIPE"

# Initial Amounts
NUM_VIRUS = 100
NUM_HAND = 7
NUM_PAPER = 2


# VIRUS (what user is trying to wipe away)
class Virus(pygame.sprite.Sprite):
    """ Set velocity and image for virus. """
    def __init__(self):
        super().__init__()

        # Virus Image
        self.image = pygame.image.load("./images/cvirus.png")
        self.image = pygame.transform.scale(self.image, (43, 48))

        self.rect = self.image.get_rect()

        # Velocity of virus
        self.x_vel = 3
        self.y_vel = 3

    def update(self):
        """ Set movement directions for virus and keep it inside the keyboard image. """
        # Move the virus
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Keep virus within the keyboard
        if self.rect.right > KEYBOARD_RIGHT or self.rect.left < KEYBOARD_LEFT:
            self.x_vel *= -1
        if self.rect.top > KEYBOARD_TOP or self.rect.bottom < KEYBOARD_BOTTOM:
            self.y_vel *= -1

# INFECTED HAND (enemy)
class Hand(pygame.sprite.Sprite):
    """ Set image and velocity for enemy hand. """
    def __init__(self):
        super().__init__()

        # Hand image for enemy
        self.image = pygame.image.load("./images/hand.png")
        self.image = pygame.transform.scale(self.image, (83, 168))

        self.rect = self.image.get_rect()

        # Velocity of hand
        self.x_vel = 6

    def update(self):
        """ Set movement directions for enemy hand. """
        # Move hands horizontally
        self.rect.x += self.x_vel

        # Keep hands in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1

# TOILET PAPER (gives extra life in game)
class Paper(pygame.sprite.Sprite):
    """ Set image and velocity for toilet paper."""
    def __init__(self):
        super().__init__()

        # Use toilet paper roll image
        self.image = pygame.image.load("./images/paper.png")
        self.image = pygame.transform.scale(self.image, (60, 66))

        self.rect = self.image.get_rect()

        # Velocity of toilet paper
        self.x_vel = 2
        self.y_vel = 2

    def update(self):
        """ Set movement directions for toilet paper. """
        # Move paper
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Keep paper in the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.x_vel *= -1
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.y_vel *= -1

# HAND HOLDING WIPE/PLAYER (User controlled)
class Player(pygame.sprite.Sprite):
    """ Set image for user-controlled hand holding wipe. """
    def __init__(self):
        super().__init__()

        # Use hand holding wipe as player
        self.image = pygame.image.load("./images/wipe.png")
        self.image = pygame.transform.scale(self.image, (90, 90))

        self.rect = self.image.get_rect()

    def update(self):
        """ Allow user to control hand using mouse. """
        self.rect.center = pygame.mouse.get_pos()

# BACKGROUND
class Background(pygame.sprite.Sprite):
    """ Set keyboard a background. """
    def __init__(self):
        super().__init__()

        # Use keyboard image
        self.image = pygame.image.load("./images/keyboard.jpeg")
        self.image = pygame.transform.scale(self.image, (1500, 800))

        self.rect = self.image.get_rect()


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

    # SPRITE GROUPS
    all_sprites = pygame.sprite.RenderUpdates()
    virus_group = pygame.sprite.Group()
    hand_group = pygame.sprite.Group()
    paper_group = pygame.sprite.Group()

    # BACKGROUND (KEYBOARD) CREATION
    background = Background()
    all_sprites.add(background)

    # TOILET PAPER CREATION
    for i in range(NUM_PAPER):
        paper = Paper()
        # Spawn inside visible screen
        paper.rect.x = random.randrange(WIDTH - paper.rect.width)
        paper.rect.y = random.randrange(HEIGHT - paper.rect.height)

        # Add paper to sprite groups
        all_sprites.add(paper)
        paper_group.add(paper)

    # VIRUS CREATION
    for i in range(NUM_VIRUS):
        virus = Virus()
        # Spawn inside keyboard area
        virus.rect.x = random.randrange(KEYBOARD_LEFT + virus.rect.left, KEYBOARD_RIGHT - virus.rect.right)
        virus.rect.y = random.randrange(KEYBOARD_BOTTOM + virus.rect.bottom, KEYBOARD_TOP - virus.rect.top)

        # Add virus to sprite groups
        all_sprites.add(virus)
        virus_group.add(virus)

    # INFECTED HAND CREATION
    for i in range(NUM_HAND):
        hand = Hand()
        # Spawn inside visible screen
        hand.rect.x = random.randrange(WIDTH - hand.rect.width)
        hand.rect.y = random.randrange(HEIGHT - hand.rect.height)

        # Add hand to sprite groups
        all_sprites.add(hand)
        hand_group.add(hand)

    # PLAYER CREATION
    player = Player()
    all_sprites.add(player)

    # Main Loop
    while not done:
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # LOGIC
        all_sprites.update()

        # PLAYER COLLIDES WITH VIRUS
        virus_collected = pygame.sprite.spritecollide(player, virus_group, True)
        for virus in virus_collected:
            # add 1 to score for each virus collected
            score += 1

        # PLAYER COLLIDES WITH INFECTED HAND
        hand_hit = pygame.sprite.spritecollide(player, hand_group, True)
        for hand in hand_hit:
            # add 1 to hit count each time user hits infected hand
            hit_count += 1

        # PLAYER COLLIDES WITH PAPER
        paper_collected = pygame.sprite.spritecollide(player, paper_group, True)
        for paper in paper_collected:
            # gives 1 extra life to player each time player collects toilet paper by -1 from hit count
            hit_count -= 1

        # DRAW
        dirty_rectangles = all_sprites.draw(screen)

        # UPDATE
        pygame.display.update(dirty_rectangles)
        clock.tick(60)

        # PLAYER WINS
        # End game if all viruses have been wiped away
        if score == NUM_VIRUS:
            print()
            print("------------------------------------------------------------------")
            print("Congratulations, your keyboard has been immaculately cleansed!")
            break

        # PLAYER LOSES
        # End game if hit count is equal to 3
        elif hit_count == 3:
            print()
            print("------------------------------------------------------------------")
            print("Oh no... you came into contact with too many infected hands!")
            break

    # ENDING MESSAGE
    # Tell user their score (since total virus = 100, # virus wiped away = %)
    print(f"You wiped away {score}% of the viruses!")
    print()
    print("Thank you for playing!")
    print("------------------------------------------------------------------")
    pygame.quit()

if __name__ == "__main__":
    main()
