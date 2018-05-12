from helper import *
from SmartValue import *
from Song import *
from AlbumManager import *
import os
from AlbumButton import *

class MusicScreen:
    def __init__(self, skrn, musicPlayer):
        self.skrn = skrn
        self.musicPlayer = musicPlayer
        self.topLeft = (225, 75)
        self.topRight = (525, 75)
        self.botRight = (575, 125)
        self.botLeft = (275, 125)

        songs = [Song(f) for f in os.listdir(CWD + '/Media/Music/')]
        self.albumManager = AlbumManager(songs)
        self.musicPlayer.playPlaylist(self.albumManager.albums[0])
        self.albumButtons = []
        self.buttonHeight = 25
        self.buttonYOffset = 25
        for x in range(len(self.albumManager.albums)):
            p1 = (self.botLeft[0], 100 + self.buttonYOffset + (1+x)*self.buttonHeight + 10*x)
            p2 = (self.topRight[0], 100 + self.buttonYOffset + (1+x)*self.buttonHeight + 10*x)
            p3 = (self.botRight[0], 125 + self.buttonYOffset + (1+x)*self.buttonHeight + 10*x)
            p4 = (self.botLeft[0], 125 + self.buttonYOffset + (1+x)*self.buttonHeight + 10*x)
            self.albumButtons.append(AlbumButton(self.skrn, self, self.albumManager.getAlbum(x).name, (p1, p2, p3, p4), self.setAlbum, x))
        self.yOffset = SmartValue(-150 - (self.buttonHeight+self.buttonYOffset)*len(self.albumButtons))
        self.points = self.getPoints()
        self.animateState = -1


    def draw(self):
        # Draw Header
        pygame.draw.lines(self.skrn, Color.Primary, True, self.points, 2)
        text(self.skrn, 'Albums', (self.points[3][0], self.points[0][1]), size=40, color=Color.Text)
        for button in self.albumButtons:
            button.draw()
    def logic(self, deltaTime):
        self.yOffset.logic(deltaTime)
        self.points = self.getPoints()
        if self.yOffset.getOff() < 2:
            if self.animateState == 1:
                self.yOffset.reset()
                self.yOffset.setValue(self.yOffset.getTarget())
        for button in self.albumButtons:
            button.logic(deltaTime)
    def getPoints(self):
        p1 = (self.topLeft[0], self.topLeft[1] + int(self.yOffset.getValue()))
        p2 = (self.topRight[0], self.topRight[1] + int(self.yOffset.getValue()))
        p3 = (self.botRight[0], self.botRight[1] + int(self.yOffset.getValue()))
        p4 = (self.botLeft[0], self.botLeft[1] + int(self.yOffset.getValue()))
        return (p1, p2, p3, p4)
    def event(self, event):
        for button in self.albumButtons:
            button.event(event)
    def animateIn(self):
        self.animateState = 0
        self.yOffset.setTarget(0)
    def animateOut(self):
        self.animateState = 1
        self.yOffset.setTarget(800)
    def setAlbum(self, album):
        self.musicPlayer.playPlaylist(self.albumManager.getAlbum(album))