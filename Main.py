from helper import *
from MainScreen import *
from ScreenManager import *

def run():
    screenManager = ScreenManager(skrn)
    mainScreen = MainScreen(skrn, screenManager)
    screenManager.addScreen(mainScreen)

    while True:
        screenManager.draw()
        pygame.display.flip()
        screenManager.logic()
        for event in pygame.event.get():
            screenManager.event(event)

if __name__ == '__main__':
    run()