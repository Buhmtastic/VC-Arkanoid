"""Game Constants and Configuration"""
from typing import Tuple
from enum import Enum

# Screen Configuration
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60

# Game Object Dimensions
PADDLE_WIDTH: int = 100
PADDLE_HEIGHT: int = 20
PADDLE_SPEED: int = 8

BALL_RADIUS: int = 10
BALL_INITIAL_SPEED_X: int = 5
BALL_INITIAL_SPEED_Y: int = -5

BRICK_WIDTH: int = 80
BRICK_HEIGHT: int = 30

POWERUP_WIDTH: int = 30
POWERUP_HEIGHT: int = 14
POWERUP_SPEED: int = 3

LASER_WIDTH: int = 5
LASER_HEIGHT: int = 15
LASER_SPEED: int = 10

ENEMY_SIZE: int = 30
ENEMY_SPEED: int = 2

BOSS_WIDTH: int = 300
BOSS_HEIGHT: int = 100
BOSS_HP: int = 16

BOMB_SIZE: int = 20
BOMB_SPEED: int = 4

# Colors (RGB)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
ORANGE: Tuple[int, int, int] = (255, 165, 0)
PURPLE: Tuple[int, int, int] = (128, 0, 128)
CYAN: Tuple[int, int, int] = (0, 255, 255)
MAGENTA: Tuple[int, int, int] = (255, 0, 255)
PINK: Tuple[int, int, int] = (255, 192, 203)
GRAY: Tuple[int, int, int] = (192, 192, 192)
DARK_GRAY: Tuple[int, int, int] = (160, 160, 160)
GOLD: Tuple[int, int, int] = (255, 215, 0)

# Brick Colors
BRICK_NORMAL_COLOR: Tuple[int, int, int] = GREEN
BRICK_SILVER_COLOR: Tuple[int, int, int] = GRAY
BRICK_SILVER_DAMAGED_COLOR: Tuple[int, int, int] = DARK_GRAY
BRICK_GOLD_COLOR: Tuple[int, int, int] = GOLD

# Game Configuration
INITIAL_LIVES: int = 3
POINTS_PER_BRICK: int = 10
POINTS_PER_ENEMY: int = 50
POINTS_PER_BOSS_HIT: int = 100

# Power-up Configuration
POWERUP_DROP_CHANCE: float = 0.3  # 30% chance
POWERUP_DURATION_FRAMES: int = 500  # ~8.3 seconds at 60 FPS
POWERUP_CATCH_DURATION: int = 5000  # Long duration for catch
PADDLE_ENLARGE_MULTIPLIER: float = 1.5
BALL_SLOW_DIVISOR: float = 2.0

# Spawn Timers (in frames)
ENEMY_SPAWN_INTERVAL: int = 300  # 5 seconds at 60 FPS
BOMB_SPAWN_INTERVAL: int = 120   # 2 seconds at 60 FPS

# Paddle Physics
PADDLE_HIT_ANGLE_RANGE: float = 16.0  # Max angle deviation from paddle hit

# UI Configuration
FONT_SIZE: int = 36
FONT_SIZE_SMALL: int = 20

# Brick Types
class BrickType(Enum):
    NORMAL = 'n'    # 1 hit
    SILVER = 's'    # 2 hits
    GOLD = 'g'      # Indestructible

# Power-up Types
class PowerUpType(Enum):
    ENLARGE = 'enlarge'  # Enlarge paddle
    SLOW = 'slow'        # Slow ball
    LASER = 'laser'      # Enable laser
    CATCH = 'catch'      # Catch ball
    DISRUPT = 'disrupt'  # Split ball into 3
    BREAK = 'break'      # Skip level
    PLAYER = 'player'    # Extra life

# Power-up Visual Configuration
POWERUP_COLORS = {
    PowerUpType.ENLARGE: GREEN,
    PowerUpType.SLOW: RED,
    PowerUpType.LASER: YELLOW,
    PowerUpType.CATCH: CYAN,
    PowerUpType.DISRUPT: MAGENTA,
    PowerUpType.BREAK: ORANGE,
    PowerUpType.PLAYER: PINK,
}

POWERUP_LABELS = {
    PowerUpType.ENLARGE: 'E',
    PowerUpType.SLOW: 'S',
    PowerUpType.LASER: 'L',
    PowerUpType.CATCH: 'C',
    PowerUpType.DISRUPT: 'D',
    PowerUpType.BREAK: 'B',
    PowerUpType.PLAYER: 'P',
}

# Sound Paths
SOUND_BRICK_DESTROY = "sounds/brick_destroy.wav"
SOUND_POWERUP = "sounds/powerup.wav"
SOUND_BOUNCE = "sounds/bounce.wav"

# Boss Configuration
BOSS_LEVEL_INDEX: int = 1  # Level 2 is boss level
