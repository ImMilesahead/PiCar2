from helper import *

class MainMenuItem:
    def __init__(self, skrn, mainDisplay, y=0, text='None', callback=None, args=None):
        self.skrn = skrn
        self.mainDisplay = mainDisplay
        self.text = text
        self.y = y
        self.callback = callback
        self.args = args

        self.dy = 50
        self.dx = 50
        self.initL = 300
        self.L = self.initL
        self.targetL = self.L

        #self.L = len(self.text)*25

        self.isActive = False

        self.before = datetime.now()

        self.minSize = 300
        self.maxSize = 300

        self.circleX = self.mainDisplay.circleCenter[0]
        self.circleR = self.mainDisplay.circleRadius

        self.points = self.getPoints()

        self.text_offset = 0
        self.targetTextOffset = 0
        

    def draw(self):
        if self.y < 480 and self.y > -50:
            pygame.draw.lines(self.skrn, Color.Primary, False, self.points, 1)
            text_pos = (self.points[3][0]+5+self.text_offset, self.points[0][1])
            if self.y > 240:
                text_pos = (self.points[0][0]+5+self.text_offset, text_pos[1])
            text(self.skrn, self.text, text_pos, 40, Color.Text)
    
    def f(self, y):
        self.circleX = self.mainDisplay.circleCenter[0]
        self.circleR = self.mainDisplay.circleRadius
        y = self.mainDisplay.circleCenter[1] - y
        theta = asin(float(y)/float(self.circleR))
        co = cos(theta)
        return self.circleR*co + self.circleX
        
    def logic(self):
        after = datetime.now()
        deltaTime = after.second - self.before.second
        deltaTime *= 1000000
        deltaTime += after.microsecond - self.before.microsecond
        deltaTime = float(deltaTime) / 1000000
        self.before = after
        
        self.points = self.getPoints()
        deltaL = self.targetL - self.L
        self.L += deltaL*deltaTime*10
        deltaText = self.targetTextOffset - self.text_offset
        self.text_offset += deltaText*deltaTime*10
        

    def event(self, event):
        self.points = self.getPoints()
        mouse_pos = pygame.mouse.get_pos()
        if event == 'Tap':
            if mouse_pos[0] >= self.points[0][0] and mouse_pos[0] <= self.points[2][0] and mouse_pos[1] >= self.points[0][1] and mouse_pos[1] <= self.points[2][1]:
                if self.args == None:
                    if not self.callback == None:
                        self.callback()
                else:
                    if not self.callback == None:
                        self.callback(self.args)
        if event == 'Swipe Right':
            if mouse_pos[0] < 250:
                self.isActive = False
                self.targetL = self.initL
                self.targetTextOffset = 0

    def setActive(self):
        self.isActive = True
        self.targetL = 445 + len(self.text)*20 - self.points[0][0]
        self.targetTextOffset = 435 - self.points[3][0]+5
    
    def setPos(self, y):
        self.y = y
    
    def getPoints(self):
        y2 = self.y+self.dy
        f1 = self.f(self.y)
        f2 = self.f(y2)
        p1 = (f1, self.y)
        p2 = (f1+self.L, self.y)
        p3 = (f2+self.L+self.dx+(f1-f2), y2)
        p4 = (f2, y2)
        return (p1, p2, p3, p4)