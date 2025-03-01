#!/usr/bin/python
"""
Filename: main.py
Authors: Yoshi Fu
Project: 2048 Game
Date: October 2022

Summary:
This script implements the 2048 Game.
"""


import pygame as pg

from board import Board
from settings import Settings

WIDTH, HEIGHT = 600, 650


def get_key() -> pg.event:
    """Get the key that is pressed down."""
    while True:
        event = pg.event.wait()
        if event.type == pg.QUIT:
            return event.type
        if event.type == pg.KEYDOWN:
            return event.key


def main() -> None:
    """Setup, draw and start the game."""
    # pygame setup
    pg.init()
    pg.display.set_caption('2048')
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True
    settings = Settings()

    # Start the game and draw it immediately.
    board = Board(screen, settings)
    screen.fill("grey")
    board.generate_tile()
    board.draw()
    pg.display.flip()

    # Poll for events
    while running:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        key = get_key()
        if key == pg.QUIT:
            running = False
        board.move(key)
        board.generate_tile()
        board.draw()

        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60

    pg.quit()


if __name__ == "__main__":
    main()
