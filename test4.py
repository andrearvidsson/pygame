import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rogue-like Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)  # Color for doors
GRAY = (169, 169, 169)  # Color for stairs

# Maze dimensions
maze_width, maze_height = screen_width // 40, screen_height // 40
cell_size = 40

# Character
char_x, char_y = 1, 1
char_color = GREEN
char_size = cell_size // 2
char_speed = 2  # Slower speed for more fluent movement

# House layout generation
def generate_house_layout(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Create rooms
    rooms = [
        (1, 1, 8, 8),  # Room 1
        (10, 1, 8, 8),  # Room 2
        (1, 10, 8, 8),  # Room 3
        (10, 10, 8, 8)  # Room 4
    ]
    
    for (x, y, w, h) in rooms:
        for i in range(y, y + h):
            for j in range(x, x + w):
                maze[i][j] = 0
    
    # Create doors
    doors = [
        (9, 4),  # Door between Room 1 and Room 2
        (4, 9),  # Door between Room 1 and Room 3
        (9, 14),  # Door between Room 3 and Room 4
        (14, 9)  # Door between Room 2 and Room 4
    ]
    
    for (x, y) in doors:
        maze[y][x] = 2
    
    # Create stairs
    stairs = [
        (5, 5),  # Stairs up in Room 1
        (15, 15)  # Stairs down in Room 4
    ]
    
    for (x, y) in stairs:
        maze[y][x] = 3
    
    return maze

maze = generate_house_layout(maze_width, maze_height)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and maze[char_y][char_x - 1] in [0, 2, 3]:
        char_x -= char_speed
    if keys[pygame.K_RIGHT] and maze[char_y][char_x + 1] in [0, 2, 3]:
        char_x += char_speed
    if keys[pygame.K_UP] and maze[char_y - 1][char_x] in [0, 2, 3]:
        char_y -= char_speed
    if keys[pygame.K_DOWN] and maze[char_y + 1][char_x] in [0, 2, 3]:
        char_y += char_speed

    # Draw everything
    screen.fill(WHITE)
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, BROWN, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif maze[y][x] == 3:
                pygame.draw.rect(screen, GRAY, (x * cell_size, y * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, char_color, (char_x * cell_size + cell_size // 4, char_y * cell_size + cell_size // 4, char_size, char_size))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
