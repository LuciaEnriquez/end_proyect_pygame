import pygame as pg
from random import randint
from random import seed

class Asteroid():

    def __init__(self, size, image):
        seed(1)
        self.x = size[0]-20
        self.y = randint(20, size[1] - 20)
        self.w = 20
        self.h = 20
        self.size = size
        self.color = (255,255,255,0)
        self.image = image
        self.setYandX()
        self.setDimensionAsteroid()
        self.delete = False

    def update(self):
        self.x -=5

        if self.x <= ( - self.w) and self.delete == False:
            self.setYandX()

    def setDelete(self):
        self.delete = True

    def setYandX(self):
        dividerPageNum = randint(1,6)
        section = self.size[1] / dividerPageNum
        self.y = randint(section , section + section - self.h)
        self.x = randint( self.size[0], self.size[0]+ 150)
        self.setDimensionAsteroid()

    def setDimensionAsteroid(self):
        dimen = randint(20, 40)
        self.image = pg.transform.scale(self.image, (dimen, dimen))
        self.w = dimen
        self.h = dimen