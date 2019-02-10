#-*- coding: utf-8 -*-

import pygame
import os
import json
import re
from basic.animation import Animation

if os.path.basename(os.getcwd()) == "src":
    folder = "../res/"
else:
    folder = "./res/"

_res = {
    "img": dict(),
    "sound": dict(),
    "font": dict(),
    "var": dict(),
    "anim": dict()
}

#Constants
OK = 0
DIE = 1

#File functions
def getPath(uri):
    return folder + uri

def listFiles(folder, extension=None):
    path = getPath(folder)
    if extension == None:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and
                 re.fullmatch(r".+\.{}".format(extension), f)]
        
    return files

#Image functions
def loadImg(idx, uri):
    _res["img"][idx] = pygame.image.load(getPath(uri))
    _res["img"][idx].convert() #Quicker drawing!

def loadImgs(data):
    for idx, uri in data:
        loadImg(idx, uri)

def getImg(idx):
    return _res["img"][idx]

#Sound functions
def loadSound(idx, uri):
    _res["sound"][idx] = pygame.mixer.Sound(getPath(uri))
    
def loadSounds(data):
    for idx, uri in data:
        loadSound(idx, uri)

def getSound(idx):
    return _res["sound"][idx]

def playSound(idx, loops=0, maxtime=0, fade_ms=0):
    getSound(idx).play(loops, maxtime, fade_ms)

#JSON File functions
def loadJSONFile(uri):
    try:
        with open(getPath(uri)) as f:
            data = json.load(f)
            status = OK
    except Exception:
        data = None
        status = DIE

    return (status, data)

#Font functions
def getFontId(name, size, bold=False, italic=False):
    return "{0}-{1}-{2}{3}".format(str(name).lower(), str(size), str(int(bold)), str(int(italic)))

def loadSystemFont(name, size, bold=False, italic=False):
    idx = getFontId(name, size, bold, italic)
    if _res["font"].get(idx) == None:
        _res["font"][idx] = pygame.font.SysFont(name, size, bold, italic)
    return _res["font"][idx]

def loadFileFont(uri, name, size, bold, italic):
    idx = getFontId(name, size, bold, italic)
    if _res["font"].get(idx) == None:
        _res["font"][idx] = pygame.font.Font(getPath(uri), size)
    return _res["font"][idx]

#Variables-over-states functions
def setVar(idx, value):
    _res["var"][idx] = value
    
def getVar(idx):
    return _res["var"].get(idx, None)

#Synchronized animation functions
def createSyncAnimation(idx, img, tw, th, ticksPerFrame=3, colorKey=None):
    _res["anim"][idx] = Animation(img, tw, th, ticksPerFrame, colorKey)
    
def getSyncAnimation(idx):
    return _res["anim"].get(idx, None)

def updateSyncAnimations():
    for anim in _res["anim"].values():
        anim.update()