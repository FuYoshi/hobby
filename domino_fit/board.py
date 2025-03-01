#!/usr/bin/python
"""
Filename: board.py
Authors: Yoshi Fu
Project: Domino Fit Game
Date: March 2024

Summary:
TODO
"""


import numpy as np
import pygame as pg

# Colors.
COLOR_TEXT = "#000000"
COLOR_BG = "#4879a2"
CORRECT = "#03c23e"
WRONG = "#fb0606"

# Text Settings.
FONT = "mvboli"
FONTSIZE = 32

# Board Settings.
BOARD_SIZE = 7
OFFSET = 60

# Tiles.
EMPTY = -1
WALL = -2


class Board:
    """Class to keep track of the state of the board."""

    def __init__(self, screen: pg.Surface) -> None:
        # Game attributes.
        self.size = BOARD_SIZE
        self.board = np.array([EMPTY] * self.size**2)
        self.current_tile = 1
        self.reset()
        self.wizardry = True

        # Pygame attributes.
        self.screen = screen
        self.offset = OFFSET
        self.tile_size = (screen.get_width() - self.offset * 2) // self.size
        self.font = pg.font.SysFont(FONT, FONTSIZE)

        # Sprite attributes.
        self.sprite_domino_one = pg.image.load("./sprites/domino1.png")
        self.sprite_domino_two = pg.image.load("./sprites/domino2.png")
        self.sprite_board = pg.image.load("./sprites/board.png")
        self.sprite_wall = pg.image.load("./sprites/wall.png")

        # Audio attributes.
        self.audio_domino_place = pg.mixer.Sound("./audio/domino_place.mp3")
        self.audio_domino_remove = pg.mixer.Sound("./audio/domino_remove.mp3")
        self.audio_solved = pg.mixer.Sound("./audio/solved.mp3")

    def _place_domino_horizontal(self, row: int, col: int, count: int) -> bool:
        if self._is_valid(row, col) and self._is_valid(row, col + 1):
            # Place the domino horizontally
            self.board[row, col] = count
            self.board[row, col + 1] = count
            if self.place_domino(row, col + 2, count - 1):
                return True
            # Backtrack
            self.board[row, col] = 0
            self.board[row, col + 1] = 2

    def _place_domino_vertical(self, row: int, col: int, count: int) -> bool:
        if self._is_valid(row, col) and self._is_valid(row + 1, col):
            # Place the domino vertically
            self.board[row, col] = count
            self.board[row + 1, col] = count
            if self.place_domino(row, col + 1, count - 1):
                return True
            # Backtrack
            self.board[row, col] = 1
            self.board[row + 1, col] = 0

    def place_domino(self, row: int, col: int, count: int) -> bool:
        """Recursively place dominoes until `count` is reached
        or when no more dominoes can be placed on the board."""
        if count == 0:
            return True

        for i in range(row, self.size):
            for j in range(col, self.size):
                choice = np.random.choice(["horizontal", "vertical"])
                if choice == "horizontal":
                    self._place_domino_horizontal(i, j, count)
                    self._place_domino_vertical(i, j, count)
                else:
                    self._place_domino_vertical(i, j, count)
                    self._place_domino_horizontal(i, j, count)

        return False

    def toggle_tile(self) -> None:
        """Toggle between the tiles."""
        self.current_tile = 2 if self.current_tile == 1 else 1

    def generate_board(self) -> None:
        """Recursively fill an empty board with dominoes until
        there are no empty spaces left."""
        while True:
            if np.all(self.board != EMPTY):
                return

            self.board = np.array([EMPTY] * self.size**2)
            wall_count = np.random.choice([5, 7])
            wall_index = np.random.choice(self.size**2, wall_count, False)
            self.board[wall_index] = WALL
            self.board.shape = (self.size, self.size)
            self.place_domino(0, 0, self.size**2 - wall_count)

    def reset(self) -> None:
        """Generate a level for the game. The level consists of
        a board that is mostly empty, except for some walls."""
        self.generate_board()
        self.rows = np.sum(np.where(self.board > 0, self.board, 0), axis=1)
        self.cols = np.sum(np.where(self.board > 0, self.board, 0), axis=0)
        self.board[self.board >= 0] = EMPTY
        self.wizardry = True

    def _draw_text(self) -> None:
        """Draw the text."""
        rows = np.sum(np.where(self.board > 0, self.board, 0), axis=1)
        cols = np.sum(np.where(self.board > 0, self.board, 0), axis=0)

        # Render row texts
        for row in range(self.size):
            text_color = (
                CORRECT
                if rows[row] == self.rows[row]
                else WRONG if rows[row] > self.rows[row] else COLOR_TEXT
            )
            text = self.font.render(str(self.rows[row]), True, text_color)

            # Render row texts on left side
            text_x = self.offset // 2
            text_y = (row + 0.5) * self.tile_size + self.offset
            text_rect = text.get_rect(center=(text_x, text_y))
            self.screen.blit(text, text_rect)

            # Render row texts on right side
            text_x = self.screen.get_width() - self.offset // 2
            text_rect = text.get_rect(center=(text_x, text_y))
            self.screen.blit(text, text_rect)

        # Render column texts
        for col in range(self.size):
            text_color = (
                CORRECT
                if cols[col] == self.cols[col]
                else WRONG if cols[col] > self.cols[col] else COLOR_TEXT
            )
            text = self.font.render(str(self.cols[col]), True, text_color)

            text_x = (col + 0.5) * self.tile_size + self.offset
            text_y = self.offset // 2
            text_rect = text.get_rect(center=(text_x, text_y))
            self.screen.blit(text, text_rect)

    def _draw_tile(self, row: int, col: int) -> None:
        """Draw the a tile."""
        rect = pg.Rect(
            row * self.tile_size + self.offset,
            col * self.tile_size + self.offset,
            self.tile_size,
            self.tile_size,
        )

        val = self.board[(col, row)]
        if val == WALL:
            self.screen.blit(self.sprite_wall, rect)
        if val == 1:
            self.screen.blit(self.sprite_domino_one, rect)
        if val == 2:
            rect.x -= self.tile_size
            self.screen.blit(self.sprite_domino_two, rect)

    def _draw_tiles(self) -> None:
        """Draw the board."""
        for row in range(self.size):
            for col in range(self.size):
                self._draw_tile(row, col)

    def _draw_current_tile(self) -> None:
        screen_width, screen_height = self.screen.get_size()
        if self.current_tile == 1:
            x = screen_width // 2
            y = screen_height - self.offset // 2
            pg.draw.circle(self.screen, COLOR_TEXT, (x, y), 10)
        elif self.current_tile == 2:
            x = screen_width // 2 - 0.15 * self.tile_size
            y = screen_height - self.offset // 2 - 0.15 * self.tile_size
            pg.draw.circle(self.screen, COLOR_TEXT, (x, y), 10)

            x = screen_width // 2 + 0.15 * self.tile_size
            y = screen_height - self.offset // 2 + 0.15 * self.tile_size
            pg.draw.circle(self.screen, COLOR_TEXT, (x, y), 10)

    def _draw_board(self) -> None:
        rect = pg.Rect(
            self.offset,
            self.offset,
            self.size * self.tile_size,
            self.size * self.tile_size,
        )
        self.screen.blit(self.sprite_board, rect)

    def draw(self) -> None:
        """Draw the game."""
        self.screen.fill(COLOR_BG)
        self._draw_board()
        self._draw_text()
        self._draw_tiles()
        self._draw_current_tile()

    def _is_occupied(self, row: int, col: int) -> bool:
        """Check if the cell on (row, col) is occupied."""
        return self.board[row, col] != EMPTY

    def _is_on_board(self, row: int, col: int) -> bool:
        """Check if the cell on (row, col) is on the board."""
        return 0 <= row < self.size and 0 <= col < self.size

    def _is_valid(self, row: int, col: int) -> bool:
        return self._is_on_board(row, col) and not self._is_occupied(row, col)

    def remove_tile(self, row: int, col: int) -> None:
        """Remove a tile from the board."""
        if not self._is_on_board(row, col):
            return

        cell = self.board[row, col]
        if cell == 0:
            self.board[row, col] = EMPTY
            if self.board[row - 1, col] == 1:
                self.board[row - 1, col] = EMPTY
            if self.board[row, col + 1] == 2:
                self.board[row, col + 1] = EMPTY
            pg.mixer.Sound.play(self.audio_domino_remove)
        if cell == 1:
            self.board[row, col] = EMPTY
            self.board[row + 1, col] = EMPTY
            pg.mixer.Sound.play(self.audio_domino_remove)
        if cell == 2:
            self.board[row, col] = EMPTY
            self.board[row, col - 1] = EMPTY
            pg.mixer.Sound.play(self.audio_domino_remove)

        self.wizardry = False

    def place_tile(self, row: int, col: int) -> None:
        """Place a tile on the board."""
        if not self._is_valid(row, col):
            return self.remove_tile(row, col)

        # Place tile vertically.
        if self.current_tile == 1 and self._is_valid(row + 1, col):
            self.board[row, col] = 1
            self.board[row + 1, col] = 0
            pg.mixer.Sound.play(self.audio_domino_place)

        # Place tile horizontally
        if self.current_tile == 2 and self._is_valid(row, col - 1):
            self.board[row, col] = 2
            self.board[row, col - 1] = 0
            pg.mixer.Sound.play(self.audio_domino_place)

        if self.is_solved():
            pg.mixer.Sound.play(self.audio_solved)
            print("Wizardry" if self.wizardry else "Winner")

    def is_solved(self) -> bool:
        """Check if the board is solved."""
        rows = np.sum(np.where(self.board > 0, self.board, 0), axis=1)
        cols = np.sum(np.where(self.board > 0, self.board, 0), axis=0)
        return (cols == self.cols).all() and (rows == self.rows).all()
