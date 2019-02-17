#-*- coding: utf-8 -*-

import pygame
import resManager
from basic import axis
from entities.world import WorldBlock
from math import ceil

class EnemyFactoryType:
    class Groups:
        ENEMIES = 0
        BULLETS = 1
        _LEN = 2
        
    class Enemies:
        SQUARED = 1

class Enemy(pygame.Rect):
    def __init__(self, root, pos):
        super().__init__(pos, root.world.tilesize)
        self._marked = False
        
    def update(self):
        pass
    
    def draw(self, ctx, offset=(0, 0)):
        pygame.draw.rect(ctx, self.color, self.move(offset))
        
    def remove(self):
        self._marked = True
    
class EnemyFactory:
    def __init__(self, world, target):
        self.world = world
        self.target = target
        self.groups = [[] for i in range(EnemyFactoryType.Groups._LEN)]
        
    def getGroup(self, type):
        return self.groups[type]
        
    def addEnemy(self, enemy):
        self.getGroup(EnemyFactoryType.Groups.ENEMIES).append(enemy)
        
    def addBullet(self, bullet):
        self.getGroup(EnemyFactoryType.Groups.BULLETS).append(bullet)  
    
    def createEnemies(self, data):
        for enemy in data:
            if self.world.getBlockAt((enemy["position"][1], enemy["position"][0])) in WorldBlock.GroupContainers.SOLIDS:
                raise Exception #Error, enemy can't be inside a solid block
            
            realPosition = [
                enemy["position"][0] * self.world.tilesize[0], 
                enemy["position"][1] * self.world.tilesize[1]
            ]
            if enemy["type"] == EnemyFactoryType.Enemies.SQUARED:
                self.addEnemy(Squared(self, realPosition, (enemy["speed"], enemy["jumpSpeed"]), enemy["direction"],
                                      enemy["shootDelay"], enemy["shootDistance"], enemy["shootSpeed"], enemy["shootSize"]))
     
    def updateAndDraw(self, ctx, offset=(0, 0)):
        if self.target == None:
            return 
        
        for group in self.groups:
            markeds = []
            for idx, element in enumerate(group):
                element.update()
                if element._marked == True:
                    markeds.append(idx)
                    pass
                
                element.draw(ctx, offset)
            
            self.sweep(markeds, group)
                
    def sweep(self, markeds, group):
        while len(markeds) > 0:
            idx = markeds.pop()
            group.pop(idx)
            
            
#ENEMIES
class Squared(Enemy):
    def __init__(self, root, pos=[0, 0], instantSpeed=(1, 5), direction=-1, shootDelay=3, shootDistance=200, shootSpeed=4, shootSize=10):
        super().__init__(root, pos)
        self.root = root
        self.type = EnemyFactoryType.Enemies.SQUARED
        self.color = (255, 0, 0)
        
        self.instantSpeed = instantSpeed
        self.direction = direction
        
        self.maxSpeed = (0, 20)
        self.speed = [0, 0]
        self.state = {
            "falling": False
        }
        
        self.gun = SquaredGun(self, shootDelay, shootDistance, shootSpeed, shootSize)
        
        self.calculateMovementSpeed()
        
    def calculateMovementSpeed(self):
        self.speed[0] = self.instantSpeed[0] * self.direction
        
    def jump(self):
        self.speed[1] = -self.instantSpeed[1]
        
    def update(self):
        self.moveAndCheckSolidCollisions()
        self.checkCollisionWithPlayer()
        self.gun.update()
        
    def moveAndCheckSolidCollisions(self):
        ghost = self.move(self.speed[0], 0)
        ghostZone = self.root.world.tree.zone(ghost)
        blocks = self.root.world.entities.getGroupByZones(WorldBlock.Groups.SOLIDS, ghostZone)
        
        collision = ghost.collidelist(blocks)
        if collision == -1:
            self.x = ghost.x
        else:
            block = blocks[collision]
            if axis.isLeftR(self, block):
                axis.setLeftR(self, block)
                self.direction = -1
                self.calculateMovementSpeed()
                #Dispatch block event
                block.onCollisionWithEnemy(self, "l")
            elif axis.isRightR(self, block):
                axis.setRightR(self, block)
                self.direction = 1
                self.calculateMovementSpeed()
                #Dispatch block event
                block.onCollisionWithEnemy(self, "r")
        
        ghost = self.move(0, self.speed[1])
        collision = ghost.collidelistall(blocks)
        if collision == []:
            self.y = ghost.y
            self.speed[1] = min(self.speed[1] + self.root.world.gravity, self.maxSpeed[1])
            self.state["falling"] = True
        else:
            block = blocks[collision[0]]
            if axis.isUpR(self, block):
                axis.setUpR(self, block)
                self.speed[1] = self.root.world.gravity
                self.state["falling"] = False
                #Dispatch block event
                block.onCollisionWithEnemy(self, "u")
            elif axis.isDownR(self, block):
                axis.setDownR(self, block)
                self.speed[1] = self.root.world.gravity
                self.state["falling"] = True
                #Dispatch block event
                block.onCollisionWithEnemy(self, "d")
                
                
    def checkCollisionWithPlayer(self):
        if self.colliderect(self.root.target):
            if axis.isUpR(self.root.target.oldGhost, self):
                self.remove()
                self.root.target.jump(self.root.target.instantSpeed[1])
            else:
                self.root.target.die()
    
    def draw(self, ctx, offset=(0, 0)):
        super().draw(ctx, offset)
        self.gun.draw(ctx, offset)
        
class SquaredGun:
    def __init__(self, enemy, shootDelay, shootDistance, shootSpeed, shootSize):
        self.enemy = enemy
        self.bullets = []
        self.setShootDelay(shootDelay)
        self.setShootDistance(shootDistance)
        self.setShootSpeed(shootSpeed)
        self.setShootSize(shootSize)
        self.enabled = True
        
    def setShootDelay(self, seconds=None):
        if seconds != None:
            if seconds == 0:
                self.shootDelay = 0
                self.enabled = False
            else:
                self.shootDelay = ceil(seconds * resManager.getVar("FPS"))
                
        self.tickCount = self.shootDelay
        
    def setShootDistance(self, distance):
        self.shootDistance = distance
        
    def setShootSpeed(self, speed):
        self.shootSpeed = speed

    def setShootSize(self, size):
        self.shootSize = size
        
    def shoot(self):
        self.enemy.root.addBullet(SquaredGunBullet(self, self.shootSpeed, self.shootSize))
        
    def update(self):
        if not self.enabled:
            return 
        
        self.tickCount -= 1
        if self.tickCount == 0:
            self.setShootDelay()
            if axis.getDistanceBetween(self.enemy, self.enemy.root.target) <= self.shootDistance:
                self.shoot()
            
    def draw(self, ctx, offset=(0, 0)):
        for bullet in self.bullets:
            bullet.draw(ctx, offset)
       
class SquaredGunBullet(pygame.Rect):
    def __init__(self, gun, shootSpeed, size=10):
        super().__init__(
            (gun.enemy.centerx - size / 2, gun.enemy.centery - size / 2),
            (size, size),            
        )
        self.gun = gun
        speed = axis.getDirectionBetween(self.gun.enemy, self.gun.enemy.root.target)
        self.speed = (speed[0] * shootSpeed, speed[1] * shootSpeed)
        self.color = (20, 20, 20)
        self._marked = False
        
    def update(self):
        self.move_ip(self.speed)
        if self.colliderect(self.gun.enemy.root.target):
            self.gun.enemy.root.target.takeDamage()
            self.remove()
        
        if not self.colliderect(self.gun.enemy.root.world.rect):
            self.remove()
        
    def draw(self, ctx, offset=(0, 0)):
        pygame.draw.rect(ctx, self.color, self.move(offset))
        
    def remove(self):
        self._marked = True