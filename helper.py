import os
import sys 
import pygame
from math import *
from pygame.locals import *
from platform import system
from datetime import datetime


class Color:
    Primary = (0, 153, 255)
    Text = (0, 153, 255)
    Background = (35, 35, 35)



def text(skrn, text, pos=(0, 0), size=60, color=(255, 200, 100)):
    sys_font = pygame.font.SysFont("Arial", int(size))
    rendered = sys_font.render(str(text), 0, color)
    skrn.blit(rendered, pos)


pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)
# Windows is used to test and debug on my laptop for now, so we don't want it fullscreen
#   Since that's apain in the ass to test on
if system() == 'Windows':
    CWD='C:\\Users\\Kuuhaku\\Desktop\\PiCar2'
    skrn = pygame.display.set_mode((800, 480))
else:
    CWD='/home/pi/PiCar2'
    skrn = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)

SWIPE_TIME = 2