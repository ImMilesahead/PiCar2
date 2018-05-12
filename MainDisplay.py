from helper import *
from MainMenuItem import *
from subprocess import call
from SmartValue import *
from MediaPlayer import *
from MusicScreen import *
from AlbumManager import *
from Song import *
class MainDisplay:
    def __init__(self, skrn):
        self.skrn = skrn
        self.circleCenter = (SmartValue(-240), SmartValue(240))

        self.circleRadius = 322
        self.updating = False

        self.buttons = []
        self.activeButton = None
        self.showVolumeControl = False
        self.volume = 1
        self.mediaPlayer = MediaPlayer(self)
        self.musicScreen = MusicScreen(self.skrn, self.mediaPlayer)

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
            self.skrn.blit(self.musicImage, (self.musicX.getValue() + self.buttons[0].points[0][0]-50, 80))
        pygame.draw.rect(self.skrn, Color.Background, (self.musicX.getInitPos() + self.buttons[0].points[0][0]-50, 80, 120, 40), 0)
        
        # We wanna draw the buttons first so that we can hide them behind the display
        for button in self.buttons:
            button.draw()
        
        #Draw oval thing
        pygame.draw.circle(self.skrn, Color.Primary, (int(self.circleCenter[0].getValue()), int(self.circleCenter[1].getValue())), self.circleRadius, 3)
        pygame.draw.circle(self.skrn, Color.Background, (int(self.circleCenter[0].getValue()), int(self.circleCenter[1].getValue())), self.circleRadius-1)
        
        # Draw Text
        p1 = (575, 0)
        p2 = (600, 25)
        p3 = (800, 25)
        points = (p1, p2, p3)

        self.musicScreen.draw()
        
        pygame.draw.lines(self.skrn, Color.Primary, False, points, 1)
        text(self.skrn, "S - Interface Mk 2", (600, 0), size=24, color=Color.Text)
        # TODO move ^ somewhere else
        text(self.skrn, self.hour, (self.circleCenter[0].getValue() + 250, self.circleCenter[1].getValue() -40), size=48, color=Color.Text)
        text(self.skrn, self.minute, (self.circleCenter[0].getValue() + 250, self.circleCenter[1].getValue()), size=48, color=Color.Text)
        if self.activeButton == None:
            song = self.mediaPlayer.getCurSong()
            if not song == None:
                songText = 'Now Playing: ' + song.name
                if len(songText) > 30:
                    songText = songText[0:30]
                text(self.skrn, songText, (175, 113), size=12, color=Color.Text)   
        if self.showVolumeControl:
            pygame.draw.rect(self.skrn, Color.Primary, (700, 30, 100, 450), 2)
            pygame.draw.rect(self.skrn, Color.Primary, (702, 480-(450*self.volume), 96, 450*self.volume))
        pygame.draw.circle(self.skrn, Color.Primary, (int(self.buttons[0].f(25+430*self.mediaPlayer.getPercent())), int(25+430*self.mediaPlayer.getPercent())), 3)   
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
        self.musicScreen.logic(deltaTime)
        self.mediaPlayer.logic()

        if self.updating:
            self.updating = False
            self.update()
    def event(self, event):
        self.lastEvent = datetime.now()
        if self.activeButton == 0:
            self.musicScreen.event(event)
        mouse_pos = pygame.mouse.get_pos()
        # Set Pos
        if mouse_pos[0] > 700 and mouse_pos[1] > 25 and self.showVolumeControl:
            self.volume = float(480 - mouse_pos[1])/455
            pygame.mixer.music.set_volume(self.volume)
        if mouse_pos[0] < 600 and mouse_pos[0] > 200 and self.activeButton == None:
            if event == 'Swipe Left':
                self.mediaPlayer.nextSong()
            elif event == 'Swipe Right':
                self.mediaPlayer.prevSong()
        if event == 'Swipe Left' and mouse_pos[0] > 600:
            self.showVolumeControl = True
            print('Volume showing')
        elif event == 'Swipe Right':
            self.buttons[0].event(event)
            if mouse_pos[0] < 150:
                if not self.activeButton == None:
                    self.deactivateButton()
        elif event == 'Tap':
            if mouse_pos[0] < 650:
                self.showVolumeControl = False
                print('Volume hidden')
            if self.showMusicControls:
                if mouse_pos[1] > 75 and mouse_pos[1] < 125:
                    if mouse_pos[0] > 200 and mouse_pos[0] < 230:
                        self.mediaPlayer.prevSong()
                    elif mouse_pos[0] < 285 and mouse_pos[0] > 125:
                        self.mediaPlayer.toggle()
                    elif mouse_pos[0] < 325 and mouse_pos[0] > 285:
                        self.mediaPlayer.nextSong()
        
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
                    self.musicX.reset()
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
            if self.activeButton == 0:
                self.musicScreen.animateOut()
                self.showMusicControls = False
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
        self.musicScreen.animateIn()
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