from helper import *
from SmartValue import *
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
        self.L = SmartValue(300)
        self.text_offset = SmartValue(0)
        self.xOffset = SmartValue(0)

        self.isActive = False

        self.circleX = self.mainDisplay.circleCenter[0]
        self.circleR = self.mainDisplay.circleRadius

        self.points = self.getPoints()

        

    def draw(self):
        if self.y < 480 and self.y > -50:
            pygame.draw.lines(self.skrn, Color.Primary, False, self.points, 1)
            text_pos = (self.points[3][0]+5+self.text_offset.getValue(), self.points[0][1])
            if self.y > 240:
                text_pos = (self.points[0][0]+5+self.text_offset.getValue(), text_pos[1])
            text(self.skrn, self.text, text_pos, 40, Color.Text)
    
    def f(self, y):
        self.circleX = self.mainDisplay.circleCenter[0].getValue()
        self.circleR = self.mainDisplay.circleRadius
        y = self.mainDisplay.circleCenter[1].getValue() - y
        theta = asin(float(y)/float(self.circleR))
        co = cos(theta)
        return self.circleR*co + self.circleX
        
    def logic(self, deltaTime):
        self.L.logic(deltaTime)
        self.xOffset.logic(deltaTime)
        self.text_offset.logic(deltaTime)
        self.points = self.getPoints()
        

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
        
    def deactivate(self):
        self.isActive = False
        self.L.reset()
        self.text_offset.reset()
        self.xOffset.reset()

    def setActive(self):
        self.isActive = True
        self.L.setTarget(445 + len(self.text)*20 - self.points[0][0])
        self.text_offset.setTarget(435 - self.points[3][0]+5)
    
    def setPos(self, y):
        self.y = y
    
    def getPoints(self):
        y2 = self.y+self.dy
        f1 = self.f(self.y)
        f2 = self.f(y2)
        p1 = (f1+self.xOffset.getValue(), self.y)
        p2 = (f1+self.L.getValue()+self.xOffset.getValue(), self.y)
        p3 = (f2+self.L.getValue()+self.dx+(f1-f2)+self.xOffset.getValue(), y2)
        p4 = (f2+self.xOffset.getValue(), y2)
        return (p1, p2, p3, p4)