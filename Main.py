from helper import *
from MainScreen import *
from ScreenManager import *

def run():
    screenManager = ScreenManager(skrn)
    mainScreen = MainScreen(skrn, screenManager)
    screenManager.addScreen(mainScreen)
    now = datetime.now()
    before = now

    while True:
        after = datetime.now()
        deltaTime = after.second - before.second
        deltaTime *= 1000000
        deltaTime += after.microsecond - before.microsecond
        deltaTime = float(deltaTime) / 1000000
        before = after

        screenManager.draw()
        screenManager.logic(deltaTime)
        pygame.display.flip()
        for event in pygame.event.get():
            screenManager.event(event)

if __name__ == '__main__':
    run()