import pygame as pg

from Asteroid import Asteroid
from Ship import Ship

SIZE =(800, 600)

class Game():

    asteroidList = []
    positionShip = []
    positionShip = []

    def __init__(self, w, h):
        self.pantalla = pg.display.set_mode((SIZE))
        self.reloj = pg.time.Clock() 
         
    def init(self):
        pg.init()

    def initGame(self):
        self.initAsteroidList()
        pg.init()
        ship = Ship(SIZE[1])
        game_over = False
        pause = False
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

                self.pantalla.fill((0, 0, 0))

                self.positionShip = (ship.x + ship.w, ship.y)

                for asteroid in self.asteroidList:
                    if self.positionShip[0] == asteroid.x and self.positionShip[1] == asteroid.y:
                        pause = not pause
                    asteroid.update()   
                    pg.draw.rect(self.pantalla, asteroid.color, pg.Rect(asteroid.x, asteroid.y, asteroid.w, asteroid.h))

                ship.update()
                pg.draw.rect(self.pantalla, ship.color, pg.Rect(ship.x, ship.y, ship.w, ship.h))
                
                pg.display.flip()

        pg.quit()

    def initAsteroidList(self):
        for i in range(5):
            asteroid = Asteroid( 20, 20, SIZE, i, 5)
            self.asteroidList.append(asteroid)
       
juego = Game(800, 600)
juego.initGame()       