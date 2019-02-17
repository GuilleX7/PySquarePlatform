#-*- coding: utf-8 -*-

import pygame
import resManager

class Text:
	def __init__(self, txt, font, pos=[0, 0], color=[0, 0, 0], antialias=False, bgColor=None):
		self.txt = txt
		self.font = font
		self.size = self.font.get_height()
		self.pos = pos
		self.color = color
		self.antialias = antialias
		self.bgColor = None
		self.render()
		
	def render(self):
		self.surface = self.font.render(self.txt, self.antialias, self.color, self.bgColor)
		
	def setText(self, txt):
		self.txt = txt
		self.render()
		
	def setFont(self, font):
		self.font = font
		self.render()
		
	def setColor(self, color):
		self.color = color
		self.render()
		
	def setBgColor(self, bgColor):
		self.bgColor = bgColor
		self.render()
		
	def setAntialias(self, antialias):
		self.antialias = antialias
		self.render()
		
	def setPos(self, pos):
		self.pos = pos
		
	def move(self, x, y):
		self.pos[0] += x
		self.pos[1] += y
		
	def getSize(self):
		return self.surface.get_size()
	
	def getRect(self):
		return pygame.Rect(pos, self.getSize())
	
	def center(self, horizontally=True, vertically=False, xOffset=0, yOffset=0):
		viewport = resManager.getVar("SIZE")
		size = self.getSize()
		newPos = self.pos
		if horizontally:
			newPos[0] = viewport[0] / 2 - size[0] / 2 + xOffset
		if vertically:
			newPos[1] = viewport[1] / 2 - size[1] / 2 + yOffset
			
		self.setPos(newPos)
		
	def draw(self, ctx, offset=(0,0)):
		ctx.blit(self.surface, (self.pos[0] + offset[0], self.pos[1] + offset[1]))