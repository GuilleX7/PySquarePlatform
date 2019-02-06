#-*- coding: utf-8 -*-

import pygame
import resManager

class ListBox(pygame.Rect):
    def __init__(self, pos, width, maxVisibleItems=6, elementHeight=30, fontHeight=20, bgColor=(255, 255, 255)):
        super().__init__((pos), (width, maxVisibleItems * elementHeight))
        self.maxVisibleItems = maxVisibleItems
        self.elementHeight = elementHeight
        self.fontHeight = fontHeight
        self.bgColor = bgColor
        
        self.font = resManager.loadSystemFont(None, fontHeight)
        self.marginLeft = 20
        self.marginTop = self.elementHeight - self.fontHeight
        
        self.selected = None
        self.offset = 0
        self.items = []
        self.signals = []
        
    def getIdx(self, name):
        for idx, item in enumerate(self.items):
            if item.name == name:
                return idx
        
        return None
    
    def getByIdx(self, idx):
        return self.items[idx]
    
    def getByName(self, name):
        for item in enumerate(self.items):
            if item.name == name:
                return item
            
        return None
    
    def length(self):
        return len(self.items)
        
    def hasItems(self):
        return self.length() > 0
        
    def addItem(self, name, text, bgColor=(255, 255, 255), focusColor=(200, 200, 200), textColor=(0, 0, 0)):
        self.items.append(ListBoxItem(self, name, text, bgColor, focusColor, textColor))
        if self.getSelected() == None:
            self.setSelected(self.length() - 1)
            self.updateOffset()
        
    def removeItem(self, name):
        idx = self.getIdx(name)
        if idx == None:
            return 0
        
        if self.getSelected() == idx:
            self.selected = None
    
        self.items.pop(idx)
        
    def clear(self):
        self.selected = None
        self.items = []
        
    def peek(self):
        return len(self.signals) > 0
        
    def poll(self):
        return self.signals.pop(0)
        
    def getSelected(self):
        return self.selected
    
    def setSelected(self, idx):
        oldIdx = self.getSelected()
        if oldIdx != None:
            self.getByIdx(oldIdx).selected = 0
            
        self.selected = idx
        self.getByIdx(idx).selected = 1
        
    def moveSelected(self, delta):
        idx = self.getSelected()
        if idx == None:
            if self.hasItems():
                self.setSelected(0)
                self.updateOffset()
            return
    
        self.setSelected((idx + delta) % self.length())
        self.updateOffset()
        
    def updateOffset(self):
        self.offset = max(self.getSelected() + 1, self.maxVisibleItems) - self.maxVisibleItems
        
    def getVisibleItems(self):
        return self.items[self.offset:self.offset + self.maxVisibleItems]
        
    def draw(self, ctx):
        ctx.fill(self.bgColor, self)
        
        for idx, item in enumerate(self.getVisibleItems()):
            color = [item.bgColor, item.focusColor][item.selected]
            ctx.fill(color, pygame.Rect(self.x, self.y + idx * self.elementHeight,
                                        self.width, self.elementHeight))
            ctx.blit(item.getSurface(), (self.x + self.marginLeft,
                                         self.y + idx * self.elementHeight + self.marginTop))
    
    def handle(self, e):
        if e.key == pygame.K_UP:
            self.moveSelected(-1)
        elif e.key == pygame.K_DOWN:
            self.moveSelected(1)
        elif e.key == pygame.K_RETURN:
            self.signals.append(self.getByIdx(self.getSelected()).name)
                
class ListBoxItem():
    def __init__(self, root, name, text, bgColor, focusColor, textColor):
        self.root = root
        self.name = name
        self.text = text
        self.bgColor = bgColor
        self.focusColor = focusColor
        self.textColor = textColor
        self.selected = 0
        self.render()
        
    def render(self):
        self.surface = self.root.font.render(self.text, True, self.textColor)
        
    def getSurface(self):
        return self.surface
    
    def setText(self, text):
        self.text = text
        self.render()
