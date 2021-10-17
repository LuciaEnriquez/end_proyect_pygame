import pygame as pg
from pygame.draw import rect
import os
from Asteroid import Asteroid
from SpaceShip import SpaceShip
from UtilsDataBase import UtilsDataBase

SIZE =(800, 600)

class Game():

    lives = 2
    asteroidList = []
    asteroidDeleteList = []
    numNextLevel = 600
    nextLevel = numNextLevel
    numCountLevel = 100
    countLevel = numCountLevel
    deleteLevelAsteroid = 6
    resourcesDir = os.getcwd()+ "/game/resources/"
    image = pg.image.load(os.path.join(resourcesDir, "asteroid.png"))
    imageSpaceShip = pg.image.load(os.path.join(resourcesDir, "spaceship.png"))
    score = 0
    count = 0

    def __init__(self, w, h):
        self.window = pg.display.set_mode((w, h))
        self.reloj = pg.time.Clock() 
         
    def init(self):
        pg.init()

    def initGame(self):
        self.addAsteroidList()
        pg.init()
        pg.font.init()
        pg.mixer.init()
        explosion = pg.mixer.Sound(os.path.join(self.resourcesDir, "explosion.mp3"))
        font = pg.font.SysFont("corbel", 30)  
        spaceShip = SpaceShip(SIZE[1], self.imageSpaceShip)
        game_over = False
        pause = False
        while not game_over:
            self.reloj.tick(50)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    game_over = True
                elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_p]:
                    if self.lives > 0:
                        pause = not pause
                elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_r] and self.lives <= 0:
                    self.resetGame()
                    pause = False

            if pause == False:
                if pg.key.get_pressed()[pg.K_DOWN]:
                        spaceShip.moveToDown()
                elif pg.key.get_pressed()[pg.K_UP]:
                        spaceShip.moveToUp()

                self.window.fill((0, 0, 0))  

                self.textScore(self.score, font)
                self.textLevel(font)
                levelNow = int(self.nextLevel / self.numNextLevel)
                if self.count >= self.nextLevel:
                    print("level" , levelNow)
                    self.nextLevel += self.numNextLevel

                if self.count >= self.countLevel and levelNow < 7:
                    self.countLevel += self.numCountLevel
                    self.addAsteroidList()

                self.count += 1

                spaceShip.update()
                self.window.blit(spaceShip.image, (spaceShip.x, spaceShip.y))

                cont = 3
                for asteroid in self.asteroidList:
                    if ((spaceShip.x <= asteroid.x) and (spaceShip.x + spaceShip.w) >= asteroid.x) and ((spaceShip.y - asteroid.h) <= asteroid.y and ((spaceShip.y + asteroid.h) >= asteroid.y)) :
                        pg.mixer.Sound.play(explosion)
                        self.asteroidDeleteList.append(asteroid)
                        if self.lives <= 0:
                            pause = True
                            self.textOverGame(font)
                            utilsDataBase.insertPointsAndLevel(self.score, int(levelNow))
                        else:
                            self.lives -= 1
                        continue

                    if asteroid.x <= (  -asteroid.w * 2):
                        self.asteroidDeleteList.append(asteroid)

                    if levelNow > self.deleteLevelAsteroid and cont > 0:
                        asteroid.setDelete()
                    elif levelNow > self.deleteLevelAsteroid and cont <= 0:
                        self.deleteLevelAsteroid = levelNow

                    cont -= 1

                    if asteroid.update():
                        self.score += 15
                    self.window.blit(asteroid.image, (asteroid.x, asteroid.y))
                
                for asteroid in self.asteroidDeleteList:
                    self.asteroidList.remove(asteroid)
                
                self.asteroidDeleteList = []
                
                pg.display.flip()

        pg.quit()


    def textOverGame(self, font):
        textOverGame = font.render('GAME OVER', True, (255, 255, 255))
        textReset = font.render('Pulsa \'R\' para comenzar de nuevo', True, (255, 255, 255))
        self.window.blit(textOverGame, textOverGame.get_rect(center = self.window.get_rect().center))
        self.window.blit(textReset, (SIZE[0]/2, SIZE[1] + 55))

    def textScore(self, points, font):
        string = "PUNTOS: " + str(points)
        text = font.render(string, True, (255, 255, 255))
        self.window.blit(text, (20, SIZE[1] + 20))

    def textLevel(self, font):
        string = "LEVEL: " + str(self.nextLevel / self.numNextLevel)
        text = font.render(string, True, (255, 255, 255))
        self.window.blit(text, (20, SIZE[1] + 55))

    def addAsteroidList(self):
        asteroid = Asteroid(SIZE, self.image)
        self.asteroidList.append(asteroid)

    def resetGame(self):
        self.lives = 2
        self.asteroidList = []
        self.asteroidDeleteList = []
        self.nextLevel = self.numNextLevel
        self.countLevel = self.numCountLevel
        self.deleteLevelAsteroid = 6
        self.addAsteroidList()
        self.addAsteroidList()
        self.score = 0
        self.count = 0
       
juego = Game(800, 700)
utilsDataBase = UtilsDataBase
#utilsDataBase.deleteTable()
utilsDataBase.createTableIfNotExits()
utilsDataBase.selectAllTable()
juego.addAsteroidList()
juego.initGame()   