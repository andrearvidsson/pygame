# Importera nödvändiga bibliotek
import pygame  # Bibliotek för spelutveckling i Python
import random  # (Ej använt här, men kan användas för slumpmoment)

# Starta Pygame så att vi kan använda dess funktioner
pygame.init()

# Skapa ett fönster för spelet och sätt storleken till 1000x1000 pixlar
screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rogue-like Game")  # Sätter fönstrets namn

# Definiera färger som vi kommer använda (RGB-format)
WHITE = (255, 255, 255)  # Vit färg
BLACK = (0, 0, 0)        # Svart färg
GREEN = (0, 255, 0)      # Grön färg (spelaren)
BROWN = (139, 69, 19)    # Brun färg (dörrar)
GRAY = (169, 169, 169)   # Grå färg (trappor)

# Bestäm hur många rutor (celler) labyrinten ska ha och hur stora de är
maze_width, maze_height = screen_width // 40, screen_height // 40  # 25x25 rutor
cell_size = 40  # Varje ruta är 40x40 pixlar

# Spelarens startposition och egenskaper
char_x, char_y = 2, 2           # Spelaren börjar på ruta (2, 2) - inne i Rum 1
char_color = GREEN              # Spelaren är grön
char_size = cell_size // 2      # Spelaren är hälften så stor som en cell
char_speed = 1                  # Sänkt hastighet för mjukare rörelse
# Variabel för att hålla reda på riktning (startar åt höger)
direction = 'right'

# Funktion som skapar en "hus-layout" (labyrint) som en 2D-lista
# 1 = vägg, 0 = golv, 2 = dörr, 3 = trappa
# Returnerar en lista med listor (rutnät)
def generate_house_layout(width, height, left_door_y=None, right_door_y=None):
    # Skapa en yttre vägg runt hela huset
    maze = [[1 if x == 0 or y == 0 or x == width - 1 or y == height - 1 else 0 for x in range(width)] for y in range(height)]

    # Lägg till inre väggar som delar upp huset i fyra rum
    for i in range(1, height - 1):
        maze[i][width // 2] = 1  # Vertikal vägg i mitten
        maze[height // 2][i] = 1  # Horisontell vägg i mitten

    # Placera dörrar i de inre väggarna
    maze[height // 4][width // 2] = 2      # Dörr mellan övre vänster och övre höger
    maze[3 * height // 4][width // 2] = 2  # Dörr mellan nedre vänster och nedre höger
    maze[height // 2][width // 4] = 2      # Dörr mellan övre vänster och nedre vänster
    maze[height // 2][3 * width // 4] = 2  # Dörr mellan övre höger och nedre höger

    # Placera dörr i vänster yttervägg på angiven rad, annars ingen dörr
    if left_door_y is not None:
        maze[left_door_y][0] = 2
        maze[left_door_y][1] = 0  # Säkerställ golv innanför dörren
        maze[left_door_y][2] = 0  # Säkerställ öppning även om inre vägg
    # Placera dörr i höger yttervägg på angiven rad, annars slumpa (alltid för maze 1)
    right_candidates = [y for y in range(1, height - 1) if maze[y][width - 2] == 0]
    if right_door_y is not None:
        if right_door_y in right_candidates:
            maze[right_door_y][width - 1] = 2
    elif right_candidates:
        y = random.choice(right_candidates)
        maze[y][width - 1] = 2

    # Lägg till trappor i två av rummen
    maze[3][3] = 3  # Trappa i övre vänstra rummet
    maze[height - 4][width - 4] = 3  # Trappa i nedre högra rummet

    return maze

# Skapa själva labyrinten/huset
mazes = [generate_house_layout(maze_width, maze_height, right_door_y=char_y)]
for _ in range(1, 2):
    mazes.append(generate_house_layout(maze_width, maze_height))
current_maze = 0  # Vilket maze vi är i
player_positions = [(char_x, char_y) for _ in range(2)]
# Lista för maze-namn
maze_names = [f"Maze: {i+1:03d}" for i in range(len(mazes))]

# Huvudloopen för spelet. Körs tills spelaren stänger fönstret
running = True
last_direction = None  # Håller reda på senaste maze-byte-riktning
maze_changed = False
while running:
    # Kolla om spelaren försöker stänga fönstret
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Avsluta loopen

    if maze_changed:
        # Flytta spelaren ett steg in på golvet efter maze-byte
        if last_direction == 'right':
            char_x = 2
        elif last_direction == 'left':
            char_x = maze_width - 3
        maze_changed = False
        last_direction = None
        continue

    maze = mazes[current_maze]  # Se till att maze alltid pekar på rätt maze
    # Kolla vilka tangenter som är nedtryckta
    keys = pygame.key.get_pressed()
    # Flytta spelaren om det är möjligt (bara till golv, dörr eller trappa)
    if keys[pygame.K_LEFT]:
        if char_x - 1 < 0:
            if current_maze > 0:
                player_positions[current_maze] = (char_x, char_y)
                current_maze -= 1
                char_x, char_y = player_positions[current_maze]
                maze = mazes[current_maze]
                # Ta bort eventuella andra dörrar i höger yttervägg
                for y in range(1, maze_height-1):
                    if y != char_y and maze[y][maze_width-1] == 2:
                        maze[y][maze_width-1] = 1
                # Se till att högerdörren finns där du kommer in
                maze[char_y][maze_width-1] = 2
                maze[char_y][maze_width-2] = 0
                maze[char_y][maze_width-3] = 0
                maze_changed = True
                last_direction = 'left'
                continue
            else:
                continue
        else:
            if maze[char_y][char_x - 1] in [0, 2, 3]:
                char_x -= char_speed
                direction = 'left'
    if keys[pygame.K_RIGHT]:
        if char_x + 1 >= maze_width:
            if current_maze < len(mazes) - 1:
                player_positions[current_maze] = (char_x, char_y)
                current_maze += 1
                char_x, char_y = player_positions[current_maze]
                maze = mazes[current_maze]
                # Ta bort eventuella andra dörrar i vänster yttervägg
                for y in range(1, maze_height-1):
                    if y != char_y and maze[y][0] == 2:
                        maze[y][0] = 1
                # Se till att vänsterdörren finns där du kommer in
                maze[char_y][0] = 2
                maze[char_y][1] = 0
                maze[char_y][2] = 0
                maze_changed = True
                last_direction = 'right'
                continue
            else:
                # Skapa nytt maze till höger, placera vänster dörr exakt där spelaren kommer in
                mazes.append(generate_house_layout(maze_width, maze_height, left_door_y=char_y))
                player_positions.append((1, char_y))
                next_maze_number = int(maze_names[-1].split(':')[1]) + 1 if maze_names else 1
                maze_names.append(f"Maze: {next_maze_number:03d}")
                current_maze += 1
                char_x, char_y = player_positions[current_maze]
                maze = mazes[current_maze]
                # Se till att vänsterdörren finns där du kommer in
                for y in range(1, maze_height-1):
                    if y != char_y and maze[y][0] == 2:
                        maze[y][0] = 1
                maze[char_y][0] = 2
                maze[char_y][1] = 0
                maze[char_y][2] = 0
                maze_changed = True
                last_direction = 'right'
                continue
        else:
            if maze[char_y][char_x + 1] in [0, 2, 3]:
                char_x += char_speed
                direction = 'right'
    if keys[pygame.K_UP] and char_y - 1 >= 0 and maze[char_y - 1][char_x] in [0, 2, 3]:
        char_y -= char_speed
        direction = 'up'
    if keys[pygame.K_DOWN] and char_y + 1 < maze_height and maze[char_y + 1][char_x] in [0, 2, 3]:
        char_y += char_speed
        direction = 'down'

    # Rita om hela skärmen varje gång
    screen.fill(WHITE)
    # Skriv ut maze-namnet i övre vänstra hörnet med extra tydlig svart outline/skugga
    font = pygame.font.SysFont(None, 60, bold=True)
    text = font.render(maze_names[current_maze], True, WHITE)
    # Rita tjock svart outline/skugga bakom texten
    for dx in [-3, -2, -1, 0, 1, 2, 3]:
        for dy in [-3, -2, -1, 0, 1, 2, 3]:
            if dx != 0 or dy != 0:
                screen.blit(font.render(maze_names[current_maze], True, BLACK), (60+dx, 60+dy))
    # Rita vit text ovanpå
    screen.blit(text, (60, 60))
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, BROWN, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif maze[y][x] == 3:
                pygame.draw.rect(screen, GRAY, (x * cell_size, y * cell_size, cell_size, cell_size))

    # Rita spelaren som en grön fyrkant i rätt ruta
    player_rect = pygame.Rect(char_x * cell_size + cell_size // 4, char_y * cell_size + cell_size // 4, char_size, char_size)
    pygame.draw.rect(screen, char_color, player_rect)
    # Rita en indikator (pil/linje) som visar riktning
    center_x = player_rect.centerx
    center_y = player_rect.centery
    if direction == 'up':
        pygame.draw.line(screen, BLACK, (center_x, center_y), (center_x, center_y - char_size // 2), 3)
    elif direction == 'down':
        pygame.draw.line(screen, BLACK, (center_x, center_y), (center_x, center_y + char_size // 2), 3)
    elif direction == 'left':
        pygame.draw.line(screen, BLACK, (center_x, center_y), (center_x - char_size // 2, center_y), 3)
    elif direction == 'right':
        pygame.draw.line(screen, BLACK, (center_x, center_y), (center_x + char_size // 2, center_y), 3)

    pygame.display.flip()                # Uppdatera fönstret så att allt syns
    pygame.time.Clock().tick(30)         # Vänta så att spelet körs i max 30 bilder per sekund

pygame.quit()                            # Avsluta Pygame när spelet är klart
