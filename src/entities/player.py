#-*- coding: utf-8 -*-

import pygame
import resManager
from basic import axis

class Player(pygame.Rect):
    def __init__(self, world, pos=[0,0], instantSpeed=(4, 10), color=[0, 0, 0]):
        pygame.Rect.__init__(self, pos, world.tilesize)
        self.root = world
        self.instantSpeed = instantSpeed
        self.color = color
        
        self.maxSpeed = (0, 20)
        self.speed = [0, 0]
        self.state = {
            "jumping": False,
            "falling": False
        }
    
    def update(self):
        self.handleMovement()
        self.checkCollisions()

    def handleMovement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed[0] = -self.instantSpeed[0]
        elif keys[pygame.K_RIGHT]:
            self.speed[0] = self.instantSpeed[0]
        else:
            self.speed[0] = 0

        if keys[pygame.K_UP] and self.state["jumping"] == self.state["falling"] == False:
            self.jump(self.instantSpeed[1])
            
    def jump(self, jumpSpeed):
        self.state["jumping"] = True
        self.speed[1] = -jumpSpeed
        resManager.playSound("jump")

    def checkCollisions(self):
        ghost = self.move(self.speed[0], 0)
        blocks = self.root.tree.zone(ghost)
        collision = ghost.collidelist(blocks)
        if collision == -1:
            self.x = ghost.x
        else:
            block = blocks[collision]
            if axis.isLeftR(self, block):
                axis.setLeftR(self, block)
                self.speed[0] = 0
                #Dispatch block event
                block.onCollisionWithPlayer(self, "l")
            elif axis.isRightR(self, block):
                axis.setRightR(self, block)
                self.speed[0] = 0
                #Dispatch block event
                block.onCollisionWithPlayer(self, "r")

        ghost = self.move(0, self.speed[1])
        collision = ghost.collidelist(blocks)
        if collision == -1:
            self.y = ghost.y
            self.speed[1] = min(self.speed[1] + self.root.gravity, self.maxSpeed[1])
            if self.state["jumping"]:
                if self.speed[1] <= 0:
                    self.state["jumping"] = False
                    self.state["falling"] = True
            else:
                self.state["falling"] = True
        else:
            block = blocks[collision]
            if axis.isUpR(self, block):
                axis.setUpR(self, block)
                self.speed[1] = self.root.gravity
                self.state["falling"] = False
                #Dispatch block event
                block.onCollisionWithPlayer(self, "u")
            elif axis.isDownR(self, block):
                axis.setDownR(self, block)
                self.speed[1] = self.root.gravity
                self.state["falling"] = True
                self.state["jumping"] = False
                #Dispatch block event
                block.onCollisionWithPlayer(self, "d")

    def draw(self, ctx, offset=(0,0)):
        pygame.draw.rect(ctx, self.color, self.move(offset))