import pygame
from helper import *
class AlbumButton:
    def __init__(self, skrn, parent, text, initialPoints, callback=None, args=None):
        self.skrn = skrn
        self.parent = parent
        self.text = text
        if len(self.text) > 15:
            self.text = text[:15]
        self.initialPoints = initialPoints
        self.points = self.initialPoints
        self.callback = callback
        self.args = args
    def draw(self):
        pygame.draw.lines(self.skrn, Color.Text, True, self.points, 2)
        text(self.skrn, self.text, (self.points[0][0]+4, self.points[0][1]+2), size=20, color=Color.Text)
    def logic(self, deltaTime):
        p1 = (self.initialPoints[0][0], self.initialPoints[0][1] + self.parent.yOffset.getValue())
        p2 = (self.initialPoints[1][0], self.initialPoints[1][1] + self.parent.yOffset.getValue())
        p3 = (self.initialPoints[2][0], self.initialPoints[2][1] + self.parent.yOffset.getValue())
        p4 = (self.initialPoints[3][0], self.initialPoints[3][1] + self.parent.yOffset.getValue())
        self.points = (p1, p2, p3, p4)
    def event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.points[0][0] and mouse_pos[0] <= self.points[2][0] and mouse_pos[1] >= self.points[0][1] and mouse_pos[1] <= self.points[2][1]:
            if event == 'Tap':
                if not self.callback == None:
                    if not self.args == None:
                        self.callback(self.args)
                    else:
                        self.callback()
