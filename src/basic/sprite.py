import pygame

class Sprite(pygame.Rect):
    def __init__(self, img, pos, size=None, area=None):
        super().__init__(pos, (0, 0))
        self.img = img
        self.x, self.y = pos

        if size == None:
            self.size = self.img.get_size()
        else:
            self.size = size

        if area == None:
            self.area = pygame.Rect((0, 0), self.size)
        else:
            self.area = area

    def draw(self, ctx, offset=(0,0)):
        ctx.blit(self.img, self, self.area.move(offset))