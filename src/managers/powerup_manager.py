"""Power-up effect management"""
from typing import List, Dict
from src.entities.paddle import Paddle
from src.entities.ball import Ball
from src.entities.powerup import PowerUp
from src.constants import (
    PowerUpType, POWERUP_DURATION_FRAMES, POWERUP_CATCH_DURATION
)


class PowerUpManager:
    """Manages power-up effects and timers"""

    def __init__(self) -> None:
        """Initialize power-up manager"""
        self.active_timers: Dict[PowerUpType, int] = {}

    def apply_powerup(
        self,
        powerup: PowerUp,
        paddle: Paddle,
        balls: List[Ball]
    ) -> int:
        """Apply power-up effect

        Args:
            powerup: PowerUp to apply
            paddle: Player paddle
            balls: List of balls in play

        Returns:
            Lives gained (0 or 1)
        """
        lives_gained = 0

        if powerup.type == PowerUpType.ENLARGE:
            paddle.enlarge()
            self.active_timers[PowerUpType.ENLARGE] = POWERUP_DURATION_FRAMES

        elif powerup.type == PowerUpType.SLOW:
            for ball in balls:
                ball.slow_down()
            self.active_timers[PowerUpType.SLOW] = POWERUP_DURATION_FRAMES

        elif powerup.type == PowerUpType.LASER:
            paddle.laser_active = True
            self.active_timers[PowerUpType.LASER] = POWERUP_DURATION_FRAMES

        elif powerup.type == PowerUpType.CATCH:
            paddle.catch_active = True
            self.active_timers[PowerUpType.CATCH] = POWERUP_CATCH_DURATION

        elif powerup.type == PowerUpType.DISRUPT:
            self._disrupt_ball(balls)

        elif powerup.type == PowerUpType.BREAK:
            # Will be handled by game engine (skip level)
            pass

        elif powerup.type == PowerUpType.PLAYER:
            lives_gained = 1

        return lives_gained

    def _disrupt_ball(self, balls: List[Ball]) -> None:
        """Split first ball into three balls

        Args:
            balls: List of balls in play
        """
        if not balls:
            return

        original_ball = balls[0]

        # Create two additional balls with different angles
        new_ball1 = Ball()
        new_ball1.rect.center = original_ball.rect.center
        new_ball1.dx = -original_ball.dx
        new_ball1.dy = original_ball.dy

        new_ball2 = Ball()
        new_ball2.rect.center = original_ball.rect.center
        new_ball2.dx = original_ball.dx
        new_ball2.dy = -original_ball.dy

        balls.append(new_ball1)
        balls.append(new_ball2)

    def update_timers(self, paddle: Paddle, balls: List[Ball]) -> None:
        """Update all active power-up timers

        Args:
            paddle: Player paddle
            balls: List of balls in play
        """
        expired_powerups = []

        for powerup_type, remaining_time in self.active_timers.items():
            self.active_timers[powerup_type] -= 1

            if self.active_timers[powerup_type] <= 0:
                expired_powerups.append(powerup_type)

        # Revert expired power-ups
        for powerup_type in expired_powerups:
            self._revert_powerup(powerup_type, paddle, balls)
            del self.active_timers[powerup_type]

    def _revert_powerup(
        self,
        powerup_type: PowerUpType,
        paddle: Paddle,
        balls: List[Ball]
    ) -> None:
        """Revert power-up effect

        Args:
            powerup_type: Type of power-up to revert
            paddle: Player paddle
            balls: List of balls in play
        """
        if powerup_type == PowerUpType.ENLARGE:
            paddle.reset_width()

        elif powerup_type == PowerUpType.SLOW:
            for ball in balls:
                ball.speed_up()

        elif powerup_type == PowerUpType.LASER:
            paddle.laser_active = False

        elif powerup_type == PowerUpType.CATCH:
            paddle.catch_active = False
            if paddle.caught_ball:
                paddle.release_ball()
