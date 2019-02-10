#-*- coding: utf-8 -*-

import pygame
import resManager
from states import state, errorstate, loadstate
from entities import player, world

class MainState(state.State):
    def create(self):
        self.ctx = pygame.display.get_surface()

        mapFile = resManager.getVar("MAPFILE")

        request = resManager.loadJSONFile(mapFile)
        if request[0] == resManager.DIE:
            resManager.setVar("ERROR_INFO", "unable to load map file")
            return errorstate.ErrorState
        
        data = request[1]

        try:
            self.world = world.World(
                data["world"]["map"], data["world"]["background"], data["world"]["gravity"]
            )
            self.player = player.Player(
                self.world,
                data["player"]["position"], instantSpeed=(data["player"]["speed"], data["player"]["jumpspeed"])
            )
            
            self.world.create()
            self.world.camera.setFreely(data["camera"]["freely"])
            self.world.camera.track(self.player)
        except Exception:
            resManager.setVar("ERROR_INFO", "invalid map file") #Oops, we've got trouble loading this
            return errorstate.ErrorState
        
        self.quit = False
    
    def update(self):
        if self.quit == True:
            return loadstate.LoadState
        
        self.player.update()
        self.world.camera.update()
    
    def draw(self):
        offset = self.world.camera.getOffset()
        self.world.draw(self.ctx, offset)
        self.player.draw(self.ctx, offset)
        pygame.display.update()
        
    def handle(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.quit = True
