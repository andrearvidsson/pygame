import pygame

# Initiera Pygame
pygame.init()

# Skapa fönster
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test3.py")

# Definiera fyrkantens startposition och storlek
square_x, square_y = 400, 300
square_size = 30
speed = 5

# Färger
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Spelloop
running = True
while running:
    # Hantera händelser
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hantera tangenttryckningar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= speed
    if keys[pygame.K_RIGHT]:
        square_x += speed
    if keys[pygame.K_UP]:
        square_y -= speed
    if keys[pygame.K_DOWN]:
        square_y += speed

    # Håll fyrkanten inom fönstrets gränser
    square_x = max(0, min(screen_width - square_size, square_x))
    square_y = max(0, min(screen_height - square_size, square_y))

    # Rensa skärmen
    screen.fill(WHITE)

    # Rita fyrkanten
    pygame.draw.rect(screen, BLUE, (square_x, square_y, square_size, square_size))

    # Uppdatera skärmen
    pygame.display.flip()

    # Begränsa antal frames per sekund
    pygame.time.Clock().tick(30)

# Avsluta Pygame
pygame.quit()