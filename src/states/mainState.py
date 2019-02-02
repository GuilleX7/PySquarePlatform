import pygame
import json
import resManager
from states.state import State
from entities import player, world

class mainState(State):
    def __init__(self):
        self.ctx = pygame.display.get_surface()

        data = resManager.loadData("map/initialLevel.json")

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