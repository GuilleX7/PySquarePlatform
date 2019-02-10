#-*- coding: utf-8 -*-

import pygame

class Animation:
    def __init__(self, img, tw, th, ticksPerFrame=3, colorKey=None):
        self.img = img
        self.tw = tw
        self.th = th
        self.ticksPerFrame = ticksPerFrame
        self.ticks = 0
        self.frame = 0
        
        self.surface = pygame.Surface((tw, th))
        if colorKey != None:
            self.surface.set_colorkey(colorKey)
        self.surface.convert()

        self.srcSize = self.img.get_size()
        self.dstSize = (tw, th)
        self.frames = [
            pygame.Rect(x * self.tw, y * self.th, self.tw, self.th)
            for x in range(self.srcSize[0] // tw)
            for y in range(self.srcSize[1] // th)
        ]
        self.frameLength = len(self.frames)
        
    def update(self):
        self.ticks = (self.ticks + 1) % self.ticksPerFrame
        if self.ticks == 0:
            self.frame = (self.frame + 1) % self.frameLength
            self.surface.blit(self.img, (0, 0), self.getActualFrame())
            
    def getSrcSize(self):
        return self.srcSize
    
    def getDstSize(self):
        return self.dstSize
    
    def getFrameAt(self, idx):
        return self.frames[idx]
    
    def getFrames(self):
        return self.frames
    
    def getActualFrame(self):
        return self.frames[self.frame]
    
    def getSurface(self):
        return self.surface