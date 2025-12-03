"""Game state management"""
from typing import List, Optional
from src.entities.paddle import Paddle
from src.entities.ball import Ball
from src.entities.brick import Brick
from src.entities.powerup import PowerUp
from src.entities.laser import Laser
from src.entities.enemy import Enemy
from src.entities.boss import Boss
from src.entities.bomb import Bomb
from src.constants import INITIAL_LIVES


class GameState:
    """Manages game state including entities, score, and level"""

    def __init__(self) -> None:
        """Initialize game state"""
        # Game progress
        self.level: int = 0
        self.score: int = 0
        self.lives: int = INITIAL_LIVES
        self.is_paused: bool = False

        # Game entities
        self.paddle: Paddle = Paddle()
        self.balls: List[Ball] = [Ball()]
        self.bricks: List[Brick] = []
        self.power_ups: List[PowerUp] = []
        self.lasers: List[Laser] = []
        self.enemies: List[Enemy] = []
        self.bombs: List[Bomb] = []
        self.boss: Optional[Boss] = None

        # Spawn timers
        self.enemy_spawn_timer: int = 0
        self.bomb_spawn_timer: int = 0

    def reset_for_new_life(self) -> None:
        """Reset entities for new life after ball loss"""
        self.paddle = Paddle()
        self.balls = [Ball()]

    def reset_for_next_level(self) -> None:
        """Reset entities for next level"""
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.power_ups.clear()
        self.lasers.clear()
        self.enemies.clear()
        self.bombs.clear()
        self.enemy_spawn_timer = 0
        self.bomb_spawn_timer = 0

    def reset_game(self) -> None:
        """Reset entire game to initial state"""
        self.level = 0
        self.score = 0
        self.lives = INITIAL_LIVES
        self.is_paused = False

        self.paddle = Paddle()
        self.balls = [Ball()]
        self.bricks.clear()
        self.power_ups.clear()
        self.lasers.clear()
        self.enemies.clear()
        self.bombs.clear()
        self.boss = None

        self.enemy_spawn_timer = 0
        self.bomb_spawn_timer = 0

    def is_stage_clear(self) -> bool:
        """Check if current stage is cleared

        Returns:
            True if no bricks and no boss remain
        """
        return len(self.bricks) == 0 and self.boss is None

    def has_balls(self) -> bool:
        """Check if any balls remain in play

        Returns:
            True if at least one ball exists
        """
        return len(self.balls) > 0

    def add_score(self, points: int) -> None:
        """Add points to score

        Args:
            points: Points to add
        """
        self.score += points

    def lose_life(self) -> None:
        """Decrement lives counter"""
        self.lives -= 1

    def gain_life(self) -> None:
        """Increment lives counter"""
        self.lives += 1

    def is_game_over(self) -> bool:
        """Check if game is over

        Returns:
            True if no lives remain
        """
        return self.lives <= 0

    def toggle_pause(self) -> None:
        """Toggle pause state"""
        self.is_paused = not self.is_paused
