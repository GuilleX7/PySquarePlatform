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
from states import mainState
import resManager

def main():
    SIZE, FPS = (720, 480), 60

    pygame.init()
    pygame.display.set_mode(SIZE)
    pygame.display.set_caption("PySquarePlatform")

    icon = pygame.Surface((32, 32))
    icon.fill(pygame.Color(0, 0, 0))
    pygame.display.set_icon(icon)

    resManager.loadImgs([
        ("bg-default", "bg-default.png")
    ])
    state = mainState.mainState()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        while pygame.event.peek():
            e = pygame.event.poll()
            state.handle(e)
            if e.type == pygame.QUIT:
              finished = True

        state.update()
        state.draw()
        clock.tick(FPS)

    pygame.quit()
        
if __name__ == '__main__':
    main()