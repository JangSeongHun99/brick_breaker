import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

BALL_RADIUS = 10
BALL_SPEED = 4
PIERCE_LIMIT = 1

BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 35

FONT = pygame.font.SysFont("Arial", 24)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30), (PADDLE_WIDTH, PADDLE_HEIGHT))

    def move(self, ball):
        predicted_x = self.predict_ball_landing(ball)
        if predicted_x < self.rect.centerx and self.rect.left > 0:
            self.rect.x -= PADDLE_SPEED
        elif predicted_x > self.rect.centerx and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PADDLE_SPEED

    def predict_ball_landing(self, ball):
        if ball.dy > 0:
            time_to_bottom = (SCREEN_HEIGHT - ball.rect.bottom) / ball.dy
            predicted_x = ball.rect.x + ball.dx * time_to_bottom
            while predicted_x < 0 or predicted_x > SCREEN_WIDTH:
                if predicted_x < 0:
                    predicted_x = -predicted_x
                elif predicted_x > SCREEN_WIDTH:
                    predicted_x = 2 * SCREEN_WIDTH - predicted_x
            return predicted_x
        else:
            return self.rect.centerx

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.dy = -BALL_SPEED
        self.pierce_count = 0

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def reset_pierce_count(self):
        self.pierce_count = 0

    def draw(self):
        pygame.draw.ellipse(screen, RED, self.rect)

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
            y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
            bricks.append(Brick(x, y))
    return bricks

def draw_score(score):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    score_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
    score_y = 10
    screen.blit(score_text, (score_x, score_y))

def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = FONT.render("Game Over!", True, RED)
    score_text = FONT.render(f"Your Score: {score}", True, WHITE)
    restart_text = FONT.render("Press any key to restart", True, WHITE)
    game_over_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2
    game_over_y = SCREEN_HEIGHT // 2 - 50
    score_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
    score_y = SCREEN_HEIGHT // 2
    restart_x = SCREEN_WIDTH // 2 - restart_text.get_width() // 2
    restart_y = SCREEN_HEIGHT // 2 + 50
    screen.blit(game_over_text, (game_over_x, game_over_y))
    screen.blit(score_text, (score_x, score_y))
    screen.blit(restart_text, (restart_x, restart_y))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    while True:
        paddle = Paddle()
        ball = Ball()
        bricks = create_bricks()
        score = 0
        running = True
        while running:
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            ball.move()
            paddle.move(ball)
            if ball.rect.colliderect(paddle.rect):
                ball.dy = -ball.dy
                ball.reset_pierce_count()
            for brick in bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    bricks.remove(brick)
                    score += 10
                    ball.pierce_count += 1
                    if ball.pierce_count >= PIERCE_LIMIT:
                        ball.dy = -ball.dy
                        ball.reset_pierce_count()
                        break
            if ball.rect.top > SCREEN_HEIGHT:
                game_over_screen(score)
                running = False
            paddle.draw()
            ball.draw()
            for brick in bricks:
                brick.draw()
            draw_score(score)
            if not bricks:
                game_over_screen(score)
                running = False
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
