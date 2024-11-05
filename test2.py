import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Pygame Window')

# Set up the font
font = pygame.font.SysFont(None, 24)  # You can change the font and size if needed

# Render the text
text = font.render('PYGAME', True, (255, 255, 255))  # White color

# Get the rectangle of the text
text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

# Main loop flag
running = True

# Main loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
    
    # Fill the screen with black color
    screen.fill((0, 0, 0))
    
    # Draw the text on the screen
    screen.blit(text, text_rect)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
