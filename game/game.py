import pygame as pg
from pygame.draw import rect
import os
from Asteroid import Asteroid
from SpaceShip import SpaceShip
from UtilsDataBase import UtilsDataBase
import ModelResults as ModelResults

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
    score = 0
    count = 0
    spaceShip = SpaceShip(SIZE[1], pg.image.load(os.path.join(resourcesDir, "spaceship.png")))

    def __init__(self, w, h):
        self.window = pg.display.set_mode((w, h))
        self.reloj = pg.time.Clock() 
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.explosion = pg.mixer.Sound(os.path.join(self.resourcesDir, "explosion.mp3"))
        self.font = pg.font.SysFont("corbel", 30)  
        self.fontBig = pg.font.SysFont("corbel", 50)  
         
    def init(self):
        pg.init()

    def initGame(self):
        self.addAsteroidList()
        self.menuIsView = False
        game_over = False
        pause = False
        viewMenu = True
        while not game_over:
            self.reloj.tick(50)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    game_over = True
                elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_s]:
                    utilsDataBase.insertPointsAndLevel(40,2)
                    utilsDataBase.insertPointsAndLevel(478,6)
                elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_m]:
                    self.resetGame()
                    pause = False
                    viewMenu = True
                elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_SPACE] and viewMenu == True:
                    self.resetGame()
                    pause = False
                    viewMenu = False
                if viewMenu == False:
                    if event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_p] and self.lives > 0:
                        pause = not pause
                        if pause:
                            self.textPause()
                    elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_r] and self.lives <= 0:
                        self.resetGame()
                        pause = False
            if viewMenu == True:
                self.initMenu()
            else:
                self.menuIsView = False
                if pause == False:
                    if pg.key.get_pressed()[pg.K_DOWN]:
                            self.spaceShip.moveToDown()
                    elif pg.key.get_pressed()[pg.K_UP]:
                            self.spaceShip.moveToUp()

                    self.window.fill((0, 0, 0))  

                    self.textScore(self.score)
                    self.textLevel()
                    levelNow = int(self.nextLevel / self.numNextLevel)
                    if self.count >= self.nextLevel:
                        print("level" , levelNow)
                        self.nextLevel += self.numNextLevel

                    if self.count >= self.countLevel and levelNow < 7:
                        self.countLevel += self.numCountLevel
                        self.addAsteroidList()

                    self.count += 1

                    self.spaceShip.update()
                    self.window.blit(self.spaceShip.image, (self.spaceShip.x, self.spaceShip.y))

                    cont = 3
                    for asteroid in self.asteroidList:
                        if ((self.spaceShip.x <= asteroid.x) and (self.spaceShip.x + self.spaceShip.w) >= asteroid.x) and ((self.spaceShip.y - asteroid.h) <= asteroid.y and ((self.spaceShip.y + asteroid.h) >= asteroid.y)) :
                            pg.mixer.Sound.play(self.explosion)
                            self.asteroidDeleteList.append(asteroid)
                            if self.lives <= 0:
                                pause = True
                                self.textOverGame()
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


    def textOverGame(self):
        textOverGame = self.font.render('GAME OVER', True, (255, 255, 255))
        textReset = self.font.render('Pulsa \'R\' para comenzar de nuevo', True, (255, 255, 255))
        self.window.blit(textOverGame, textOverGame.get_rect(center = self.window.get_rect().center))
        self.window.blit(textReset, (SIZE[0]/2, SIZE[1] + 20))

    def textScore(self, points):
        string = "PUNTOS: " + str(points)
        textClose = self.font.render('Pulsa \'M\' para cerrar y \'P\' para pausar', True, (255, 255, 255))
        text = self.font.render(string, True, (255, 255, 255))
        self.window.blit(text, (20, SIZE[1] + 20))
        self.window.blit(textClose, (SIZE[0]/2, SIZE[1] + 55))

    def textLevel(self):
        string = "LEVEL: " + str(self.nextLevel / self.numNextLevel)
        text = self.font.render(string, True, (255, 255, 255))
        self.window.blit(text, (20, SIZE[1] + 55))

    def textPause(self):
        text = self.font.render("Juego pausado pulse \'P\' para continuar", True, (255, 255, 255))
        self.window.blit(text, text.get_rect(center = self.window.get_rect().center))

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

    def initMenu(self):
        if self.menuIsView == False:
            self.menuIsView = True
            self.window.fill((0, 0, 0)) 
            textWelcome = self.fontBig.render("BIENVENIDO A SearhWorld", True, (255, 255, 255))
            self.window.blit(textWelcome, (int(SIZE[0]/2 - textWelcome.get_rect()[2]/2) , 50))
            textBestScore = self.font.render("Mejores resultados", True, (255, 255, 255))
            self.window.blit(textBestScore, (int(SIZE[0]/2 - textBestScore.get_rect()[2]/2) , 70 + textWelcome.get_rect()[3]))
            positionY1 = 120
            positionY2 = textBestScore.get_rect()[3]
            for modelResults in utilsDataBase.selectAllTable():
                string = "Puntos: " + str(modelResults)
                textScore = self.font.render(string, True, (255, 255, 255))
                self.window.blit(textScore, (int(SIZE[0]/2 - textScore.get_rect()[2]/2) , positionY1 + positionY2))
                positionY1 += 15
                positionY2 += textScore.get_rect()[3]

            textSpace = self.fontBig.render("Pulsa \'ESPACIO\' para comenzar el juego", True, (255, 255, 255))
            self.window.blit(textSpace, (int(SIZE[0]/2 - textSpace.get_rect()[2]/2) , SIZE[1]/3*2))
       
juego = Game(800, 700)
utilsDataBase = UtilsDataBase
#utilsDataBase.deleteTable()
utilsDataBase.createTableIfNotExits()
utilsDataBase.selectAllTable()
juego.addAsteroidList()
juego.initGame()   