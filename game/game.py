import pygame as pg
from random import seed
from random import randint

TAMANNO =(800, 600)

class Bola():
    def __init__(self, x, y, w, h, color=(255, 255, 205)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def actualizate(self):
        self.x -=5

        if self.x <= 0:
            self.y = randint(20, TAMANNO[1] - 20)
            self.x = TAMANNO[0]-20

class Game():

    def __init__(self, w, h):
        self.pantalla = pg.display.set_mode((TAMANNO))
        self.reloj = pg.time.Clock() 
         
    def init(self):
        pg.init()

    def bucle_principal(self):
        seed(1)
        bola = Bola(TAMANNO[0]-20, randint(20, TAMANNO[1] - 20), 20, 20)
        pg.init()
        game_over = False
        while not game_over:
            self.reloj.tick(50)

            #eventos = pg.event.get()
            #for evento in eventos:
            #    if evento.type == pg.KEYDOWN:
            #        game_over = True

            

            bola.actualizate()       

            self.pantalla.fill((0, 0, 0))
            pg.draw.rect(self.pantalla, bola.color, pg.Rect(bola.x, bola.y, bola.w, bola.h))

            pg.display.flip()

        pg.quit()
        
        #self.bucle_principal()

       
juego = Game(800, 600)
juego.bucle_principal()       