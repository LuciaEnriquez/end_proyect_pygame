import pygame as pg
import os

from pygame import image

class SpaceShip():

    resourcesDir = os.getcwd()+ "/game/resources/"
    status = ["MOVE", "DECLINE", "STOP"]
    isStatus1Ok = False

    def __init__(self, size, image):
        self.x = 0
        self.y = size / 2
        self.w = 50
        self.h = 40
        self.image = pg.transform.scale(image, (50, 40))
        self.size = size - self.h
        self.color = (255, 255, 255)
        self.top = False
        self.bottom = False
        self.rotation = 0

    def update(self):
        if self.y <= 0:
            self.top = True
        else:
            self.top = False
            
        if self.y >= self.size:
            self.bottom = True
        else:
            self.bottom = False

    def moveToUp(self):
        if(self.top == False):
            self.y -= 5

    def moveToDown(self):
        if(self.bottom == False):
            self.y += 5

    def reset(self):
        self.isStatus1Ok = False
        self.w = 50
        self.h = 40
        self.rotation = 0
        self.image = pg.image.load(os.path.join(self.resourcesDir, "spaceship.png"))
        self.image = pg.transform.scale(self.image, (50, 40))
        self.x = 0
        self.y = self.size / 2 + self.h / 2

    def moveToRight(self, xPlanet, slowSeep):
        self.w = 50
        self.h = 50
        positionY = self.size / 2 + self.h / 2
        if self.y >= positionY + 8:
            self.y -= 8
        elif self.y <= positionY - 8:
            self.y += 8
        else:
            self.y = positionY
        if xPlanet != self.x - self.w:
            if (slowSeep >= self.x):
                self.x += 6
            elif self.rotation < 180:
                self.rotation += 45
                imageName = "spaceship" + str(self.rotation)+ ".png"
                self.image = pg.image.load(os.path.join(self.resourcesDir, imageName))
                self.image = pg.transform.scale(self.image, (50, 50))
                self.x += 6
            else:
                self.x +=1
                if self.x - self.w == xPlanet - 60:
                    return self.status[1]
        else:
            return self.status[2]        

        return self.status[0]
                

