import pygame as pg
from pygame.draw import rect

from Asteroid import Asteroid
from Ship import Ship

SIZE =(800, 600)

class Game():

    asteroidList = []
    asteroidDeleteList = []
    numNextLevel = 400
    nextLevel = numNextLevel
    numCountLevel = 90
    countLevel = numCountLevel
    deleteLevelAsteroid = 7

    def __init__(self, w, h):
        self.window = pg.display.set_mode((w, h))
        self.reloj = pg.time.Clock() 
         
    def init(self):
        pg.init()

    def initGame(self):
        self.addAsteroidList()
        pg.init()
        font = None #pg.font.SysFont("corbel", 30)  
        ship = Ship(SIZE[1])
        game_over = False
        pause = False
        count = 0
        while not game_over:
            self.reloj.tick(50)

            eventos = pg.event.get()
            for evento in eventos:
                if evento.type == pg.QUIT:
                    game_over = True

            if pg.key.get_pressed()[pg.K_p]:
                pause = not pause

            if pause == False:
                if pg.key.get_pressed()[pg.K_DOWN]:
                        ship.moveToDown()
                elif pg.key.get_pressed()[pg.K_UP]:
                        ship.moveToUp()

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

                ship.update()
                pg.draw.rect(self.window, ship.color, pg.Rect(ship.x, ship.y, ship.w, ship.h))

                cont = 3
                for asteroid in self.asteroidList:
                    if ((ship.x <= asteroid.x) and (ship.x + ship.w) >= asteroid.x) and ((ship.y - asteroid.h) <= asteroid.y and ((ship.y + asteroid.h) >= asteroid.y)) :
                        pause = not pause
                        self.textOverGame(font)

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
        image = pg.image.load("/Users/miguel/Documents/Proyectos python/end_proyect_pygame/game/asteroid.png")
        asteroid = Asteroid(SIZE, image)
        self.asteroidList.append(asteroid)
       
juego = Game(800, 700)
juego.initGame()   