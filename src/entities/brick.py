"""Brick entity for level obstacles"""
import pygame
from typing import Tuple
from src.constants import (
    BRICK_WIDTH, BRICK_HEIGHT, BrickType,
    BRICK_NORMAL_COLOR, BRICK_SILVER_COLOR,
    BRICK_SILVER_DAMAGED_COLOR, BRICK_GOLD_COLOR
)


class Brick:
    """Destructible brick obstacle"""

    def __init__(self, x: int, y: int, brick_type: BrickType) -> None:
        """Initialize brick at position with type

        Args:
            x: X coordinate
            y: Y coordinate
            brick_type: Type of brick (normal, silver, gold)
        """
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.type = brick_type
        self.hits: int = 0
        self.color = self._get_initial_color()

    def _get_initial_color(self) -> Tuple[int, int, int]:
        """Get initial color based on brick type

        Returns:
            RGB color tuple
        """
        if self.type == BrickType.NORMAL:
            return BRICK_NORMAL_COLOR
        elif self.type == BrickType.SILVER:
            return BRICK_SILVER_COLOR
        elif self.type == BrickType.GOLD:
            return BRICK_GOLD_COLOR
        return BRICK_NORMAL_COLOR

    def hit(self) -> bool:
        """Register hit on brick

        Returns:
            True if brick should be destroyed
        """
        if self.type == BrickType.NORMAL:
            self.hits += 1
            return self.hits >= 1

        elif self.type == BrickType.SILVER:
            self.hits += 1
            if self.hits == 1:
                self.color = BRICK_SILVER_DAMAGED_COLOR
            return self.hits >= 2

        elif self.type == BrickType.GOLD:
            # Indestructible
            return False

        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Render brick on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)
