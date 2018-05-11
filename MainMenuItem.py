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
        self.L=300
        #self.L = len(self.text)*25

        self.minSize = 300
        self.maxSize = 300

        self.circleX = self.mainDisplay.circleCenter[0]
        self.circleR = self.mainDisplay.circleRadius

        self.points = self.getPoints()
        

    def draw(self):
        if self.y < 480 and self.y > -50:
            pygame.draw.lines(self.skrn, Color.Primary, False, self.points, 1)
            text_pos = (self.points[3][0]+5, self.points[0][1])
            if self.y > 240:
                text_pos = (self.points[0][0]+5, text_pos[1])
            text(self.skrn, self.text, text_pos, 40, Color.Text)
    
    def f(self, y):
        self.circleX = self.mainDisplay.circleCenter[0]
        self.circleR = self.mainDisplay.circleRadius
        y = self.mainDisplay.circleCenter[1] - y
        theta = asin(float(y)/float(self.circleR))
        co = cos(theta)
        return self.circleR*co + self.circleX
        
    def logic(self):
        self.points = self.getPoints()

    def event(self, event):
        self.points = self.getPoints()
        if event == 'Tap':
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] >= self.points[0][0] and mouse_pos[0] <= self.points[2][0] and mouse_pos[1] >= self.points[0][1] and mouse_pos[1] <= self.points[2][1]:
                if self.args == None:
                    if not self.callback == None:
                        self.callback()
                else:
                    if not self.callback == None:
                        self.callback(self.args)


    
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