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

class WorldEntities:
    class BLOCKID:
        AIR = 0
        SOLID = 1

    def __init__(self, root):
        self.root = root
        self.solids = [[] for x in range(self.root.size[0])]

    def createBlock(self, id, x, y):
        if id == self.BLOCKID.SOLID:
            self.solids[x].append(pygame.Rect((x * self.root.tilesize[0], y * self.root.tilesize[1]), self.root.tilesize))

    def draw(self, ctx, offset=(0,0)):
        for grid in self.solids:
            for solid in grid:
                pygame.draw.rect(ctx, (0, 255, 0), solid.move(offset))

class WorldCamera:
    def __init__(self, root, freely=True):
        self.root = root
        self.viewport = resManager.getVar("SIZE")
        self.half = (self.viewport[0] // 2, self.viewport[1] // 2)
        self.limit = (
            self.root.tilesize[0] * self.root.size[0] - self.viewport[0],
            self.root.tilesize[1] * self.root.size[1] - self.viewport[1]
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
    def __init__(self, map, tilesize=(30, 30), background="bg-default", gravity=0.5):
        self.map = map
        self.tilesize = tilesize
        self.background = Sprite(resManager.getImg(background), (0, 0))
        self.gravity = gravity

        self.size = (len(self.map[0]), len(self.map))

        self.entities = WorldEntities(self)
        self.tree = WorldTree(self)
        self.camera = WorldCamera(self)

    def create(self):
        for y, line in enumerate(self.map):
            for x, blockid in enumerate(line):
                self.entities.createBlock(blockid, x, y)

    def draw(self, ctx, offset=(0,0)):
        self.background.draw(ctx)
        self.entities.draw(ctx, offset)