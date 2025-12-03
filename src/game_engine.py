"""Main game engine and loop"""
import pygame
import sys
import random
from typing import List
from src.game_state import GameState
from src.managers.sound_manager import SoundManager
from src.managers.collision_manager import CollisionManager
from src.managers.powerup_manager import PowerUpManager
from src.managers.level_manager import LevelManager
from src.entities.powerup import PowerUp
from src.entities.laser import Laser
from src.entities.enemy import Enemy
from src.entities.bomb import Bomb
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE,
    FONT_SIZE, PowerUpType, POWERUP_DROP_CHANCE,
    ENEMY_SPAWN_INTERVAL, BOMB_SPAWN_INTERVAL,
    POINTS_PER_BRICK, POINTS_PER_ENEMY, POINTS_PER_BOSS_HIT
)


class GameEngine:
    """Main game engine that manages game loop and updates"""

    def __init__(self, level_data: List[List[str]]) -> None:
        """Initialize game engine

        Args:
            level_data: List of level layouts
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("VC-Arkanoid")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)

        # Game components
        self.state = GameState()
        self.sound_manager = SoundManager()
        self.collision_manager = CollisionManager()
        self.powerup_manager = PowerUpManager()
        self.level_manager = LevelManager(level_data)

        # Load first level
        self._load_level(0)

        self.running: bool = True

    def _load_level(self, level_index: int) -> None:
        """Load specified level

        Args:
            level_index: Index of level to load
        """
        self.state.level = level_index
        self.state.bricks = self.level_manager.load_level(level_index)

        if self.level_manager.should_spawn_boss(level_index):
            self.state.boss = self.level_manager.create_boss()
        else:
            self.state.boss = None

    def run(self) -> None:
        """Main game loop"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

        # Game ended - show appropriate screen
        if self.state.is_game_over():
            if self._show_game_over_screen():
                self._restart_game()
        else:
            if self._show_game_win_screen():
                self._restart_game()

        pygame.quit()
        sys.exit()

    def _restart_game(self) -> None:
        """Restart game from beginning"""
        self.state.reset_game()
        self.powerup_manager = PowerUpManager()
        self._load_level(0)
        self.running = True
        self.run()

    def _handle_events(self) -> None:
        """Process input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.state.toggle_pause()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.state.is_paused:
                    self._handle_mouse_click()

    def _handle_mouse_click(self) -> None:
        """Handle mouse click for laser firing and ball release"""
        if self.state.paddle.laser_active:
            # Fire lasers from both sides of paddle
            left_x = self.state.paddle.rect.left + 10
            right_x = self.state.paddle.rect.right - 10
            y = self.state.paddle.rect.top
            self.state.lasers.append(Laser(left_x, y))
            self.state.lasers.append(Laser(right_x, y))

        if self.state.paddle.caught_ball:
            self.state.paddle.release_ball()

    def _update(self) -> None:
        """Update game state"""
        if self.state.is_paused:
            return

        # Update paddle
        self.state.paddle.move()

        # Update balls
        self._update_balls()

        # Check for life loss
        if not self.state.has_balls():
            self.state.lose_life()
            if self.state.is_game_over():
                self.running = False
            else:
                self.state.reset_for_new_life()

        # Update game entities
        self._update_power_ups()
        self._update_lasers()
        self._update_enemies()
        self._update_bombs()

        # Check for stage clear
        if self.state.is_stage_clear():
            self._advance_level()

    def _update_balls(self) -> None:
        """Update all balls and handle collisions"""
        for ball in self.state.balls[:]:
            ball.move()

            # Wall collisions
            if ball.bounce_wall():
                self.sound_manager.play_bounce()

            # Paddle collision
            if ball.bounce_paddle(self.state.paddle):
                self.sound_manager.play_bounce()

            # Brick collisions
            collided_brick = self.collision_manager.check_ball_brick_collision(
                ball, self.state.bricks
            )
            if collided_brick:
                if collided_brick.hit():
                    self.state.bricks.remove(collided_brick)
                    self.state.add_score(POINTS_PER_BRICK)
                    self.sound_manager.play_brick_destroy()
                    self._try_spawn_powerup(collided_brick.rect.centerx, collided_brick.rect.centery)
                ball.reverse_dy()

            # Enemy collisions
            collided_enemy = self.collision_manager.check_ball_enemy_collision(
                ball, self.state.enemies
            )
            if collided_enemy:
                self.state.enemies.remove(collided_enemy)
                self.state.add_score(POINTS_PER_ENEMY)
                ball.reverse_dy()

            # Boss collision
            if self.collision_manager.check_ball_boss_collision(ball, self.state.boss):
                if self.state.boss and self.state.boss.hit():
                    self.state.boss = None  # Boss defeated
                else:
                    self.state.add_score(POINTS_PER_BOSS_HIT)
                ball.reverse_dy()
                self.sound_manager.play_bounce()

            # Out of bounds
            if ball.is_out_of_bounds():
                self.state.balls.remove(ball)

    def _try_spawn_powerup(self, x: int, y: int) -> None:
        """Try to spawn power-up at position

        Args:
            x: X coordinate
            y: Y coordinate
        """
        if random.random() < POWERUP_DROP_CHANCE:
            powerup_types = list(PowerUpType)
            powerup_type = random.choice(powerup_types)
            powerup = PowerUp(x, y, powerup_type)
            self.state.power_ups.append(powerup)

    def _update_power_ups(self) -> None:
        """Update power-ups and handle collection"""
        # Move power-ups
        for powerup in self.state.power_ups[:]:
            powerup.move()

            # Check collision with paddle
            if self.collision_manager.check_powerup_paddle_collision(
                powerup, self.state.paddle
            ):
                # Apply power-up effect
                if powerup.type == PowerUpType.BREAK:
                    self._advance_level()
                else:
                    lives_gained = self.powerup_manager.apply_powerup(
                        powerup, self.state.paddle, self.state.balls
                    )
                    if lives_gained > 0:
                        self.state.gain_life()

                self.state.power_ups.remove(powerup)
                self.sound_manager.play_powerup()

            # Remove if out of bounds
            elif powerup.is_out_of_bounds():
                self.state.power_ups.remove(powerup)

        # Update power-up timers
        self.powerup_manager.update_timers(self.state.paddle, self.state.balls)

    def _update_lasers(self) -> None:
        """Update lasers and handle collisions"""
        for laser in self.state.lasers[:]:
            laser.move()

            # Check out of bounds
            if laser.is_out_of_bounds():
                self.state.lasers.remove(laser)
                continue

            # Check brick collision
            collided_brick = self.collision_manager.check_laser_brick_collision(
                laser, self.state.bricks
            )
            if collided_brick:
                if collided_brick.hit():
                    self.state.bricks.remove(collided_brick)
                    self.state.add_score(POINTS_PER_BRICK)
                self.state.lasers.remove(laser)
                continue

            # Check enemy collision
            collided_enemy = self.collision_manager.check_laser_enemy_collision(
                laser, self.state.enemies
            )
            if collided_enemy:
                self.state.enemies.remove(collided_enemy)
                self.state.add_score(POINTS_PER_ENEMY)
                self.state.lasers.remove(laser)

    def _update_enemies(self) -> None:
        """Update enemies and spawn new ones"""
        # Spawn timer
        self.state.enemy_spawn_timer += 1
        if self.state.enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
            self.state.enemy_spawn_timer = 0
            self.state.enemies.append(Enemy())

        # Move enemies
        for enemy in self.state.enemies[:]:
            enemy.move()
            if enemy.is_out_of_bounds():
                self.state.enemies.remove(enemy)

    def _update_bombs(self) -> None:
        """Update bombs dropped by boss"""
        # Spawn bombs if boss exists
        if self.state.boss:
            self.state.bomb_spawn_timer += 1
            if self.state.bomb_spawn_timer >= BOMB_SPAWN_INTERVAL:
                self.state.bomb_spawn_timer = 0
                bomb = Bomb(self.state.boss.rect.centerx, self.state.boss.rect.bottom)
                self.state.bombs.append(bomb)

        # Move bombs
        for bomb in self.state.bombs[:]:
            bomb.move()

            # Check collision with paddle
            if self.collision_manager.check_bomb_paddle_collision(
                bomb, self.state.paddle
            ):
                self.state.lose_life()
                self.state.bombs.remove(bomb)
                if self.state.is_game_over():
                    self.running = False

            # Remove if out of bounds
            elif bomb.is_out_of_bounds():
                self.state.bombs.remove(bomb)

    def _advance_level(self) -> None:
        """Advance to next level"""
        next_level = self.state.level + 1

        if self.level_manager.has_next_level(next_level):
            self.state.reset_for_next_level()
            self._load_level(next_level)
        else:
            # Game won!
            self.running = False

    def _draw(self) -> None:
        """Render game"""
        self.screen.fill(BLACK)

        # Draw entities
        self.state.paddle.draw(self.screen)

        for ball in self.state.balls:
            ball.draw(self.screen)

        for brick in self.state.bricks:
            brick.draw(self.screen)

        for powerup in self.state.power_ups:
            powerup.draw(self.screen)

        for laser in self.state.lasers:
            laser.draw(self.screen)

        for enemy in self.state.enemies:
            enemy.draw(self.screen)

        if self.state.boss:
            self.state.boss.draw(self.screen)

        for bomb in self.state.bombs:
            bomb.draw(self.screen)

        # Draw UI
        self._draw_ui()

        # Draw pause overlay
        if self.state.is_paused:
            self._draw_pause_overlay()

        pygame.display.flip()

    def _draw_ui(self) -> None:
        """Draw UI elements"""
        score_text = self.font.render(f"Score: {self.state.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.state.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        level_text = self.font.render(f"Level: {self.state.level + 1}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))

    def _draw_pause_overlay(self) -> None:
        """Draw pause screen overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font.render("PAUSED", True, WHITE)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(pause_text, text_rect)

        hint_text = self.font.render("Press P or ESC to resume", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(hint_text, hint_rect)

    def _show_game_over_screen(self) -> bool:
        """Show game over screen

        Returns:
            True if player wants to restart
        """
        self.screen.fill(BLACK)

        game_over_text = self.font.render("GAME OVER", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80))

        score_text = self.font.render(f"Final Score: {self.state.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 30))

        restart_text = self.font.render("Press R to restart", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20))

        exit_text = self.font.render("Press ESC to exit", True, WHITE)
        self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()

        return self._wait_for_key()

    def _show_game_win_screen(self) -> bool:
        """Show victory screen

        Returns:
            True if player wants to restart
        """
        self.screen.fill(BLACK)

        win_text = self.font.render("YOU WIN!", True, WHITE)
        self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 80))

        score_text = self.font.render(f"Final Score: {self.state.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 30))

        restart_text = self.font.render("Press R to restart", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20))

        exit_text = self.font.render("Press ESC to exit", True, WHITE)
        self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()

        return self._wait_for_key()

    def _wait_for_key(self) -> bool:
        """Wait for player input on end screen

        Returns:
            True if restart requested, False otherwise
        """
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return False
