from helper import *
from MainMenuItem import *
from subprocess import call

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
        self.lastEvent = datetime.now()

        mmbfile = open(CWD + '/MainMenuButtons.txt', 'r')
        self.buttonInfo = [f.split(' ') for f in mmbfile.read().split('\n')]
        mmbfile.close()
        x = 1
        self.updating = False
        for b in self.buttonInfo:
            self.buttons.append(MainMenuItem(self.skrn, self, x*75, b[0], self.setActive, x-1))
            x += 1
        self.translate((240, 0))

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
        after = datetime.now()
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

        if off > 0:
            deltaPos = (self.targetPos[0] - self.circleCenter[0], self.targetPos[1] - self.circleCenter[1])
            deltaPos = (deltaPos[0] * deltaTime*10, deltaPos[1]*deltaTime*10)
            self.translate(deltaPos)
        for button in self.buttons:
            button.logic()
        if self.updating:
            self.updating = False
            self.update()
        n = after - self.lastEvent
        if n.total_seconds() > 15 and not self.activeButton == None:
            self.buttons[self.activeButton].notActive()
            self.activeButton = None

    def event(self, event):
        self.lastEvent = datetime.now()
        print(event)
        if event == 'Swipe Right':        
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < 250:
                self.activeButton = None
        for button in self.buttons:
            button.event(event)

    def setActive(self, button):
        if button < len(self.buttons):
            if button == 4:
                pygame.quit()
                sys.exit()
            elif button == 3:
                self.updateStatus()
            else:
                self.activeButton = button
                self.buttons[button].setActive()
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
            button.points = button.getPoints()
    
    def distanceFrom(self, point):
        dx = self.circleCenter[0] - point[0]
        dy = self.circleCenter[1] - point[1]
        return sqrt(pow(dx, 2) + pow(dy, 2))
    
    def updateStatus(self):
        self.updating = True
        self.buttons[3].text = 'Updating...'
        
    def update(self):
        now = datetime.now()
        while now.microsecond > 100000:
            now = datetime.now()
        call(['git', 'pull', 'origin', 'master'])
        self.buttons[3].text = 'Up to date!'