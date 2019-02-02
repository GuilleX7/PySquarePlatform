import pygame
import resManager
from states import state, errorstate
from entities import player, world

class mainState(state.State):
    def create(self):
        self.ctx = pygame.display.get_surface()

        #To be changed
        mapFile = resManager.getVar("MAPFILE")

        request = resManager.loadJSONFile(mapFile)
        if request[0] == resManager.DIE:
            resManager.setVar("ERROR_INFO", "unable to load map file")
            return errorstate.errorState
        
        data = request[1]

        self.world = world.World(
            data["world"]["map"], background=data["world"]["background"], gravity=data["world"]["gravity"]
        )
        self.player = player.Player(
            self.world,
            data["player"]["position"], instantSpeed=(data["player"]["speed"], data["player"]["jumpspeed"])
        )

        self.world.create()
        self.world.camera.setFreely(data["camera"]["freely"])
        self.world.camera.track(self.player)
    
    def update(self):
        self.player.update()
        self.world.camera.update()
    
    def draw(self):
        offset = self.world.camera.getOffset()
        self.world.draw(self.ctx, offset)
        self.player.draw(self.ctx, offset)
        pygame.display.update()