class Planet:

    def __init__(self, size, image):
        self.w = 140
        self.h = size[1]
        self.x = size[0] + self.w
        self.y = 0
        self.size = size
        self.image = image
        self.color = (0,0,0)
        self.maxX = size[0] - 130

    def update(self):
        if self.maxX < self.x:
            self.x -= 5
            return False
        return True

    def reset(self):
        self.w = 140
        self.h = self.size[1]
        self.x = self.size[0] + self.w
        self.y = 0
