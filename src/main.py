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
from states import menustate

def main():
    #Global constants
    resManager.setVar("SIZE", (720, 480))
    resManager.setVar("FPS", 60)
    resManager.setVar("TITLE", "PySquarePlatform")
    resManager.setVar("SOUND", True)
    resManager.setVar("FINISHED", False)

    pygame.init()
    pygame.display.set_mode(resManager.getVar("SIZE"), pygame.DOUBLEBUF)
    ctx = pygame.display.get_surface()
    pygame.display.set_caption(resManager.getVar("TITLE"))
    pygame.mixer.set_num_channels(64)

    icon = pygame.Surface((32, 32))
    icon.fill(pygame.Color(0, 0, 0))
    pygame.display.set_icon(icon)

    #Load data here
    resManager.loadImgs([
        ("bg-default", "img/bg-default.png"),
        ("bg-dark", "img/bg-dark.png"),
        ("coin", "img/coin.png"),
        ("hud-heart", "img/hud-heart.png"),
        ("hud-coin", "img/hud-coin.png"),
        ("ground-spikes", "img/ground-spikes.png"),
        ("flag", "img/flag.png")
    ])
    resManager.loadSounds([
        ("jump", "sound/jump.ogg"),
        ("break", "sound/break.ogg"),
        ("listbox_move", "sound/listbox_move.ogg"),
        ("listbox_signal", "sound/listbox_signal.ogg")
    ])
    resManager.createSyncAnimation("coin", resManager.getImg("coin"), 20, 24, ticksPerFrame=5, colorKey=(255, 255, 255))
    resManager.createImgSurface("ground-spikes", resManager.getImg("ground-spikes"), colorKey=(255, 255, 255))
    resManager.createImgSurface("flag", resManager.getImg("flag"), colorKey=(0, 255, 0))
    
    state = changeState(menustate.MenuState)
    
    clock = pygame.time.Clock()
    FPS = resManager.getVar("FPS")

    while not resManager.getVar("FINISHED"):
        while pygame.event.peek():
            e = pygame.event.poll()
            state.handle(e)
            if e.type == pygame.QUIT:
                resManager.setVar("FINISHED", True)

        resManager.updateSyncAnimations()
        newStateClass = state.update()
        if newStateClass == None:
            state.draw()
        else:
            state.destroy()
            state = changeState(newStateClass)
            
        clock.tick(FPS)

    pygame.quit()
    
def changeState(stateClass):
    state = stateClass()
    newState = state.create()
    if newState != None:
        state.destroy()
        return changeState(newState)
    
    return state
        
if __name__ == '__main__':
    main()