import pygame as pg
from pygame.draw import rect
import os
from Asteroid import Asteroid
from SpaceShip import SpaceShip

SIZE =(800, 600)

class Game():

    lives = 2
    asteroidList = []
    asteroidDeleteList = []
    numNextLevel = 400
    nextLevel = numNextLevel
    numCountLevel = 100
    countLevel = numCountLevel
    deleteLevelAsteroid = 6
    resourcesDir = os.getcwd()+ "/game/resources/"
    image = pg.image.load(os.path.join(resourcesDir, "asteroid.png"))
    imageSpaceShip = pg.image.load(os.path.join(resourcesDir, "spaceship.png"))

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
        font = None #pg.font.SysFont("corbel", 30)  
        spaceShip = SpaceShip(SIZE[1], self.imageSpaceShip)
        game_over = False
        pause = False
        count = 0
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
                    count = 0

            if pause == False:
                if pg.key.get_pressed()[pg.K_DOWN]:
                        spaceShip.moveToDown()
                elif pg.key.get_pressed()[pg.K_UP]:
                        spaceShip.moveToUp()

                self.window.fill((0, 0, 0))  

                self.textScore(count, font)
                self.textLevel(font)
                levelNow = int(self.nextLevel / self.numNextLevel)
                if count >= self.nextLevel:
                    print("level" , levelNow)
                    self.nextLevel += self.numNextLevel

                if count >= self.countLevel and levelNow < 7:
                    self.countLevel += self.numCountLevel
                    self.addAsteroidList()

                count += 1

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

                    asteroid.update()   
                    self.window.blit(asteroid.image, (asteroid.x, asteroid.y))
                
                for asteroid in self.asteroidDeleteList:
                    self.asteroidList.remove(asteroid)
                
                self.asteroidDeleteList = []
                
                pg.display.flip()

        pg.quit()


    def textOverGame(self, font):
        print()
        #text = font.render('GAME OVER', True, (255, 255, 255))
        #self.window.blit(text, text.get_rect(center = self.window.get_rect().center))

    def textScore(self, points, font):
        string = "POINTS: " + str(points)
        #text = font.render(string, True, (255, 255, 255))
        #self.window.blit(text, (20, SIZE[1] + 20))

    def textLevel(self, font):
        string = "LEVEL: " + str(self.nextLevel / self.numNextLevel)
        #text = font.render(string, True, (255, 255, 255))
        #self.window.blit(text, (20, SIZE[1] + 55))

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
       
juego = Game(800, 700)
juego.initGame()   