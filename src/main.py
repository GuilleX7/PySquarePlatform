#-*- coding: utf-8 -*-

'''
    A py-videogame about Mario-like squares!
    Copyright (C) 2019  GuilleX7 (guillex7.github.io)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import pygame
import states
import resManager
from states import loadstate

def main():
    #Global constants
    resManager.setVar("SIZE", (720, 480))
    resManager.setVar("FPS", 60)
    resManager.setVar("TITLE", "PySquarePlatform")

    pygame.init()
    pygame.display.set_mode(resManager.getVar("SIZE"), pygame.DOUBLEBUF)
    ctx = pygame.display.get_surface()
    pygame.display.set_caption(resManager.getVar("TITLE"))

    icon = pygame.Surface((32, 32))
    icon.fill(pygame.Color(0, 0, 0))
    pygame.display.set_icon(icon)

    #Load data here
    resManager.loadImgs([
        ("bg-default", "img/bg-default.png")
    ])
    resManager.loadSounds([
        ("jump", "sound/jump.ogg"),
        ("break", "sound/break.ogg"),
        ("listbox_move", "sound/listbox_move.ogg"),
        ("listbox_signal", "sound/listbox_signal.ogg")
    ])
    
    state = changeState(loadstate.LoadState)
    clock = pygame.time.Clock()
    FPS = resManager.getVar("FPS")
    finished = False

    while not finished:
        while pygame.event.peek():
            e = pygame.event.poll()
            state.handle(e)
            if e.type == pygame.QUIT:
              finished = True

        newStateClass = state.update()
        if newStateClass == None:
            state.draw()
        else:
            state = changeState(newStateClass)
            
        clock.tick(FPS)

    pygame.quit()
    
def changeState(stateClass):
    state = stateClass()
    newState = state.create()
    if newState != None:
        return changeState(newState)
    
    return state
        
if __name__ == '__main__':
    main()