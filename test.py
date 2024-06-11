#import the libraries needed for this program.
import pygame, sys
pygame.init()

	#set the display to be 1280x768 and set it's caption to "PyGame"
display = pygame.display.set_mode((1280, 768))
pygame.display.set_caption('PyGame') # add a title to this game!

	#set the frame rate of the program to be at least 60 frames per second:
clock = pygame.time.Clock()
clock.tick(60) # set frame rate to 60 frames per second

    #clear the screen and fill it with black color
display.fill((0, 0, 0))

pygame.display.update()
