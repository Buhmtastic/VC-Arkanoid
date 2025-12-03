"""Power-up entity for gameplay enhancements"""
import pygame
from src.constants import (
    POWERUP_WIDTH, POWERUP_HEIGHT, POWERUP_SPEED,
    PowerUpType, POWERUP_COLORS, POWERUP_LABELS,
    BLACK, FONT_SIZE_SMALL
)


class PowerUp:
    """Falling power-up that grants special abilities"""

    def __init__(self, x: int, y: int, powerup_type: PowerUpType) -> None:
        """Initialize power-up at position

        Args:
            x: Center X coordinate
            y: Center Y coordinate
            powerup_type: Type of power-up effect
        """
        self.rect = pygame.Rect(
            x - POWERUP_WIDTH // 2,
            y - POWERUP_HEIGHT // 2,
            POWERUP_WIDTH,
            POWERUP_HEIGHT
        )
        self.type = powerup_type
        self.dy = POWERUP_SPEED
        self.color = POWERUP_COLORS.get(powerup_type, (0, 0, 255))
        self.label = POWERUP_LABELS.get(powerup_type, '?')

    def move(self) -> None:
        """Update power-up position (falling)"""
        self.rect.y += self.dy

    def draw(self, screen: pygame.Surface) -> None:
        """Render power-up on screen

        Args:
            screen: Pygame surface to draw on
        """
        # Draw colored rectangle
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw label text
        font = pygame.font.Font(None, FONT_SIZE_SMALL)
        text = font.render(self.label, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_out_of_bounds(self) -> bool:
        """Check if power-up fell off screen

        Returns:
            True if out of bounds
        """
        from src.constants import SCREEN_HEIGHT
        return self.rect.top > SCREEN_HEIGHT
