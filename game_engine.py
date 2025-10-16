import pygame
from .ball import Ball
from .paddle import Paddle

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        # Paddles
        paddle_width, paddle_height = 20, 100
        self.player = Paddle(50, self.height // 2 - 50, paddle_width, paddle_height, speed=7, screen_height=self.height)
        self.ai = Paddle(self.width - 70, self.height // 2 - 50, paddle_width, paddle_height, speed=5, screen_height=self.height)

        # Ball
        self.ball = Ball(self.width // 2 - 15, self.height // 2 - 15, 30, 30, self.width, self.height)

        # Scores
        self.player_score = 0
        self.ai_score = 0

        # Font for score and messages
        self.font = pygame.font.SysFont(None, 40)

        # Load sounds
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

    def handle_input(self, events):
        """Handle player paddle input (W/S keys)"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(up=True)
        if keys[pygame.K_s]:
            self.player.move(up=False)

    def update(self):
        prev_vel_x = self.ball.velocity_x
        prev_vel_y = self.ball.velocity_y

        # Move ball
        self.ball.move()

        # Wall collision sound
        if self.ball.velocity_y != prev_vel_y:
            self.sound_wall.play()

        # Paddle collision
        if self.ball.rect().colliderect(self.player.rect()) or self.ball.rect().colliderect(self.ai.rect()):
            self.ball.check_collision(self.player, self.ai)
            self.sound_paddle.play()

        # Simple AI: follow the ball
        if self.ball.y < self.ai.y + self.ai.height // 2:
            self.ai.move(up=True)
        elif self.ball.y > self.ai.y + self.ai.height // 2:
            self.ai.move(up=False)

        # Check scoring
        scored = False
        if self.ball.x <= 0:
            self.ai_score += 1
            scored = True
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            scored = True

        if scored:
            self.sound_score.play()
            self.ball.reset()

    def render(self, screen):
        # Draw paddles
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())

        # Draw ball
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen, target_score=5):
        """Check if either player reached the winning score"""
        winner_text = ""
        if self.player_score >= target_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= target_score:
            winner_text = "AI Wins!"
        else:
            return False  # game continues

        # Display winner message
        screen.fill((0, 0, 0))
        text_surface = self.font.render(winner_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Wait 2 seconds so player can see it
        pygame.time.delay(2000)
        return True

    def reset_game(self):
        """Reset scores and ball for replay"""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
