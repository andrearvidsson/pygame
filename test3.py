import pygame

# Initiera Pygame
pygame.init()

# Skapa fönster
skärm_bredd, skärm_höjd = 800, 600
skärm = pygame.display.set_mode((skärm_bredd, skärm_höjd))
pygame.display.set_caption("Test3.py")

# Definiera fyrkantens startposition och storlek
fyrkant_x, fyrkant_y = 400, 300
fyrkant_storlek = 30
hastighet = 5

# Färger
VIT = (255, 255, 255)
BLÅ = (0, 0, 255)

# Spelloop
kör = True
while kör:
    # Hantera händelser
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kör = False

    # Hantera tangenttryckningar
    tangenter = pygame.key.get_pressed()
    if tangenter[pygame.K_LEFT]:
        fyrkant_x -= hastighet
    if tangenter[pygame.K_RIGHT]:
        fyrkant_x += hastighet
    if tangenter[pygame.K_UP]:
        fyrkant_y -= hastighet
    if tangenter[pygame.K_DOWN]:
        fyrkant_y += hastighet

    # Håll fyrkanten inom fönstrets gränser
    fyrkant_x = max(0, min(skärm_bredd - fyrkant_storlek, fyrkant_x))
    fyrkant_y = max(0, min(skärm_höjd - fyrkant_storlek, fyrkant_y))

    # Rensa skärmen
    skärm.fill(VIT)

    # Rita fyrkanten
    pygame.draw.rect(skärm, BLÅ, (fyrkant_x, fyrkant_y, fyrkant_storlek, fyrkant_storlek))

    # Uppdatera skärmen
    pygame.display.flip()

    # Begränsa antal frames per sekund
    pygame.time.Clock().tick(30)

# Avsluta Pygame
pygame.quit()