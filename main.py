"""VC-Arkanoid - Main Entry Point

A modern Arkanoid clone built with Pygame.
Refactored with OOP principles and modular architecture.
"""
from src.game_engine import GameEngine
from data.levels import LEVELS


def main() -> None:
    """Main entry point for the game"""
    game = GameEngine(LEVELS)
    game.run()


if __name__ == "__main__":
    main()
