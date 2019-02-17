#-*- coding: utf-8 -*-

from math import sqrt, atan2, cos, sin

isUpR = lambda a, b: a.y + a.height <= b.y
isDownR = lambda a, b: a.y >= b.y + b.height
isLeftR = lambda a, b: a.x + a.width <= b.x
isRightR = lambda a, b: a.x >= b.x + b.width

def setUpR(a, b):
    a.y = b.y - a.height
def setDownR(a, b):
    a.y = b.y + b.height
def setLeftR(a, b):
    a.x = b.x - a.width
def setRightR(a, b):
    a.x = b.x + b.width
    
def getDistanceBetween(a, b):
    return sqrt(pow(b.centerx - a.centerx, 2) + pow(b.centery - a.centery, 2))

def getAngleBetween(a, b):
    return atan2(b.centery - a.centery, b.centerx - a.centerx)

def getDirectionBetween(a, b):
    angle = getAngleBetween(a, b)
    return (cos(angle), sin(angle))