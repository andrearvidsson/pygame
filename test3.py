import pygame
import sys
import random

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
BLACK = (0, 0, 0)

# Set up the font
font = pygame.font.Font(None, 144)

# Render the text
text = font.render("GAME", True, WHITE)
text_rect = text.get_rect(center=(400, 300))

# Define a variable to track the shape
is_square = True
blink_interval = 500  # milliseconds
last_blink_time = pygame.time.get_ticks()

# Define dots
dot_radius = 10
dot_color = (255, 255, 0)  # Yellow
dots = [(random.randint(dot_radius, screen_width - dot_radius), random.randint(dot_radius, screen_height - dot_radius)) for _ in range(5)]

# Initialize score
score = 0
score_font = pygame.font.Font(None, 36)

# Splash screen loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False

    # Fill the screen with black
    screen.fill(BLACK)
    
    # Draw the text
    screen.blit(text, text_rect)
    
    # Update the display
    pygame.display.flip()

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

    # Check for collision with dots
    player_rect = pygame.Rect(square_x, square_y, square_size, square_size)
    new_dots = []
    for dot in dots:
        if player_rect.collidepoint(dot):
            score += 5
        else:
            new_dots.append(dot)
    dots = new_dots

    # Blink the shape
    current_time = pygame.time.get_ticks()
    if current_time - last_blink_time >= blink_interval:
        is_square = not is_square
        last_blink_time = current_time

    # Rensa skärmen
    screen.fill(WHITE)

    # Rita fyrkanten eller cirkeln
    if is_square:
        pygame.draw.rect(screen, BLUE, (square_x, square_y, square_size, square_size))
    else:
        pygame.draw.circle(screen, BLUE, (square_x + square_size // 2, square_y + square_size // 2), square_size // 2)

    # Draw dots
    for dot in dots:
        pygame.draw.circle(screen, dot_color, dot, dot_radius)

    # Draw score
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Uppdatera skärmen
    pygame.display.flip()

    # Begränsa antal frames per sekund
    pygame.time.Clock().tick(30)

# Avsluta Pygame
pygame.quit()