#-*- coding: utf-8 -*-

import pygame

class Sprite(pygame.Rect):
    def __init__(self, img, pos, size=(0, 0), colorKey=None):
        super().__init__(pos, size)
        self.img = img

        if size == (0, 0):
            self.size = self.img.get_size()
        else:
            self.size = size
            
        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey(colorKey)
        self.surface.convert()
        self.surface.blit(self.img, (0, 0))

    def draw(self, ctx, offset=(0, 0)):
        ctx.blit(self.surface, self.move(offset))