"""
Filename: Snake.py
Authors: Yoshi Fu
Project: Snake Game
Date: October 2022

Summary:
- This file contains a Snake class sprite for the snake game.
- The snake has a method to look at certain direction.
- The snake has a method to move in a certain direction.
- The snake can eat apples to grow in size.
- The snake can check for self collision and halt accordingly.
"""

import pygame


class Snake(pygame.sprite.Sprite):
    """A class to represent a snake in the snake game.

    Attributes
    ----------
    size : int
        size of the image.
    image : pygame.Surface
        drawing information scaled by size.
    rect : pygame.Rect
        position and size of the apple.
    board : pygame.Rect
        position and size of the board.
    orientation : np.array
        vector describing direction of sight.
    head : bool
        bool that specifies if this is the head.
    tail : pygame.Rect
        position and size of the tail.
    body : list[pygame.Rect]
        list containing position and size of body.
    length : int
        total length of the snake.
    snakes : list[pygame.sprite.Sprite]
        list containing sprites to check for collision.

    Methods
    -------
    update():
        checks for key inputs and collisions.
    mask():
        create mask with positions of snake on board.
    eat():
        eat the apple and relocate it.
    move():
        move the snake in a direction.
    moveup():
        change snake orientation to up.
    movedown():
        change snake orientation to down.
    moveleft():
        change snake orientation to left.
    moveright():
        change snake orientation to right.
    """

    def __init__(self, size: int, position: tuple[int, int], head: bool):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill("darkgreen")

        screen = pygame.display.get_surface()
        self.board = screen.get_rect()

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        if head:
            self.head = head
            self.body = [self]
            self.tail = self.rect
            self.orientation = (0, 0)
            self.length = 0
            self.snakes = pygame.sprite.Group()

    def update(self, apple: pygame.sprite.Sprite):
        if not self.head:
            return

        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.moveup()
        if key[pygame.K_DOWN]:
            self.movedown()
        if key[pygame.K_LEFT]:
            self.moveleft()
        if key[pygame.K_RIGHT]:
            self.moveright()

        if pygame.sprite.collide_rect(self, apple):
            self.eat(apple)

        if len(pygame.sprite.spritecollide(self, self.snakes, False)) > 1:
            print("game over")
            self.head = False

        self.move()

    def mask(self):
        rows = self.board.w // self.size
        cols = self.board.h // self.size
        mask = [[1 for _ in range(rows)] for _ in range(cols)]
        for body in self.body:
            row = body.rect.topleft[0] // self.size
            col = body.rect.topleft[1] // self.size
            mask[col][row] = 0
        return mask

    def eat(self, apple: pygame.sprite.Sprite):
        self.length += 1
        apple.relocate(self.mask())

    def move(self):
        newpos = self.rect.move(self.orientation)
        if self.board.contains(newpos):
            snake = Snake(self.size, newpos.topleft, False)
            self.body.append(snake)
            self.rect = snake.rect
            if self.length != len(self.body):
                self.tail = self.body.pop(0).rect

            self.snakes.add(snake)
            self.snakes.remove(self.body[0])
        pygame.event.pump()

    def moveup(self):
        if self.orientation != (0, self.size):
            self.orientation = (0, -self.size)

    def movedown(self):
        if self.orientation != (0, -self.size):
            self.orientation = (0, self.size)

    def moveleft(self):
        if self.orientation != (self.size, 0):
            self.orientation = (-self.size, 0)

    def moveright(self):
        if self.orientation != (-self.size, 0):
            self.orientation = (self.size, 0)
