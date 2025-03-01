#!/usr/bin/python
"""
Filename: label.py
Authors: Yoshi Fu
Project: 2048 Game
Date: October 2022

Summary:
This module implements a Label class for the 2048 game.
"""


class Label:
    """Class to keep track of a text field."""

    def __init__(self, font, text, color, position, anchor="topleft"):
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        setattr(self.rect, anchor, position)
        print(self.rect)

    def draw(self, surface):
        """Draw the label on the surface."""
        surface.blit(self.image, self.rect)
