from helper import *

class ScreenManager:
    def __init__(self, skrn):
        self.skrn = skrn
        self.screens = []
        self.currentScreen = 0
        self.numberOfScreens = 0

        
        self.startTime = None
        self.endTime = None
        self.startPos = None
        self.endPos = None
    def addScreen(self, screen):
        self.screens.append(screen)
        self.numberOfScreens += 1
    def draw(self):
        self.skrn.fill(Color.Background)
        # Draw current screen
        self.screens[self.currentScreen].draw()
    def logic(self, deltaTime):
        self.screens[self.currentScreen].logic(deltaTime)
    def event(self, event):
        '''
        Swipe and tap detection
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.startPos = pygame.mouse.get_pos()
            self.startTime = datetime.now()
        if event.type == pygame.MOUSEBUTTONUP:
            self.endPos = pygame.mouse.get_pos()
            self.endTime = datetime.now()
            if self.endPos[0] == self.startPos[0] and self.endPos[1] == self.startPos[1]:
                self.screens[self.currentScreen].event('Tap')
            else:
                # Swipe
                # Find time took to swipe
                d_second = self.endTime.second - self.startTime.second
                d_micro = self.endTime.microsecond - self.startTime.microsecond
                if d_micro < 0:
                    d_second -= 1
                    d_micro += 1000000
                # Find direction    
                d_x = self.endPos[0] - self.startPos[0]
                d_y = self.startPos[1] - self.endPos[1]
                angle = 0
                try:
                    theta = atan(float(d_y)/float(d_x))
                    theta = 180*theta/pi
                    if d_x > 0 and d_y > 0:
                        #Q1
                        angle = theta
                    elif d_x < 0 and d_y > 0:
                        #Q2
                        angle = 180 + theta
                    elif d_x < 0 and d_y < 0:
                        #Q3
                        angle = 180 + theta
                    elif d_x > 0 and d_y < 0:
                        #Q4
                        angle = 360 + theta
                except:
                    if d_y > 0:
                        angle = 90
                    else:
                        angle = 270
                    print('possible error or divide by zero')
                if d_second < SWIPE_TIME:
                    if angle <  45 or angle > 315:
                        # Swipe Right
                        self.screens[self.currentScreen].event('Swipe Right')
                    elif angle > 45 and angle < 135:
                        self.screens[self.currentScreen].event('Swipe Up')
                    elif angle > 135 and angle < 225:
                        self.screens[self.currentScreen].event('Swipe Left')
                    elif angle > 225 and angle < 315:
                        self.screens[self.currentScreen].event('Swipe Down')     
        self.screens[self.currentScreen].event(event)              
    def loadScreen(self, screen):
        if screen < self.numberOfScreens:
            self.currentScreen = screen
        else:
            print ('Tried to load an unavailable screen')