from helper import *
from MainDisplay import *

class MainScreen:
    def __init__(self, skrn, screenManager):
        self.skrn = skrn
        self.screenManager = screenManager
    
        self.mainDisplay = MainDisplay(skrn)

    def draw(self):
        
        # Draw Time
        self.mainDisplay.draw()
        

    def logic(self):
        self.mainDisplay.logic()


    def event(self, event):
        self.mainDisplay.event(event)
