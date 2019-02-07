#-*- coding: utf-8 -*-

import pygame
import resManager
from os import path
from states import state, mainstate
from basic.ui import container, listbox
from basic import sprite, text


class LoadState(state.State):
    def create(self):
        self.ctx = pygame.display.get_surface()
        
        self.background = sprite.Sprite(resManager.getImg("bg-default"), [0, 0])
        
        self.title = text.Text("Select a map", resManager.loadSystemFont(None, 40), [0, 50])
        self.title.center()
        self.instructions = text.Text("ARROWS to move, ENTER to choose, F5 to refresh files", resManager.loadSystemFont(None, 20), [0, 400])
        self.instructions.center()
        
        self.container = container.Container()
        self.listbox = self.container.add("listbox1", listbox.ListBox([110, 90], 500, maxVisibleItems=10, bgColor=(150, 150, 150)))
        self.refresh()
       
        pygame.key.set_repeat(300, 100)
        
    def refresh(self):
        BASEPATH = "map"
        self.listbox.clear()
        for file in resManager.listFiles(BASEPATH, "json"):
            self.listbox.addItem(path.join(resManager.getPath(BASEPATH), file), file, bgColor=(200, 200, 200), focusColor=(255, 255, 255))
        
    def update(self):
        if self.listbox.peek():
            filepath = self.listbox.poll()
            resManager.setVar("MAPFILE", filepath)
            return mainstate.MainState
                
    def draw(self):
        self.background.draw(self.ctx)
        self.title.draw(self.ctx)
        self.instructions.draw(self.ctx)
        self.container.draw(self.ctx)
        pygame.display.update()
        
    def handle(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_F5:
                self.refresh()
                return
            
            self.container.handle(e)