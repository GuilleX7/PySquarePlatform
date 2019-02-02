import pygame
import resManager
from states import state, mainstate
from basic.text import Text

class errorState(state.State):
    def create(self):
        self.ctx = pygame.display.get_surface()
        self.ctx.fill((255,50,50))
        
        font = resManager.loadSystemFont(None, 30)
        self.texts = [
            Text("Ooops! Something gone wrong (but don't worry!)", font, [0, 150]),
            Text("The error says: {}".format(resManager.getVar("ERROR_INFO")), font, [0, 190]),
            Text("Press any key to restart the game", font, [0, 230])
        ]
        for text in self.texts:
            text.center()
            text.draw(self.ctx)
            
        pygame.display.update()
        self.restart = False
        
    def update(self):
        if self.restart:
            resManager.setVar("ERROR_INFO", "")
            return mainstate.mainState
        
    def handle(self, e):
        if e.type == pygame.KEYDOWN:
            self.restart = True