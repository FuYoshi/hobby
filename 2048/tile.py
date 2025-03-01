#!/usr/bin/python
"""
Filename: tile.py
Authors: Yoshi Fu
Project: 2048 Game
Date: October 2022

Summary:
This module implements a Tile class for the 2048 game.
"""

import random
from dataclasses import dataclass

from pygame import Color

INVALID = -1
EMPTY = 0


color_dict = {EMPTY: Color(255, 255, 255)}


@dataclass
class Tile:
    """Class for keeping track of the number on a tile on the board."""

    row: int = INVALID
    col: int = INVALID
    val: int = EMPTY

    def __str__(self) -> str:
        return str(self.val)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tile):
            return other.val == self.val and self.val != EMPTY
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Tile):
            return self.val > other.val
        raise TypeError("Only Tile objects or int can be compared")

    def set_value(self, new_value: int = EMPTY) -> None:
        """Set the value of the tile."""
        self.val = new_value

    def get_color(self) -> None:
        """Get the color of the tile."""
        if self.val not in color_dict:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color_dict[self.val] = Color(r, g, b)
        return color_dict[self.val]

    def is_valid(self) -> bool:
        """Check if the tile is valid."""
        return self.row != INVALID and self.col != INVALID

    def is_empty(self) -> bool:
        """Check if the tile is empty."""
        return self.val == EMPTY

    def not_empty(self) -> bool:
        """Check if the tile is not empty."""
        return not self.is_empty()

    def index_of(self, direction: str) -> (int, int):
        """Get the index of the tile neighbouring this one."""
        if direction == "w":
            return self._w()
        if direction == "a":
            return self._a()
        if direction == "s":
            return self._s()
        if direction == "d":
            return self._d()

    def _w(self) -> (int, int):
        return self.row - 1, self.col

    def _a(self) -> (int, int):
        return self.row, self.col - 1

    def _s(self) -> (int, int):
        return self.row + 1, self.col

    def _d(self) -> (int, int):
        return self.row, self.col + 1
