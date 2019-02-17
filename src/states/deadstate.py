#-*- coding: utf-8 -*-

import pygame
import resManager
from states import state, loadstate
from basic.text import Text

class DeadState(state.State):
    def create(self):
        self.ctx = pygame.display.get_surface()
        self.ctx.blit(resManager.getImg("bg-dark"), (0, 0))
        
        bigFont = resManager.loadSystemFont(None, 150)
        smallFont = resManager.loadSystemFont(None, 30)
        self.texts = [
            Text("YOU", bigFont, [90, 0], (255, 255, 255)),
            Text("DIED", bigFont, [380, 0], (255, 0, 0)),
            Text("Press ENTER to continue...", smallFont, [0, 0], (255, 255, 255)),
        ]
        for text in self.texts[:2]:
            text.center(False, True)
            text.draw(self.ctx)
        
        self.texts[2].center(True, True, 0, 80)
        self.texts[2].draw(self.ctx)
            
        pygame.display.update()
        self.restart = False
        
    def update(self):
        if self.restart:
            return loadstate.LoadState
        
    def handle(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.restart = True