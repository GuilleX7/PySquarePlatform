#-*- coding: utf-8 -*-

class Container:
    def __init__(self):
        self.components = dict()
        self.focusedOn = None
        
    def add(self, name, element, focus=True):
        self.components[name] = element
        if focus:
            self.focus(name)
            
        return self.components[name]
    
    def getByName(self, name):
        return self.components.get(name, None)
    
    def getFocused(self):
        return self.getByName(self.focusedOn)
    
    def removeByName(self, name):
        self.components.pop(name, None)
        
    def focus(self, name):
        self.focusedOn = name
    
    def draw(self, ctx):
        for component in self.components.values():
            component.draw(ctx)
    
    def handle(self, e):
        if self.focusedOn != None:
            self.getFocused().handle(e)