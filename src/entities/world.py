#-*- coding: utf-8 -*-

import pygame
import resManager
from basic.sprite import Sprite

class WorldTree:
    def __init__(self, root):
        self.root = root
        self.limitX = self.root.size[0] - 1

    def locate(self, rect):
        return rect.x // self.root.tilesize[0]

    def zone(self, rect):
        loc = self.locate(rect)
        if loc < -1 or loc > self.limitX:
            return []
        elif loc != self.limitX:
            return self.root.entities.solids[loc] + self.root.entities.solids[loc + 1]
        else:
            return self.root.entities.solids[loc]

class WorldBlockBase(pygame.Rect):    
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self._marked = False
    
    def draw(self, ctx, offset=(0, 0)):
        pygame.draw.rect(ctx, self.color, self.move(offset))
    
    def onCollisionWithPlayer(self, player, collisionSide):
        pass
    
    def remove(self):
        self._marked = True
    
class WorldBlock:
    #Constants
    class Types:
        AIR = 0
        SOLID = 1
        SOLID_JUMPY = 2
        SOLID_BREAKY = 3
        
    #Block classes
    class SOLID(WorldBlockBase):
        def __init__(self, pos, size):
            super().__init__(pos, size)
            self.type = WorldBlock.Types.SOLID
            self.color = (0, 200, 0)
            
    class SOLID_JUMPY(WorldBlockBase):
        def __init__(self, pos, size):
            super().__init__(pos, size)
            self.type = WorldBlock.Types.SOLID_JUMPY
            self.color = (255, 255, 0)
            
        def onCollisionWithPlayer(self, player, collisionSide):
            if collisionSide == "u":
                player.jump(player.instantSpeed[1] * 2)
                
    class SOLID_BREAKY(WorldBlockBase):
        def __init__(self, pos, size):
            super().__init__(pos, size)
            self.type = WorldBlock.Types.SOLID_BREAKY
            self.color = (100, 100, 100)
            
        def onCollisionWithPlayer(self, player, collisionSide):
            if collisionSide == "u":
                player.jump(player.instantSpeed[1] / 2)
                resManager.playSound("break")
                self.remove()

class WorldEntities:
    def __init__(self, root):
        self.root = root
        self.solids = [[] for x in range(self.root.size[0])]
        self.markeds = []

    def createBlock(self, type, x, y):
        realPosition = (x * self.root.tilesize[0], y * self.root.tilesize[1])
        if type == WorldBlock.Types.SOLID:
            self.solids[x].append(WorldBlock.SOLID(realPosition, self.root.tilesize))
        elif type == WorldBlock.Types.SOLID_JUMPY:
            self.solids[x].append(WorldBlock.SOLID_JUMPY(realPosition, self.root.tilesize))
        elif type == WorldBlock.Types.SOLID_BREAKY:
            self.solids[x].append(WorldBlock.SOLID_BREAKY(realPosition, self.root.tilesize))

    def draw(self, ctx, offset=(0,0)):
        for gridx, grid in enumerate(self.solids):
            for idx, block in enumerate(grid):
                if block._marked == True:
                    self.markeds.append((gridx, idx)) #Mark
                    pass
                
                block.draw(ctx, offset)
                
        self.sweep() #And sweep
        
    def sweep(self):
        while len(self.markeds) > 0:
            gridx, idx = self.markeds.pop()
            self.solids[gridx].pop(idx) #Say goodbye :(

class WorldCamera:
    def __init__(self, root, freely=True):
        self.root = root
        self.viewport = resManager.getVar("SIZE")
        self.half = (self.viewport[0] // 2, self.viewport[1] // 2)
        self.limit = (
            max(self.root.tilesize[0] * self.root.size[0] - self.viewport[0], 0),
            max(self.root.tilesize[1] * self.root.size[1] - self.viewport[1], 0)
        )

        self.setAt([0, 0])
        self.tracking = None
        self.setFreely(freely)

    def setFreely(self, freely):
        self.freely = freely
    
    def track(self, rect):
        self.fixed = False
        self.tracking = rect
    
    def detach(self):
        self.tracking = None

    def setAt(self, pos, fix=False):
        self.fixed = fix
        self.pos = pos

    def centerAt(self, pos, fix=False):
        self.setAt([pos[0] - self.half[0], pos[1] - self.half[1]], fix)

    def getPos(self):
        return self.pos

    def getOffset(self):
        return (-self.pos[0], -self.pos[1])

    def getRect(self):
        return pygame.Rect(self.pos, self.viewport)

    def update(self):
        if self.fixed or self.tracking == None:
            return

        self.centerAt((self.tracking.x, self.tracking.y))

        if not self.freely:
            if self.pos[0] <= 0:
                self.pos[0] = 0
            elif self.pos[0] >= self.limit[0]:
                self.pos[0] = self.limit[0]

            if self.pos[1] <= 0:
                self.pos[1] = 0
            elif self.pos[1] >= self.limit[1]:
                self.pos[1] = self.limit[1]

class World:
    def __init__(self, map, background="bg-default", gravity=0.5, tilesize=(30, 30)):
        self.map = map
        self.background = Sprite(resManager.getImg(background), (0, 0))
        self.gravity = gravity
        self.tilesize = tilesize

        self.size = (len(self.map[0]), len(self.map))

        self.entities = WorldEntities(self)
        self.tree = WorldTree(self)
        self.camera = WorldCamera(self)

    def create(self):
        for y, line in enumerate(self.map):
            if len(line) != self.size[0]: #Line width is not as map width!
                raise Exception
            
            for x, blockid in enumerate(line):
                self.entities.createBlock(blockid, x, y)

    def draw(self, ctx, offset=(0,0)):
        self.background.draw(ctx)
        self.entities.draw(ctx, offset)