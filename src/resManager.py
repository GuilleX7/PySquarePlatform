#-*- coding: utf-8 -*-

import pygame
import os
import json
import re

if os.path.basename(os.getcwd()) == "src":
    folder = "../res/"
else:
    folder = "./res/"

_res = {
    "img": dict(),
    "font": dict(),
    "var": dict()
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

def loadImgs(uris):
    for idx, uri in uris:
        loadImg(idx, uri)

def getImg(id):
    return _res["img"][id]

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
    