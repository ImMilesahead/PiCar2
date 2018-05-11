from helper import *
from MainMenuItem import *

class MainDisplay:
    def __init__(self, skrn):
        self.skrn = skrn
        self.initPos = (-240, 240)
        self.circleCenter = self.initPos
        self.targetPos = self.initPos
        self.circleRadius = 322

        self.buttons = []
        self.activeButton = None
        self.before = datetime.now()

        mmbfile = open(os.getcwd() + '/MainMenuButtons.txt', 'r')
        self.buttonInfo = [f.split(' ') for f in mmbfile.read().split('\n')]
        mmbfile.close()
        x = 1
        for b in self.buttonInfo:
            self.buttons.append(MainMenuItem(self.skrn, self, x*75, b[0], self.setActive, x-1))
            x += 1
        self.translate((100, 0))

        #self.buttons = [self.music, self.diag, self.maps, self.update, self.quit]


    def draw(self):
        #Draw oval thing
        pygame.draw.circle(self.skrn, Color.Primary, (int(self.circleCenter[0]), int(self.circleCenter[1])), self.circleRadius   , 2)

        now = datetime.now()
        hour = now.hour
        if hour < 10:
            hour = '0' + str(hour)
        minute = now.minute
        if minute < 10:
            minute = '0' + str(minute)
        
        text(self.skrn, hour, (self.circleCenter[0] + 250, self.circleCenter[1] -40), size=48, color=Color.Text)
        text(self.skrn, minute, (self.circleCenter[0] +250, self.circleCenter[1]), size=48, color=Color.Text)

        for button in self.buttons:
            button.draw()


    def logic(self):
        now = datetime.now
        after = now()
        deltaTime = after.second - self.before.second
        deltaTime *= 1000000
        deltaTime += after.microsecond - self.before.microsecond
        deltaTime = float(deltaTime) / 1000000
        self.before = after
        if self.activeButton == None:
            self.targetPos = self.initPos
        else:
            self.targetPos = (self.initPos[0] - 435, self.initPos[1])
        off = self.distanceFrom(self.targetPos)

        if off < 15 and off > 0:
            self.circleCenter = self.targetPos
        elif off > 0:
            deltaPos = (self.targetPos[0] - self.circleCenter[0], self.targetPos[1] - self.circleCenter[1])
            deltaPos = (deltaPos[0] * deltaTime*10, deltaPos[1]*deltaTime*10)
            self.translate(deltaPos)
        for button in self.buttons:
            button.logic()

    def event(self, event):
        if event == 'Swipe Right':
            self.activeButton = None
        for button in self.buttons:
            button.event(event)

    def setActive(self, button):
        if button == 4:
            pygame.quit()
            sys.exit()
        if button < len(self.buttons):
            self.activeButton = button
            pass
        else:
            # Should never happen
            pass
    def getActiveButton(self):
        return self.activeButton

    def translate(self, deltaPos):
        self.circleCenter = (self.circleCenter[0] + deltaPos[0], self.circleCenter[1] + deltaPos[1])
        for button in self.buttons:
            button.y += deltaPos[1]
    
    def distanceFrom(self, point):
        dx = self.circleCenter[0] - point[0]
        dy = self.circleCenter[1] - point[1]
        return sqrt(pow(dx, 2) + pow(dy, 2))