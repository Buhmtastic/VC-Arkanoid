"""Paddle entity for player control"""
import pygame
from typing import Optional
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT,
    PADDLE_SPEED, WHITE
)


class Paddle:
    """Player-controlled paddle that catches and reflects the ball"""

    def __init__(self) -> None:
        """Initialize paddle at bottom center of screen"""
        x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = WHITE
        self.speed = PADDLE_SPEED

        # Power-up states
        self.laser_active: bool = False
        self.catch_active: bool = False
        self.caught_ball: Optional['Ball'] = None

    def move(self) -> None:
        """Update paddle position based on mouse and keyboard input"""
        # Primary control: Mouse
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x

        # Secondary control: Keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep paddle within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Update caught ball position if any
        if self.caught_ball:
            self.caught_ball.rect.centerx = self.rect.centerx

    def draw(self, screen: pygame.Surface) -> None:
        """Render paddle on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_width(self) -> None:
        """Reset paddle width to normal size"""
        center_x = self.rect.centerx
        self.rect.width = PADDLE_WIDTH
        self.rect.centerx = center_x

    def enlarge(self) -> None:
        """Enlarge paddle width"""
        from src.constants import PADDLE_ENLARGE_MULTIPLIER
        center_x = self.rect.centerx
        self.rect.width = int(PADDLE_WIDTH * PADDLE_ENLARGE_MULTIPLIER)
        self.rect.centerx = center_x

    def release_ball(self) -> None:
        """Release caught ball"""
        if self.caught_ball:
            self.caught_ball.is_caught = False
            self.caught_ball.dy = -abs(self.caught_ball.dy)
            self.caught_ball = None
