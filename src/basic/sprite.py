#-*- coding: utf-8 -*-

import pygame

class Sprite(pygame.Rect):
    def __init__(self, img, pos, size=(0, 0), area=None):
        super().__init__(pos, size)
        self.img = img
        self.x, self.y = pos

        if size == (0, 0):
            self.size = self.img.get_size()
        else:
            self.size = size

        if area == None:
            self.area = pygame.Rect((0, 0), self.size)
        else:
            self.area = area

    def draw(self, ctx, offset=(0,0)):
        ctx.blit(self.img, self, self.area.move(offset))