"""Collision detection and handling"""
from typing import List, Optional
from src.entities.ball import Ball
from src.entities.paddle import Paddle
from src.entities.brick import Brick
from src.entities.powerup import PowerUp
from src.entities.enemy import Enemy
from src.entities.boss import Boss
from src.entities.laser import Laser
from src.entities.bomb import Bomb


class CollisionManager:
    """Handles all collision detection and response in the game"""

    @staticmethod
    def check_ball_brick_collision(
        ball: Ball,
        bricks: List[Brick]
    ) -> Optional[Brick]:
        """Check if ball collides with any brick

        Args:
            ball: Ball object
            bricks: List of brick objects

        Returns:
            Collided brick or None
        """
        for brick in bricks:
            if ball.rect.colliderect(brick.rect):
                return brick
        return None

    @staticmethod
    def check_ball_enemy_collision(
        ball: Ball,
        enemies: List[Enemy]
    ) -> Optional[Enemy]:
        """Check if ball collides with any enemy

        Args:
            ball: Ball object
            enemies: List of enemy objects

        Returns:
            Collided enemy or None
        """
        for enemy in enemies:
            if ball.rect.colliderect(enemy.rect):
                return enemy
        return None

    @staticmethod
    def check_ball_boss_collision(
        ball: Ball,
        boss: Optional[Boss]
    ) -> bool:
        """Check if ball collides with boss

        Args:
            ball: Ball object
            boss: Boss object or None

        Returns:
            True if collision occurred
        """
        if boss and ball.rect.colliderect(boss.rect):
            return True
        return False

    @staticmethod
    def check_powerup_paddle_collision(
        powerup: PowerUp,
        paddle: Paddle
    ) -> bool:
        """Check if power-up collides with paddle

        Args:
            powerup: PowerUp object
            paddle: Paddle object

        Returns:
            True if collision occurred
        """
        return powerup.rect.colliderect(paddle.rect)

    @staticmethod
    def check_laser_brick_collision(
        laser: Laser,
        bricks: List[Brick]
    ) -> Optional[Brick]:
        """Check if laser collides with any brick

        Args:
            laser: Laser object
            bricks: List of brick objects

        Returns:
            Collided brick or None
        """
        for brick in bricks:
            if laser.rect.colliderect(brick.rect):
                return brick
        return None

    @staticmethod
    def check_laser_enemy_collision(
        laser: Laser,
        enemies: List[Enemy]
    ) -> Optional[Enemy]:
        """Check if laser collides with any enemy

        Args:
            laser: Laser object
            enemies: List of enemy objects

        Returns:
            Collided enemy or None
        """
        for enemy in enemies:
            if laser.rect.colliderect(enemy.rect):
                return enemy
        return None

    @staticmethod
    def check_bomb_paddle_collision(
        bomb: Bomb,
        paddle: Paddle
    ) -> bool:
        """Check if bomb collides with paddle

        Args:
            bomb: Bomb object
            paddle: Paddle object

        Returns:
            True if collision occurred
        """
        return bomb.rect.colliderect(paddle.rect)
