#-*- coding: utf-8 -*-

import pygame
import resManager
from basic.sprite import Sprite
from basic.animation import Animation

class WorldTree:
    def __init__(self, root):
        self.root = root
        self.limitX = self.root.size[0] - 1

    def locate(self, rect):
        return rect.x // self.root.tilesize[0]

    def zone(self, rect):
        loc = self.locate(rect)
        if loc < -1 or loc > self.limitX:
            return tuple()
        elif loc != self.limitX:
            return (loc, loc + 1)
        else:
            return (loc, )

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
    class Groups:
        SOLIDS = 0
        SPECIALS = 1
        _LEN = 2
    
    class Types:
        AIR = 0
        SOLID = 1
        SOLID_JUMPY = 2
        SOLID_BREAKY = 3
        SOLID_INVISIBLE = 4
        SPECIAL_COIN = 9
        
    #SOLID classes
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
            elif collisionSide == "d":
                resManager.playSound("break")
                self.remove()
                
    class SOLID_INVISIBLE(WorldBlockBase):
        def __init__(self, pos, size):
            super().__init__(pos, size)
            self.type = WorldBlock.Types.SOLID_INVISIBLE
            self.color = (100, 0, 100)
            self.visible = False
            
        def onCollisionWithPlayer(self, player, collisionSide):
            if collisionSide == "d":
                self.visible = True
            
        def draw(self, ctx, offset=(0, 0)):
            if self.visible:
                WorldBlockBase.draw(self, ctx, offset=offset)
 
    #SPECIAL classes
    class SPECIAL_COIN(WorldBlockBase):
        def __init__(self, pos, size):
            super().__init__((pos[0] + 5, pos[1] + 3), (size[0] - 10, size[1] - 6))
            self.type = WorldBlock.Types.SPECIAL_COIN
            
        def onCollisionWithPlayer(self, player, collisionSide):
            player.score += 1
            #resManager.playSound("coin") #Disabled because it sounds really bad... looking for a fix :(
            self.remove()
                
        def draw(self, ctx, offset=(0, 0)):
            ctx.blit(resManager.getSyncAnimation("coin").getSurface(), self.move(offset))
            
 
class WorldEntities:
    def __init__(self, root):
        self.root = root
        self.groups = [self.initWorldArray() for i in range(WorldBlock.Groups._LEN)]
        
    def initWorldArray(self):
        return [[] for x in range(self.root.size[0])]
    
    def getGroupByZones(self, group, zones):
        result = []
        for zone in zones:
            result += self.groups[group][zone]
        return result
    
    def getAllGroup(self, group):
        return [block
                for block in grid
                for grid in self.groups[group]]
    
    def getAll(self):
        return [block
                for block in grid
                for grid in group
                for group in self.groups]

    def createBlock(self, type, x, y):
        realPosition = (x * self.root.tilesize[0], y * self.root.tilesize[1])
        #SOLIDS
        if type == WorldBlock.Types.SOLID:
            self.groups[WorldBlock.Groups.SOLIDS][x].append(WorldBlock.SOLID(realPosition, self.root.tilesize))
        elif type == WorldBlock.Types.SOLID_JUMPY:
            self.groups[WorldBlock.Groups.SOLIDS][x].append(WorldBlock.SOLID_JUMPY(realPosition, self.root.tilesize))
        elif type == WorldBlock.Types.SOLID_BREAKY:
            self.groups[WorldBlock.Groups.SOLIDS][x].append(WorldBlock.SOLID_BREAKY(realPosition, self.root.tilesize))
        elif type == WorldBlock.Types.SOLID_INVISIBLE:
            self.groups[WorldBlock.Groups.SOLIDS][x].append(WorldBlock.SOLID_INVISIBLE(realPosition, self.root.tilesize))
        #SPECIALS
        elif type == WorldBlock.Types.SPECIAL_COIN:
            self.groups[WorldBlock.Groups.SPECIALS][x].append(WorldBlock.SPECIAL_COIN(realPosition, self.root.tilesize))

    def updateAndDraw(self, ctx, offset=(0,0)):
        for group in self.groups:
            markeds = []
            for gridx, grid in enumerate(group):
                for idx, block in enumerate(grid):
                    if block._marked == True:
                        markeds.append((gridx, idx))
                        pass
                    
                    block.draw(ctx, offset)
                    
            self.sweep(markeds, group)
        
    def sweep(self, markeds, group):
        while len(markeds) > 0:
            gridx, idx = markeds.pop()
            group[gridx].pop(idx) #Say goodbye :(

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
        self.entities.updateAndDraw(ctx, offset)