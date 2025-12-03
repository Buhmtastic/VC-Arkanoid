"""Laser entity fired from paddle"""
import pygame
from src.constants import (
    LASER_WIDTH, LASER_HEIGHT, LASER_SPEED, YELLOW
)


class Laser:
    """Laser projectile fired upward from paddle"""

    def __init__(self, x: int, y: int) -> None:
        """Initialize laser at position

        Args:
            x: Center X coordinate
            y: Top Y coordinate
        """
        self.rect = pygame.Rect(
            x - LASER_WIDTH // 2,
            y,
            LASER_WIDTH,
            LASER_HEIGHT
        )
        self.color = YELLOW
        self.dy = -LASER_SPEED

    def move(self) -> None:
        """Update laser position (moving upward)"""
        self.rect.y += self.dy

    def draw(self, screen: pygame.Surface) -> None:
        """Render laser on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def is_out_of_bounds(self) -> bool:
        """Check if laser left screen

        Returns:
            True if out of bounds
        """
        return self.rect.bottom < 0
