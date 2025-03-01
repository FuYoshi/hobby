#!/usr/bin/python
"""
Filename: settings.py
Authors: Yoshi Fu
Project: 2048 Game
Date: October 2022

Summary:
This module implements a Settings class for the 2048 game.
"""

from dataclasses import dataclass

import pygame as pg


@dataclass
class Settings:
    """Class for keeping track of the settings for the 2048 game."""
    size: int = 4
    board_shape: tuple[int] = (size, size)
    tile_size: int = (150, 150)
    font_size: int = 40
    score_size: int = 50
    border_size: int = 10
    pg.font.init()
    font: pg.font = pg.font.SysFont("lucidahandwritingcursief.ttf", font_size)
