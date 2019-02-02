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