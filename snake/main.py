"""
Filename: main.py
Authors: Yoshi Fu
Project: Snake Game
Date: October 2022

Summary:
- This script implements the Snake Game.
"""

import pygame

from Apple import Apple
from Snake import Snake

pygame.init()


def main():
    screenColor = "green"
    screen = pygame.display.set_mode((800, 800))
    screen.fill(screenColor)
    pygame.display.set_caption("Snake")

    snake = Snake(50, (100, 100), True)
    apple = Apple(50)

    clock = pygame.time.Clock()

    while True:
        # Game logic.
        snake.update(apple)

        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # Render the graphics.
        screen.blit(apple.image, apple.rect)
        screen.blit(snake.image, snake.rect)

        pygame.display.flip()  # Refresh on-screen display
        screen.fill(screenColor, snake.tail)  # Draw over snake tail.
        clock.tick(10)  # wait until next frame (at 60 FPS)


if __name__ == "__main__":
    main()
