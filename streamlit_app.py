import streamlit as st
import pygame
import time

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
ROW_COUNT = 5
COLUMN_COUNT = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Block Breaker')

# Paddle
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx, ball_dy = 5, -5

# Bricks
bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for row in range(ROW_COUNT) for col in range(COLUMN_COUNT)]

def draw():
    screen.fill(BLUE)
    pygame.draw.rect(screen, GREEN, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)
    pygame.display.flip()

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-10, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(10, 0)

def move_ball():
    global ball_dx, ball_dy
    ball.move_ip(ball_dx, ball_dy)
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_dx = -ball_dx
    if ball.top <= 0 or ball.colliderect(paddle):
        ball_dy = -ball_dy
    if ball.bottom >= SCREEN_HEIGHT:
        return False
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        brick = bricks.pop(hit_index)
        ball_dy = -ball_dy
    return True

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move_paddle()
        if not move_ball():
            running = False
        
        draw()
        clock.tick(30)

    pygame.quit()

st.title("Block Breaker Game")

if st.button('Start Game'):
    main()
