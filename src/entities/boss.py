"""Boss entity (Doh) for boss level"""
import pygame
from src.constants import (
    SCREEN_WIDTH, BOSS_WIDTH, BOSS_HEIGHT, BOSS_HP, PURPLE
)


class Boss:
    """Doh boss that requires multiple hits to defeat"""

    def __init__(self) -> None:
        """Initialize boss at top center"""
        x = SCREEN_WIDTH // 2 - BOSS_WIDTH // 2
        y = 50
        self.rect = pygame.Rect(x, y, BOSS_WIDTH, BOSS_HEIGHT)
        self.color = PURPLE
        self.hp: int = BOSS_HP

    def hit(self) -> bool:
        """Register hit on boss

        Returns:
            True if boss is defeated
        """
        self.hp -= 1
        return self.hp <= 0

    def draw(self, screen: pygame.Surface) -> None:
        """Render boss on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw HP bar
        from src.constants import WHITE, RED
        hp_bar_width = BOSS_WIDTH
        hp_bar_height = 5
        hp_percentage = self.hp / BOSS_HP

        # Background (red)
        hp_bar_bg = pygame.Rect(self.rect.x, self.rect.bottom + 5, hp_bar_width, hp_bar_height)
        pygame.draw.rect(screen, RED, hp_bar_bg)

        # Foreground (white, shows remaining HP)
        hp_bar_fg = pygame.Rect(
            self.rect.x,
            self.rect.bottom + 5,
            int(hp_bar_width * hp_percentage),
            hp_bar_height
        )
        pygame.draw.rect(screen, WHITE, hp_bar_fg)
