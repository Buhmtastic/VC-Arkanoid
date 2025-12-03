"""Enemy entity that falls from top"""
import pygame
import random
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, ENEMY_SPEED, ORANGE
)


class Enemy:
    """Falling enemy that player must avoid or destroy"""

    def __init__(self) -> None:
        """Initialize enemy at random position at top"""
        x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.rect = pygame.Rect(x, 0, ENEMY_SIZE, ENEMY_SIZE)
        self.color = ORANGE
        self.dy = ENEMY_SPEED

    def move(self) -> None:
        """Update enemy position (falling)"""
        self.rect.y += self.dy

    def draw(self, screen: pygame.Surface) -> None:
        """Render enemy on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def is_out_of_bounds(self) -> bool:
        """Check if enemy fell off screen

        Returns:
            True if out of bounds
        """
        return self.rect.top > SCREEN_HEIGHT
