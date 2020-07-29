import pygame
from math import *

def getIndex(width, size):
    (xpos, ypos) = pygame.mouse.get_pos()
    x = floor(xpos/(width/size))
    y = floor(ypos/(width/size))

    return (x, y)
