from helper import *
from MainMenuItem import *
from subprocess import call
from SmartValue import *

class MainDisplay:
    def __init__(self, skrn):
        self.skrn = skrn
        self.circleCenter = (SmartValue(-240), SmartValue(240))

        self.circleRadius = 322
        self.updating = False

        self.buttons = []
        self.activeButton = None

        mmbfile = open(CWD + '/MainMenuButtons.txt', 'r')
        self.buttonInfo = [f.split(' ') for f in mmbfile.read().split('\n')]
        mmbfile.close()
        x = 1
        for b in self.buttonInfo:
            self.buttons.append(MainMenuItem(self.skrn, self, x*75, b[0], self.setActive, x-1))
            x += 1
        self.buttons[0].slcallback=self.musicLeft
        self.buttons[0].srcallback=self.musicRight

        self.showMusicControls = False
        self.musicX = SmartValue(350)

        self.musicImage = pygame.image.load(CWD + '/Media/Pictures/MediaControls.png')
        self.musicImage = pygame.transform.scale(self.musicImage, (120, 40))

        self.animateCircleAngle = 90
        self.lastEvent = datetime.now()
        self.hour = '00'
        self.minute = '00'

    def draw(self):
        if self.musicX.getValue() < 390:
            self.skrn.blit(self.musicImage, (self.musicX.getValue(), 80))
        pygame.draw.rect(self.skrn, Color.Background, (self.musicX.getInitPos(), 80, 120, 40), 0)
        # We wanna draw the buttons first so that we can hide them behind the display
        for button in self.buttons:
            button.draw()
        #Draw oval thing
        pygame.draw.circle(self.skrn, Color.Primary, (int(self.circleCenter[0].getValue()), int(self.circleCenter[1].getValue())), self.circleRadius, 2)
        pygame.draw.circle(self.skrn, Color.Background, (int(self.circleCenter[0].getValue()), int(self.circleCenter[1].getValue())), self.circleRadius-1)
        # Draw Text
        p1 = (575, 0)
        p2 = (600, 25)
        p3 = (800, 25)
        points = (p1, p2, p3)
        
        pygame.draw.lines(self.skrn, Color.Primary, False, points, 1)
        text(self.skrn, "S - Interface Mk 2", (600, 0), size=24, color=Color.Text)
        # TODO move ^ somewhere else
        text(self.skrn, self.hour, (self.circleCenter[0].getValue() + 250, self.circleCenter[1].getValue() -40), size=48, color=Color.Text)
        text(self.skrn, self.minute, (self.circleCenter[0].getValue() + 250, self.circleCenter[1].getValue()), size=48, color=Color.Text)

        
    def logic(self, deltaTime):
        # Update Time to Display
        now = datetime.now()
        self.hour = now.hour
        self.minute = now.minute
        if self.hour < 10:
            self.hour = '0' + str(self.hour)
        if self.minute < 10:
            self.minute = '0' + str(self.minute)
        # Do other stuff
        self.musicX.logic(deltaTime)
        # Update Circle Smart position
        self.circleCenter[0].logic(deltaTime)
        self.circleCenter[1].logic(deltaTime)
        if self.activeButton == None or self.activeButton == 0:
            self.circleCenter[0].reset()
            self.circleCenter[1].reset()


        for button in self.buttons:
            button.logic(deltaTime)

        if self.updating:
            self.updating = False
            self.update()
        now = datetime.now()
        n = now - self.lastEvent
        if n.total_seconds() > 5:
            if not self.activeButton == None:
                self.deactivateButton()
                self.lastEvent = now
            else:
                self.animateCircleAngle -= 0.1
                if self.animateCircleAngle < 0:
                    self.animateCircleAngle = 360
                if self.animateCircleAngle < 270 and self.animateCircleAngle > 90:
                    self.animateCircleAngle = 90
                x = self.circleCenter[0].getValue() + self.circleRadius*cos(pi*self.animateCircleAngle/180)
                y = self.circleCenter[1].getValue() + self.circleRadius*sin(pi*self.animateCircleAngle/180)
                animatePos = (int(x), 480-int(y))
                pygame.draw.circle(self.skrn, Color.Primary, animatePos, 5, 0) 
        else:
            self.animateCircleAngle = 90

    def event(self, event):
        self.lastEvent = datetime.now()
        if event == 'Swipe Right':
            self.buttons[0].event(event)
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < 250:
                if not self.activeButton == None:
                    self.deactivateButton()
        
        for button in self.buttons[1:]:
            button.event(event)
        if not self.showMusicControls:
            self.buttons[0].event(event)
    def setActive(self, button):
        if self.activeButton == None:    
            if button < len(self.buttons):
                if button == 4:
                    pygame.quit()
                    sys.exit()
                elif button == 3:
                    self.updateStatus()
                elif button == 0:
                    self.setMusic()
                else:
                    self.showMusicControls = False
                    self.activeButton = button
                    self.circleCenter[0].setTarget(-240-435)
                    self.buttons[button].setActive()
            else:
                # Should never happen
                print('SoMeThInG wEnT WrOnG')
                pass
        else:
            self.deactivateButton()
    def deactivateButton(self):
        if not self.activeButton == None:
            for button in self.buttons:
                button.deactivate()
            self.activeButton = None
    def getActiveButton(self):
        return self.activeButton   
    def updateStatus(self):
        self.updating = True
        self.buttons[3].text = 'Updating...'
    def update(self):
        now = datetime.now()
        while now.microsecond > 100000:
            now = datetime.now()
        call(['git', 'pull', 'origin', 'master'])
        self.buttons[3].text = 'Up to date!'
    def setMusic(self):
        self.activeButton = 0
        for button in self.buttons:
            button.xOffset.setTarget(-400)
        self.buttons[0].L.setTarget(len(self.buttons[0].text)*30)
        self.buttons[0].xOffset.setTarget(0)

    def musicLeft(self):
        self.showMusicControls = True
        self.musicX.setTarget(215)
    def musicRight(self):
        self.showMusicControls = False
        self.musicX.reset()