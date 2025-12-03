"""Bomb entity dropped by boss"""
import pygame
from src.constants import (
    SCREEN_HEIGHT, BOMB_SIZE, BOMB_SPEED, MAGENTA
)


class Bomb:
    """Bomb dropped by boss that damages player"""

    def __init__(self, x: int, y: int) -> None:
        """Initialize bomb at position

        Args:
            x: Center X coordinate
            y: Top Y coordinate
        """
        self.rect = pygame.Rect(
            x - BOMB_SIZE // 2,
            y,
            BOMB_SIZE,
            BOMB_SIZE
        )
        self.color = MAGENTA
        self.dy = BOMB_SPEED

    def move(self) -> None:
        """Update bomb position (falling)"""
        self.rect.y += self.dy

    def draw(self, screen: pygame.Surface) -> None:
        """Render bomb on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def is_out_of_bounds(self) -> bool:
        """Check if bomb fell off screen

        Returns:
            True if out of bounds
        """
        return self.rect.top > SCREEN_HEIGHT
