from random import randint
from random import seed

class Asteroid():

    def __init__(self, w, h, size, numSection, dividerPageNum, color=(23, 54, 205)):
        seed(1)
        self.x = size[0]-20
        self.y = randint(20, size[1] - 20)
        self.w = w
        self.h = h
        self.numSection = numSection
        self.dividerPageNum = dividerPageNum
        self.size = size
        self.color = color
        self.setYandX(numSection, dividerPageNum)

    def update(self):
        self.x -=5

        if self.x <= self.w:
            self.setYandX(self.numSection, self.dividerPageNum)

    def setYandX(self, numSection, dividerPageNum):
        section = self.size[1] / dividerPageNum
        self.y = randint(section * numSection, section * (numSection+1) - self.h)
        self.x =  randint( self.size[0]-20, self.size[0]+ 150)