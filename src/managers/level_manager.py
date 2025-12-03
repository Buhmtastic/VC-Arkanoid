"""Level management and progression"""
from typing import List, Optional
from src.entities.brick import Brick
from src.entities.boss import Boss
from src.constants import (
    BRICK_WIDTH, BRICK_HEIGHT, BrickType, BOSS_LEVEL_INDEX
)


class LevelManager:
    """Manages level loading and progression"""

    def __init__(self, level_data: List[List[str]]) -> None:
        """Initialize level manager

        Args:
            level_data: List of level layouts
        """
        self.level_data = level_data
        self.current_level: int = 0

    def load_level(self, level_index: int) -> List[Brick]:
        """Load bricks for specified level

        Args:
            level_index: Index of level to load

        Returns:
            List of brick objects
        """
        bricks = []

        if level_index >= len(self.level_data):
            return bricks

        layout = self.level_data[level_index]

        for row_index, row in enumerate(layout):
            for col_index, brick_char in enumerate(row):
                if brick_char != ' ':
                    brick_type = self._char_to_brick_type(brick_char)
                    if brick_type:
                        x = col_index * BRICK_WIDTH
                        y = row_index * BRICK_HEIGHT + 50
                        brick = Brick(x, y, brick_type)
                        bricks.append(brick)

        return bricks

    def _char_to_brick_type(self, char: str) -> Optional[BrickType]:
        """Convert character to brick type

        Args:
            char: Character representing brick type

        Returns:
            BrickType or None if invalid
        """
        brick_map = {
            'n': BrickType.NORMAL,
            's': BrickType.SILVER,
            'g': BrickType.GOLD,
        }
        return brick_map.get(char)

    def should_spawn_boss(self, level_index: int) -> bool:
        """Check if boss should spawn for this level

        Args:
            level_index: Current level index

        Returns:
            True if boss level
        """
        return level_index == BOSS_LEVEL_INDEX

    def create_boss(self) -> Boss:
        """Create boss instance

        Returns:
            Boss object
        """
        return Boss()

    def has_next_level(self, level_index: int) -> bool:
        """Check if there is a next level

        Args:
            level_index: Current level index

        Returns:
            True if more levels exist
        """
        return level_index + 1 < len(self.level_data)

    def get_total_levels(self) -> int:
        """Get total number of levels

        Returns:
            Total level count
        """
        return len(self.level_data)
