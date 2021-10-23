import pygame as pg
from pygame import time
from pygame.draw import rect
import os
from Asteroid import Asteroid
from SpaceShip import SpaceShip
from UtilsDataBase import UtilsDataBase
from Planet import Planet

SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game():

    listStatus = ["MENU", "INTRO","JUEGO"]
    listItem = ["NUEVA PARTIDA","BORRAR TODOS LOS RESULTADOS","SALIR"]
    selectListItem = listItem[0]
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
    planet = Planet(SIZE, pg.image.load(os.path.join(resourcesDir, "planet.png")))
    isShowPlanet = False

    def __init__(self, w, h):
        self.window = pg.display.set_mode((w, h))
        self.time = pg.time.Clock() 
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.explosion = pg.mixer.Sound(os.path.join(self.resourcesDir, "explosion.mp3"))
        self.landingSound = pg.mixer.Sound(os.path.join(self.resourcesDir, "landing.mp3"))
        self.font = pg.font.SysFont("corbel", 30)  
        self.fontBig = pg.font.SysFont("corbel", 50)  
         
    def init(self):
        pg.init()

    def initGame(self):
        self.addAsteroidList()
        self.menuIsView = False
        game_over = False
        pause = False
        selectStatus = self.listStatus[0]
        timeInfo = pg.time.get_ticks()
        while not game_over:
            self.time.tick(50)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    game_over = True
                elif event.type == pg.KEYDOWN:
                    lenList = len(self.listItem)
                    indexList = self.listItem.index(self.selectListItem)
                    if pg.key.get_pressed()[pg.K_m]:
                        self.resetGame()
                        pause = False
                        selectStatus = self.listStatus[0]
                    elif (pg.key.get_pressed()[pg.K_SPACE] or pg.key.get_pressed()[pg.K_INSERT]) and selectStatus == self.listStatus[0]:
                        if indexList == 0:
                            self.resetGame()
                            pause = False
                            selectStatus = self.listStatus[1]
                            timeInfo = pg.time.get_ticks()
                        elif indexList == 1:
                            utilsDataBase.resetTable()
                            self.menuIsView = False
                        elif indexList == 2:
                            game_over = True
                            
                    if selectStatus == self.listStatus[2]:
                        if pg.key.get_pressed()[pg.K_p] and self.lives > 0:
                            pause = not pause
                            if pause:
                                self.textPause()
                        elif pg.key.get_pressed()[pg.K_r] and self.lives <= 0:
                            self.resetGame()
                            pause = False
                    else:
                        if pg.key.get_pressed()[pg.K_DOWN] and indexList < lenList - 1:
                            indexList += 1
                            self.selectListItem = self.listItem[indexList]
                            self.menuIsView = False
                        elif pg.key.get_pressed()[pg.K_UP] and indexList > 0:
                            indexList -= 1
                            self.selectListItem = self.listItem[indexList]
                            self.menuIsView = False


            if selectStatus == self.listStatus[0]:
                self.initMenu()
            elif selectStatus == self.listStatus[1]:
                self.initIntro()
                if pg.time.get_ticks() > timeInfo + 10000:
                    self.resetGame()
                    pause = False
                    selectStatus = self.listStatus[2]
            else:
                self.menuIsView = False
                if pause == False:
                    if pg.key.get_pressed()[pg.K_DOWN]:
                            self.spaceShip.moveToDown()
                    elif pg.key.get_pressed()[pg.K_UP]:
                            self.spaceShip.moveToUp()

                    self.window.fill(BLACK)  

                    self.textLevel()
                    levelNow = int(self.nextLevel / self.numNextLevel)
                    if self.count >= self.nextLevel:
                        self.nextLevel += self.numNextLevel

                    if self.count >= self.countLevel and levelNow < (self.deleteLevelAsteroid - 2):
                        self.countLevel += self.numCountLevel
                        self.addAsteroidList()
                    
                    if self.deleteLevelAsteroid <= levelNow:
                        self.isShowPlanet = True

                    self.count += 1

                    self.spaceShip.update()

                    for asteroid in self.asteroidList:
                        if ((self.spaceShip.x <= asteroid.x) and (self.spaceShip.x + self.spaceShip.w) >= asteroid.x) and ((self.spaceShip.y - asteroid.h) <= asteroid.y and ((self.spaceShip.y + asteroid.h) >= asteroid.y)) :
                            pg.mixer.Sound.play(self.explosion)
                            self.asteroidDeleteList.append(asteroid)
                            if self.lives <= 0:
                                pause = True
                                self.textOverGame()
                                self.lives = -1
                                if self.score > 0:
                                    utilsDataBase.insertPointsAndLevel(self.score, int(levelNow))
                            else:
                                self.lives -= 1
                            continue

                        if asteroid.x <= (  -asteroid.w * 2):
                            self.asteroidDeleteList.append(asteroid)

                        if self.isShowPlanet:
                            asteroid.setStop(True)

                        if asteroid.update():
                            self.score += 15
                        self.window.blit(asteroid.image, (asteroid.x, asteroid.y))
                    
                    for asteroid in self.asteroidDeleteList:
                        self.asteroidList.remove(asteroid)
                    
                    self.asteroidDeleteList = []
                    self.textScore(self.score)

                    moveSpaceShip = False
                    if len(self.asteroidList) <= 4 and self.isShowPlanet:
                        moveSpaceShip = self.planet.update()
                        self.window.blit(self.planet.image, (self.planet.x, self.planet.y))

                    if len(self.asteroidList) <= 0 and moveSpaceShip:
                        stateSpaceShip = self.spaceShip.moveToRight(self.planet.x - 100, SIZE[0]/5*3)
                        if stateSpaceShip == SpaceShip.status[1]:
                            pg.mixer.Sound.play(self.landingSound)
                        elif stateSpaceShip == SpaceShip.status[2]:
                            pause = True
                            self.textWonGame()
                            if self.score > 0:
                                utilsDataBase.insertPointsAndLevel(self.score, int(levelNow))
                        
                    self.window.blit(self.spaceShip.image, (self.spaceShip.x, self.spaceShip.y))

            pg.display.flip()

        pg.quit()


    def textOverGame(self):
        textOverGame = self.fontBig.render('GAME OVER', True, WHITE)
        textReset = self.font.render('Pulsa \'R\' para comenzar de nuevo', True, WHITE)
        self.window.blit(textOverGame, textOverGame.get_rect(center = self.window.get_rect().center))
        self.window.blit(textReset, (SIZE[0]/2, SIZE[1] + 20))

    def textWonGame(self):
        textWonGame = self.fontBig.render('¡Enhorabuena has ganado!', True, WHITE)
        self.window.blit(textWonGame, textWonGame.get_rect(center = self.window.get_rect().center))
    
    def textLives(self):
        string = "VIDAS: " + str(self.nextLevel / self.numNextLevel)
        text = self.font.render(string, True, WHITE)
        self.window.blit(text, (20, SIZE[1] + 55))

    def textScore(self, points):
        string = "PUNTOS: " + str(points)
        stringLives = "VIDAS: " + str(self.lives +1)
        textClose = self.font.render('Pulsa \'M\' para cerrar y \'P\' para pausar', True, WHITE)
        text = self.font.render(string, True, WHITE)
        textLives = self.font.render(stringLives, True, WHITE)
        self.window.blit(text, (20, SIZE[1] + 20))
        self.window.blit(textLives, (int(text.get_rect()[2] + 40), SIZE[1] + 20))
        self.window.blit(textClose, (SIZE[0]/2, SIZE[1] + 55))

    def textLevel(self):
        string = "LEVEL: " + str(self.nextLevel / self.numNextLevel)
        text = self.font.render(string, True, WHITE)
        self.window.blit(text, (20, SIZE[1] + 55))

    def textPause(self):
        text = self.font.render("Juego pausado pulse \'P\' para continuar", True, WHITE)
        self.window.blit(text, text.get_rect(center = self.window.get_rect().center))

    def addAsteroidList(self):
        asteroid = Asteroid(SIZE, self.image)
        self.asteroidList.append(asteroid)

    def resetGame(self):
        self.isShowPlanet = False
        self.spaceShip.reset()
        self.planet.reset()
        self.lives = 2
        self.asteroidList = []
        self.asteroidDeleteList = []
        self.nextLevel = self.numNextLevel
        self.countLevel = self.numCountLevel
        self.addAsteroidList()
        self.addAsteroidList()
        self.score = 0
        self.count = 0

    def initIntro(self):
        self.window.fill(BLACK) 
        position = 50
        textPrimary = self.fontBig.render("Intro a SearhWorld", True, WHITE)
        self.window.blit(textPrimary, (int(SIZE[0]/2 - textPrimary.get_rect()[2]/2) , position))
        position += textPrimary.get_rect()[3] + 50
        textSecundary = self.font.render("- Para mover hacia arriba la nave pulsa 'flecha arriba'", True, WHITE)
        self.window.blit(textSecundary, (int(SIZE[0]/2 - textSecundary.get_rect()[2]/2) , position))
        position += textSecundary.get_rect()[3] + 12
        textSecundary = self.font.render("- Para mover hacia abajo la nave pulsa 'flecha abajo'", True, WHITE)
        self.window.blit(textSecundary, (int(SIZE[0]/2 - textSecundary.get_rect()[2]/2) , position))
        position += textSecundary.get_rect()[3] + 12
        textSecundary = self.font.render("- Mientras se incremente el nivel se iran incrementando los asteroides", True, WHITE)
        self.window.blit(textSecundary, (int(SIZE[0]/2 - textSecundary.get_rect()[2]/2) , position))
        position += textSecundary.get_rect()[3] + 12
        textSecundary = self.font.render("- Al final aparecerá un planeta nuevo, si tiene todas tus vidas aterrizaras", True, WHITE)
        self.window.blit(textSecundary, (int(SIZE[0]/2 - textSecundary.get_rect()[2]/2) , position))
        position = SIZE[1]/4*3
        textPrimary = self.fontBig.render("¡Buena suerte!", True, WHITE)
        self.window.blit(textPrimary, (int(SIZE[0]/2 - textPrimary.get_rect()[2]/2) , position))

    def initMenu(self):
        if self.menuIsView == False:
            self.menuIsView = True
            self.window.fill(BLACK) 
            textWelcome = self.fontBig.render("BIENVENIDO A SearhWorld", True, WHITE)
            self.window.blit(textWelcome, (int(SIZE[0]/2 - textWelcome.get_rect()[2]/2) , 50))
            listResults = utilsDataBase.selectAllTable()
            if listResults != []:
                textBestScore = self.font.render("Mejores resultados", True, WHITE)
                self.window.blit(textBestScore, (int(SIZE[0]/2 - textBestScore.get_rect()[2]/2) , 70 + textWelcome.get_rect()[3]))
                positionY1 = 120
                positionY2 = textBestScore.get_rect()[3]
                cont = 1
                for result in listResults:
                    string = str(cont) + "º premio: " + result
                    textScore = self.font.render(string, True, WHITE)
                    self.window.blit(textScore, (int(SIZE[0]/2 - textScore.get_rect()[2]/2) , positionY1 + positionY2))
                    positionY1 += 15
                    positionY2 += textScore.get_rect()[3]
                    cont += 1

            positionSelect = SIZE[1]/4*3
            textSelect = self.font.render("Pulsa 'ESPACIO' para continuar la opcción seleccionada", True, WHITE)
            self.window.blit(textSelect, (int(SIZE[0]/2 - textSelect.get_rect()[2]/2) , positionSelect))
            positionSelect += textSelect.get_rect()[3] + 20
            for item in self.listItem:
                colorSelect = BLACK
                color = WHITE
                if self.selectListItem == item:
                    color = BLACK
                    colorSelect = WHITE
                textNewGame = self.font.render(item, True, color)
                pg.draw.rect(self.window, colorSelect, pg.Rect(int(SIZE[0]/2 - 400/2) , positionSelect,400,textNewGame.get_rect()[3]))
                self.window.blit(textNewGame, (int(SIZE[0]/2 - textNewGame.get_rect()[2]/2) , positionSelect))
                positionSelect += textNewGame.get_rect()[3]
       
juego = Game(800, 700)
utilsDataBase = UtilsDataBase
utilsDataBase.createTableIfNotExits()
utilsDataBase.selectAllTable()
juego.addAsteroidList()
juego.initGame()   