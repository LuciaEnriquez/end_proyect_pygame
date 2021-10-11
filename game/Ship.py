class Ship():

    def __init__(self, size, color=(255, 255, 255)):
        self.x = 0
        self.y = size / 2
        self.w = 50
        self.h = 25
        self.size = size - self.h
        self.color = color
        self.top = False
        self.bottom = False

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
