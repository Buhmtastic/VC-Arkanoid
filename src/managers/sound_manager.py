"""Sound management for game audio"""
import pygame
from typing import Optional
from src.constants import (
    SOUND_BRICK_DESTROY, SOUND_POWERUP, SOUND_BOUNCE
)


class SoundManager:
    """Manages loading and playing game sounds"""

    def __init__(self) -> None:
        """Initialize sound system and load sound files"""
        pygame.mixer.init()
        self.brick_destroy: Optional[pygame.mixer.Sound] = self._load_sound(SOUND_BRICK_DESTROY)
        self.powerup: Optional[pygame.mixer.Sound] = self._load_sound(SOUND_POWERUP)
        self.bounce: Optional[pygame.mixer.Sound] = self._load_sound(SOUND_BOUNCE)

    def _load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """Load sound file with error handling

        Args:
            path: Path to sound file

        Returns:
            Sound object or None if loading failed
        """
        try:
            return pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Cannot load sound: {path} - {e}")
            return None

    def play(self, sound: Optional[pygame.mixer.Sound]) -> None:
        """Play sound if available

        Args:
            sound: Sound object to play
        """
        if sound:
            sound.play()

    def play_brick_destroy(self) -> None:
        """Play brick destruction sound"""
        self.play(self.brick_destroy)

    def play_powerup(self) -> None:
        """Play power-up collection sound"""
        self.play(self.powerup)

    def play_bounce(self) -> None:
        """Play bounce sound"""
        self.play(self.bounce)
