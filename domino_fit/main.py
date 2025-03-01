#!/usr/bin/python
"""
Filename: main.py
Authors: Yoshi Fu
Project: Domino Fit Game
Date: March 2024

Summary:
TODO
"""


import sys

import pygame as pg

from board import Board

WINDOW_W = 600
WINDOW_H = 600


def main() -> None:
    """Setup, draw and start the game."""
    pg.init()
    pg.display.set_caption("Domino Fit")
    screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pg.time.Clock()
    running = True

    board = Board(screen)

    while running:
        board.draw()
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_r:
                    board.reset()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    row = (event.pos[1] - board.offset) // board.tile_size
                    col = (event.pos[0] - board.offset) // board.tile_size
                    board.place_tile(row, col)
                if event.button == 3:
                    board.toggle_tile()
        clock.tick(60)  # limits FPS to 60

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
