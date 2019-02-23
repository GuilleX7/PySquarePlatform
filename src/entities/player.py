#-*- coding: utf-8 -*-

import pygame
import resManager
from basic import axis
from basic.text import Text
from basic.sprite import Sprite
from entities.world import WorldBlock

class PlayerHUD:
    def __init__(self, root):
        self.root = root
        self.coin = Sprite(resManager.getImg("hud-coin"), [10, 10], colorKey=(255, 255, 255))
        self.scoreText = Text("SCORE: 0", resManager.loadSystemFont(None, 20), [30, 10])
        self.heart = Sprite(resManager.getImg("hud-heart"), [10, 30], colorKey=(255, 255, 255))
        self.lifeText = Text("x 0", resManager.loadSystemFont(None, 20), [30, 30])
        
    def draw(self, ctx):
        self.scoreText.setText("x {0}".format(self.root.score))
        self.lifeText.setText("x {0}".format(self.root.lifes))
        
        self.coin.draw(ctx)
        self.scoreText.draw(ctx)
        self.heart.draw(ctx)
        self.lifeText.draw(ctx)

class Player(pygame.Rect):
    def __init__(self, root, pos=[0,0], instantSpeed=(4, 10), lifes=2, maxLifes=5, maxScore=50):
        pygame.Rect.__init__(self, pos, root.tilesize)
        self.root = root
        self.instantSpeed = instantSpeed
        self.color = (0, 0, 0)
        
        self.lifes = lifes
        self.maxLifes = maxLifes
        self.score = 0
        self.maxScore = maxScore
        self.hud = PlayerHUD(self)
        
        self.maxSpeed = (0, 20)
        self.speed = [0, 0]
        self.state = {
            "jumping": False,
            "falling": False
        }
        
        self.died = False
        self.won = False
        
        self.saveGhost()
        
    def giveScore(self, score):
        self.score += score
        if self.score >= self.maxScore:
            self.giveLifes(self.score // self.maxScore)
            self.score = self.score % self.maxScore
        
    def giveLifes(self, lifes):
        self.lifes += lifes
        if self.lifes > self.maxLifes:
            self.lifes = self.maxLifes
        
    def takeDamage(self, damage=1):
        self.lifes -= damage
        if self.lifes <= 0:
            self.die()
        
    def die(self):
        self.died = True
        self.lifes = 0
        
    def win(self):
        self.won = True

    def hasDied(self):
        return self.died
    
    def hasWon(self):
        return self.won
    
    def saveGhost(self):
        self.oldGhost = self.copy()
    
    def update(self):            
        self.handlePlayerInput()
        self.handleMovement()
        self.checkSpecialCollisions()

    def handlePlayerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed[0] = -self.instantSpeed[0]
        elif keys[pygame.K_RIGHT]:
            self.speed[0] = self.instantSpeed[0]
        else:
            self.speed[0] = 0

        if keys[pygame.K_UP] and self.state["jumping"] == self.state["falling"] == False:
            self.jump(self.instantSpeed[1])
            
    def jump(self, jumpSpeed=None):
        if self.state["jumping"] == True:
            return
        
        if jumpSpeed == None:
            jumpSpeed = self.instantSpeed[1]
        
        self.state["jumping"] = True
        self.speed[1] = -jumpSpeed
        resManager.playSound("jump")

    def handleMovement(self):
        #We'll use this "ghost" in order to know from which side we collided
        self.saveGhost()
        
        #If we've fallen off the world, die instantly
        if self.y >= self.root.realsize[1]:
            self.die()
        
        ghost = self.move(self.speed[0], 0)
        ghostZone = self.root.tree.zone(ghost)
        blocks = self.root.entities.getGroupByZones(WorldBlock.Groups.SOLIDS, ghostZone)
        
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
                
    def checkSpecialCollisions(self):
        selfZone = self.root.tree.zone(self)
        blocks = self.root.entities.getGroupByZones(WorldBlock.Groups.SPECIALS, selfZone)
        collisions = self.collidelistall(blocks)
        for collision in collisions:
            block = blocks[collision]
            #Dispatch block event
            block.onCollisionWithPlayer(self, None)

    def draw(self, ctx, offset=(0,0)):
        pygame.draw.rect(ctx, self.color, self.move(offset))
        self.hud.draw(ctx)