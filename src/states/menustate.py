import pygame
import resManager
from states import state, loadstate
from basic.ui import container, listbox
from basic import sprite, text

class MenuState(state.State):
    def create(self):
        self.ctx = pygame.display.get_surface()
        
        self.background = sprite.Sprite(resManager.getImg("bg-default"), [0, 0])
        
        self.title = text.Text("Main menu", resManager.loadSystemFont(None, 40), [0, 50])
        self.title.center()
        
        self.container = container.Container()
        self.listbox = self.container.add("listbox1", listbox.ListBox([110, 90], 500, maxVisibleItems=10, bgColor=(150, 150, 150)))
        self.listbox.addItem("l", "Load map", bgColor=(200, 200, 200), focusColor=(255, 255, 255))
        self.listbox.addItem("s", "", bgColor=(200, 200, 200), focusColor=(255, 255, 255))
        self.refresh()
        
        pygame.key.set_repeat(300, 100)
    
    def refresh(self):
        if resManager.getVar("SOUND") == True:
            strtmp = "Sound: ON"
        else:
            resManager.setVar("SOUND", False)
            strtmp = "Sound: OFF"
            
        self.listbox.getByIdx(1).setText(strtmp)

    def update(self):
        if self.listbox.peek():
            signal = self.listbox.poll()
            if signal == "l":
                return loadstate.LoadState
            elif signal == "s":
                resManager.setVar("SOUND", not resManager.getVar("SOUND"))
                self.refresh()
    
    def draw(self):
        self.background.draw(self.ctx)
        self.title.draw(self.ctx)
        self.container.draw(self.ctx)
        pygame.display.update()
        
    def handle(self, e):
        if e.type == pygame.KEYDOWN:
            self.container.handle(e)
            
    def destroy(self):
        pygame.key.set_repeat()