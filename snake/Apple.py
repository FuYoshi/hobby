"""
Filename: Apple.py
Authors: Yoshi Fu
Project: Snake Game
Date: October 2022

Summary:
- This file contains an Apple class sprite for the snake game.
- The apple relocates to a random position on the board when eaten.
"""

import random

import pygame


class Apple(pygame.sprite.Sprite):
    """A class to represent an apple in the snake game.

    Attributes
    ----------
    size : int
        size of the image.
    image : pygame.Surface
        drawing information scaled by size.
    board : pygame.Rect
        position and size of the board.
    rect : pygame.Rect
        position and size of the apple.

    Methods
    -------
    relocate():
        move the apple to a new position.
    """

    def __init__(self, size: int):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.image.load("sprites/apple.png")
        self.image = pygame.transform.scale(self.image, (size, size))

        screen = pygame.display.get_surface()
        self.board = screen.get_rect()

        self.rect = self.image.get_rect()
        self.relocate()

    def relocate(self, snake_mask: list = None):
        """Move the apple to a new position."""
        if not snake_mask:
            rows = self.board.w // self.size
            cols = self.board.h // self.size
            snake_mask = [[1 for _ in range(rows)] for _ in range(cols)]

        w = len(snake_mask)
        h = len(snake_mask[0])
        weight_mask = [sum(row) for row in snake_mask]

        row = random.choices(range(w), weights=weight_mask).pop()
        col = random.choices(range(h), weights=snake_mask[row]).pop()

        self.rect.top = row * self.size
        self.rect.right = col * self.size
