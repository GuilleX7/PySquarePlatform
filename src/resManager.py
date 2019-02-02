import pygame
import os
import json

if os.path.basename(os.getcwd()) == "src":
    folder = "../res/"
else:
    folder = "./res/"

img = dict()

def getPath(uri):
    return folder + uri

def loadImgs(uris):
    for idx, uri in uris:
        loadImg(idx, uri)

def loadImg(idx, uri):
    img[idx] = pygame.image.load(getPath(uri))
    img[idx].convert() #Quicker drawing!

def getImg(id):
    return img[id]

def loadData(uri):
    with open(getPath(uri)) as f:
        data = json.load(f)
        
    return data