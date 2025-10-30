import pygame
import sys
import random
from levels import LEVELS

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
LASER_WIDTH = 5
LASER_HEIGHT = 15
LASER_SPEED = 10

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Game Classes ---
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = WHITE
        self.laser_active = False
        self.catch_active = False
        self.caught_ball = None

    def move(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.caught_ball:
            self.caught_ball.rect.centerx = self.rect.centerx

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = RED
        self.dx = 5
        self.dy = -5
        self.is_caught = False

    def move(self, paddle, bricks, power_ups, enemies, sound_manager, doh):
        if self.is_caught:
            return

        self.rect.x += self.dx
        self.rect.y += self.dy

        # Collision with walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
            sound_manager.play(sound_manager.bounce)
        if self.rect.top <= 0:
            self.dy *= -1
            sound_manager.play(sound_manager.bounce)

        # Collision with paddle
        if self.rect.colliderect(paddle.rect):
            if paddle.catch_active:
                self.is_caught = True
                paddle.caught_ball = self
                self.rect.bottom = paddle.rect.top
            else:
                self.dy *= -1
                sound_manager.play(sound_manager.bounce)

        # Collision with bricks
        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                if brick.hit():
                    bricks.remove(brick)
                    # self.score is not accessible here, score is in Game class
                    sound_manager.play(sound_manager.brick_destroy)
                    if random.random() < 0.3: # 30% chance to drop a power-up
                        power_up_type = random.choice(['enlarge', 'slow', 'laser', 'catch', 'disrupt', 'break', 'player'])
                        power_ups.append(PowerUp(brick.rect.centerx, brick.rect.centery, power_up_type))
                self.dy *= -1
                break
        
        # Collision with enemies
        for enemy in enemies[:]:
            if self.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                # self.score is not accessible here, score is in Game class
                self.dy *= -1
                break

        # Collision with Doh
        if doh and self.rect.colliderect(doh.rect):
            if doh.hit():
                return True # Doh is defeated
            self.dy *= -1
            sound_manager.play(sound_manager.bounce)
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)

class Brick:
    def __init__(self, x, y, brick_type):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.type = brick_type
        self.hits = 0
        if self.type == 'n':
            self.color = GREEN
        elif self.type == 's':
            self.color = (192, 192, 192)
        elif self.type == 'g':
            self.color = (255, 215, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def hit(self):
        if self.type == 'n':
            self.hits += 1
            return self.hits >= 1
        elif self.type == 's':
            self.hits += 1
            if self.hits == 1:
                self.color = (160, 160, 160)
            return self.hits >= 2
        elif self.type == 'g':
            return False
        return False

class PowerUp:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x - 15, y - 7, 30, 14)
        self.type = type
        self.color = BLUE
        self.dy = 3

    def move(self):
        self.rect.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - LASER_WIDTH // 2, y, LASER_WIDTH, LASER_HEIGHT)
        self.color = YELLOW
        self.dy = -LASER_SPEED

    def move(self):
        self.rect.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 30), 0, 30, 30)
        self.color = (255, 165, 0) # Orange
        self.dy = 2

    def move(self):
        self.rect.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.brick_destroy = self.load_sound("sounds/brick_destroy.wav")
        self.powerup = self.load_sound("sounds/powerup.wav")
        self.bounce = self.load_sound("sounds/bounce.wav")

    def load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            print(f"Cannot load sound: {path}")
        return None

    def play(self, sound):
        if sound:
            sound.play()

class Doh:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 50, 300, 100)
        self.color = (128, 0, 128) # Purple
        self.hp = 16

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

class Bomb:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 10, y, 20, 20)
        self.color = (255, 0, 255) # Magenta
        self.dy = 4

    def move(self):
        self.rect.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("VC-Arkanoid")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 0
        self.lives = 3
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.sound_manager = SoundManager()
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.bricks = self.create_bricks(self.level)
        self.power_ups = []
        self.lasers = []
        self.enemies = []
        self.doh = None
        self.bombs = []
        self.power_up_timers = {}
        self.enemy_spawn_timer = 0
        self.bomb_spawn_timer = 0

    def create_bricks(self, level_index):
        bricks = []
        if level_index < len(LEVELS):
            level_data = LEVELS[level_index]
            for row_index, row in enumerate(level_data):
                for col_index, brick_char in enumerate(row):
                    if brick_char != ' ':
                        brick_type = ''
                        if brick_char == 'n':
                            brick_type = 'n'
                        elif brick_char == 's':
                            brick_type = 's'
                        elif brick_char == 'g':
                            brick_type = 'g'
                        brick = Brick(col_index * BRICK_WIDTH, row_index * BRICK_HEIGHT + 50, brick_type)
                        bricks.append(brick)
        return bricks

    def stage_clear(self):
        return not self.bricks and not self.doh

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        if self.lives <= 0:
            self.show_game_over_screen()
        else:
            self.show_game_win_screen()
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.paddle.laser_active:
                    self.lasers.append(Laser(self.paddle.rect.centerx, self.paddle.rect.top))
                if self.paddle.caught_ball:
                    self.paddle.caught_ball.is_caught = False
                    self.paddle.caught_ball.dy *= -1
                    self.paddle.caught_ball = None

    def update(self):
        self.paddle.move()
        for ball in self.balls[:]:
            doh_defeated = ball.move(self.paddle, self.bricks, self.power_ups, self.enemies, self.sound_manager, self.doh)
            if doh_defeated:
                self.doh = None
            if ball.rect.bottom >= SCREEN_HEIGHT:
                self.balls.remove(ball)

        if not self.balls:
            self.lives -= 1
            if self.lives > 0:
                self.balls.append(Ball())
            else:
                self.running = False # Game Over

        self.update_power_ups()
        self.update_lasers()
        self.update_enemies()
        self.update_boss()
        self.update_bombs()

        if self.stage_clear():
            self.next_level()

    def next_level(self):
        self.level += 1
        if self.level < len(LEVELS):
            self.bricks = self.create_bricks(self.level)
            self.balls = [Ball()]
            self.power_ups = []
            self.lasers = []
            self.enemies = []
            self.power_up_timers = {}
            if self.level == 1: # Boss level
                self.doh = Doh()
        else:
            self.doh = None # No more boss
            self.running = False # You win

    def update_power_ups(self):
        for power_up in self.power_ups[:]:
            power_up.move()
            if power_up.rect.colliderect(self.paddle.rect):
                self.apply_power_up(power_up)
                self.power_ups.remove(power_up)
                self.sound_manager.play(self.sound_manager.powerup)
            elif power_up.rect.top > SCREEN_HEIGHT:
                self.power_ups.remove(power_up)

        for power_up_type, timer in list(self.power_up_timers.items()):
            self.power_up_timers[power_up_type] -= 1
            if self.power_up_timers[power_up_type] <= 0:
                self.revert_power_up(power_up_type)
                del self.power_up_timers[power_up_type]

    def update_lasers(self):
        for laser in self.lasers[:]:
            laser.move()
            if laser.rect.bottom < 0:
                self.lasers.remove(laser)
            else:
                for brick in self.bricks[:]:
                    if laser.rect.colliderect(brick.rect):
                        if brick.hit():
                            self.bricks.remove(brick)
                            self.score += 10
                        self.lasers.remove(laser)
                        break
                for enemy in self.enemies[:]:
                    if laser.rect.colliderect(enemy.rect):
                        self.enemies.remove(enemy)
                        self.score += 50
                        self.lasers.remove(laser)
                        break

    def update_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= 300: # Spawn an enemy every 5 seconds
            self.enemy_spawn_timer = 0
            self.enemies.append(Enemy())

        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)

    def update_boss(self):
        if self.doh:
            self.bomb_spawn_timer += 1
            if self.bomb_spawn_timer >= 120: # Spawn a bomb every 2 seconds
                self.bomb_spawn_timer = 0
                self.bombs.append(Bomb(self.doh.rect.centerx, self.doh.rect.bottom))

    def update_bombs(self):
        for bomb in self.bombs[:]:
            bomb.move()
            if bomb.rect.colliderect(self.paddle.rect):
                self.lives -= 1
                self.bombs.remove(bomb)
                if self.lives <= 0:
                    self.running = False
            elif bomb.rect.top > SCREEN_HEIGHT:
                self.bombs.remove(bomb)

    def apply_power_up(self, power_up):
        if power_up.type == 'enlarge':
            self.paddle.rect.width = PADDLE_WIDTH * 1.5
            self.power_up_timers['enlarge'] = 500 # 500 frames
        elif power_up.type == 'slow':
            for ball in self.balls:
                ball.dx /= 2
                ball.dy /= 2
            self.power_up_timers['slow'] = 500
        elif power_up.type == 'laser':
            self.paddle.laser_active = True
            self.power_up_timers['laser'] = 500
        elif power_up.type == 'catch':
            self.paddle.catch_active = True
            self.power_up_timers['catch'] = 5000 # A long time, or until ball is released
        elif power_up.type == 'disrupt':
            if self.balls:
                original_ball = self.balls[0]
                new_ball1 = Ball()
                new_ball1.rect.center = original_ball.rect.center
                new_ball1.dx = -original_ball.dx
                new_ball1.dy = original_ball.dy
                new_ball2 = Ball()
                new_ball2.rect.center = original_ball.rect.center
                new_ball2.dx = original_ball.dx
                new_ball2.dy = -original_ball.dy
                self.balls.append(new_ball1)
                self.balls.append(new__ball2)
        elif power_up.type == 'break':
            self.next_level()
        elif power_up.type == 'player':
            self.lives += 1

    def revert_power_up(self, power_up_type):
        if power_up_type == 'enlarge':
            self.paddle.rect.width = PADDLE_WIDTH
        elif power_up_type == 'slow':
            for ball in self.balls:
                ball.dx *= 2
                ball.dy *= 2
        elif power_up_type == 'laser':
            self.paddle.laser_active = False
        elif power_up_type == 'catch':
            self.paddle.catch_active = False
            if self.paddle.caught_ball:
                self.paddle.caught_ball.is_caught = False
                self.paddle.caught_ball = None

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, WHITE)
        self.screen.blit(surface, (x, y))

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        self.draw_text("Press any key to exit", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_win_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("YOU WIN!", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50)
        self.draw_text("Press any key to exit", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw(self):
        self.screen.fill(BLACK)
        self.paddle.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        for laser in self.lasers:
            laser.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        if self.doh:
            self.doh.draw(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)
        
        # Draw UI
        self.draw_text(f"Score: {self.score}", 10, 10)
        self.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 120, 10)
        self.draw_text(f"Level: {self.level + 1}", SCREEN_WIDTH // 2 - 50, 10)

        pygame.display.flip()

# --- Main ---
if __name__ == "__main__":
    game = Game()
    game.run()
