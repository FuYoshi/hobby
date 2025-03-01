#!/usr/bin/python
"""
Filename: board.py
Authors: Yoshi Fu
Project: 2048 Game
Date: October 2022

Summary:
This module implements a Board class for the 2048 game.
"""


import numpy as np
import pygame as pg

from label import Label
from settings import Settings
from tile import Tile

W = "w"
A = "a"
S = "s"
D = "d"


class Board:
    """Class for keeping track of the board state."""

    def __init__(self, screen: pg.Surface, settings: Settings) -> None:
        self.screen = screen
        self.size = settings.size
        self.font = settings.font
        self.shape = settings.board_shape
        self.score_size = settings.score_size
        self.border_size = settings.border_size
        self.tile_size = settings.tile_size

        # Game state
        self.score = 0
        self.high_score = 0
        self.board = self._init_board()

    def __str__(self) -> str:
        string = ""
        for r in range(self.size):
            for c in range(self.size):
                tile = self.board[r, c]
                string += str(tile) + "\t"
            string += "\n"
        return string

    def draw(self) -> None:
        """Draw the game on the screen."""
        self._draw_tiles()
        self._draw_score()

    def generate_tile(self) -> None:
        """Randomly generate a tile on an empty spot on the board."""
        vfunc = np.vectorize(Tile.is_empty)
        empty_tiles = self.board[vfunc(self.board)]
        if len(empty_tiles) > 0:
            empty_tile = np.random.choice(empty_tiles)
            value = 2 if np.random.binomial(1, 0.9) else 4
            empty_tile.set_value(value)

    def reset(self) -> None:
        """Reset the state of the game."""
        self.score = 0
        self.board = self._init_board()

    def move(self, key) -> None:
        """Perform a move in the game."""
        if key == pg.K_r:
            self.reset()
        if self._alive():
            if key == pg.K_w or key == pg.K_UP:
                self._move_tiles(direction=W)
            if key == pg.K_a or key == pg.K_LEFT:
                self._move_tiles(direction=A)
            if key == pg.K_s or key == pg.K_RIGHT:
                self._move_tiles(direction=S)
            if key == pg.K_d or key == pg.K_DOWN:
                self._move_tiles(direction=D)

    def _init_board(self) -> np.ndarray:
        """Initialize the state of the board."""
        board = []
        for r in range(self.size):
            for c in range(self.size):
                board.append(Tile(r, c))
        return np.array(board, dtype=Tile).reshape(self.shape)

    def _draw_tiles(self) -> None:
        w, h = self.tile_size
        for r in range(self.shape[0]):
            for c in range(self.shape[1]):
                # Draw tile.
                tile = self.board[r, c]
                tile_rect = pg.Rect(
                    (c * w + self.border_size, r * h + self.border_size),
                    (w - 2 * self.border_size, h - 2 * self.border_size),
                )
                pg.draw.rect(self.screen, tile.get_color(), tile_rect)

                # Draw text on tiles.
                tile_text = self.font.render(str(tile), True, "white")
                tile_rect = tile_text.get_rect(center=tile_rect.center)
                self.screen.blit(tile_text, tile_rect)

    def _draw_score(self) -> None:
        x = 0 + self.score_size // 2
        y = self.screen.get_height() - self.score_size // 2
        score = Label(
            font=self.font,
            text=f"Score: {self.score}",
            color="white",
            position=(x, y),
            anchor="midleft",
        )
        score.draw(self.screen)

        x = self.size * self.tile_size[0] - self.score_size // 2
        high_score = Label(
            font=self.font,
            text=f"Best: {self.high_score}",
            color="white",
            position=(x, y),
            anchor="midright",
        )
        high_score.draw(self.screen)

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def _get_tile(self, tile: Tile, direction: str) -> Tile:
        other_index = tile.index_of(direction)
        if self._in_bounds(*other_index):
            return self.board[other_index]
        return Tile()

    def _is_movable(self, tile: Tile, direction: str) -> bool:
        other_tile = self._get_tile(tile, direction)
        if not other_tile.is_valid():
            return False
        return other_tile.is_empty() or other_tile == tile

    def _combine_tiles(self, a: Tile, b: Tile):
        a.val, b.val = 0, a.val * 2
        self.score += b.val
        if self.high_score < self.score:
            self.high_score = self.score

    def _swap_tiles(self, a: Tile, b: Tile):
        a.val, b.val = b.val, a.val

    def _move_tile(self, tile: Tile, direction: str) -> None:
        if self._is_movable(tile, direction):
            other_tile = self._get_tile(tile, direction)
            if other_tile.is_valid() and other_tile.not_empty():
                self._combine_tiles(tile, other_tile)
            else:
                self._swap_tiles(tile, other_tile)
                self._move_tile(other_tile, direction)

    def _move_tiles(self, direction: str) -> None:
        vfunc = np.vectorize(Tile.not_empty)
        tiles = self.board[np.where(vfunc(self.board))]
        if direction in [S, D]:
            tiles = np.flip(tiles)

        for tile in tiles:
            self._move_tile(tile, direction)

    def _has_valid_moves(self, tile: Tile) -> bool:
        other_tile = self._get_tile(tile, W)
        if other_tile.is_valid() and other_tile == tile:
            return True
        other_tile = self._get_tile(tile, A)
        if other_tile.is_valid() and other_tile == tile:
            return True
        other_tile = self._get_tile(tile, S)
        if other_tile.is_valid() and other_tile == tile:
            return True
        other_tile = self._get_tile(tile, D)
        if other_tile.is_valid() and other_tile == tile:
            return True
        return False

    def _alive(self) -> bool:
        vfunc = np.vectorize(Tile.is_empty)
        empty_tiles = self.board[vfunc(self.board)]
        if len(empty_tiles) > 0:
            return True

        for r in range(self.size):
            for c in range(self.size):
                tile = self.board[r, c]
                if self._has_valid_moves(tile):
                    return True
        return False
