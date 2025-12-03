"""Ball entity for game physics"""
import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS,
    BALL_INITIAL_SPEED_X, BALL_INITIAL_SPEED_Y,
    RED, PADDLE_HIT_ANGLE_RANGE
)


class Ball:
    """Game ball that bounces off walls, paddle, and bricks"""

    def __init__(self) -> None:
        """Initialize ball at center of screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        self.rect = pygame.Rect(center_x, center_y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = RED
        self.dx: float = BALL_INITIAL_SPEED_X
        self.dy: float = BALL_INITIAL_SPEED_Y
        self.is_caught: bool = False

    def move(self) -> None:
        """Update ball position"""
        if self.is_caught:
            return

        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

    def bounce_wall(self) -> bool:
        """Check and handle wall collisions

        Returns:
            True if ball bounced off a wall
        """
        bounced = False
        # Side walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
            bounced = True
        # Top wall
        if self.rect.top <= 0:
            self.dy *= -1
            bounced = True
        return bounced

    def bounce_paddle(self, paddle: 'Paddle') -> bool:
        """Check and handle paddle collision

        Args:
            paddle: Paddle object to check collision with

        Returns:
            True if ball collided with paddle
        """
        if not self.rect.colliderect(paddle.rect):
            return False

        if paddle.catch_active:
            # Catch the ball
            self.is_caught = True
            paddle.caught_ball = self
            self.rect.bottom = paddle.rect.top
        else:
            # Calculate bounce angle based on hit position
            hit_pos = (self.rect.centerx - paddle.rect.left) / paddle.rect.width
            # hit_pos ranges from 0 (left edge) to 1 (right edge)
            # Map to angle: -PADDLE_HIT_ANGLE_RANGE/2 (left) to +PADDLE_HIT_ANGLE_RANGE/2 (right)
            self.dx = (hit_pos - 0.5) * PADDLE_HIT_ANGLE_RANGE
            self.dy = -abs(self.dy)  # Always bounce upward

        return True

    def is_out_of_bounds(self) -> bool:
        """Check if ball fell below screen

        Returns:
            True if ball is out of bounds
        """
        return self.rect.bottom >= SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface) -> None:
        """Render ball on screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)

    def slow_down(self) -> None:
        """Reduce ball speed (power-up effect)"""
        from src.constants import BALL_SLOW_DIVISOR
        self.dx /= BALL_SLOW_DIVISOR
        self.dy /= BALL_SLOW_DIVISOR

    def speed_up(self) -> None:
        """Restore ball speed (revert slow power-up)"""
        from src.constants import BALL_SLOW_DIVISOR
        self.dx *= BALL_SLOW_DIVISOR
        self.dy *= BALL_SLOW_DIVISOR

    def reverse_dy(self) -> None:
        """Reverse vertical direction"""
        self.dy *= -1
