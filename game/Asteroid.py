import pygame as pg
from random import randint

class Asteroid():

    def __init__(self, size, image):
        self.x = size[0]-20
        self.y = 0
        self.w = 20
        self.h = 20
        self.size = size
        self.color = (255,255,255,0)
        self.image = image
        self.setYandX()
        self.setDimensionAsteroid()
        self.delete = False
        self.speed = randint(2 , 8)

    def update(self):
        self.x -= self.speed

        if self.x <= ( - self.w) and self.delete == False:
            self.setYandX()

    def setDelete(self):
        self.delete = True

    def setYandX(self):
        section = self.size[1]
        self.y = randint(0 , section - self.h)
        self.x = randint( self.size[0], self.size[0] + 300)
        self.setDimensionAsteroid()

    def setDimensionAsteroid(self):
        dimen = randint(20, 40)
        self.image = pg.transform.scale(self.image, (dimen, dimen))
        self.w = dimen
        self.h = dimen