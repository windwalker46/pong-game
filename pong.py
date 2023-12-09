# pong.py
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)

# Paddle and Ball
paddle_width = 15
paddle_height = 90
ball_size = 20

# Create Rects for paddles and ball
player_paddle = pygame.Rect(50, (screen_height - paddle_height) / 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(screen_width - 50 - paddle_width, (screen_height - paddle_height) / 2, paddle_width, paddle_height)
ball = pygame.Rect(screen_width / 2 - ball_size / 2, screen_height / 2 - ball_size / 2, ball_size, ball_size)

# Ball Speed
ball_speed_x = 7
ball_speed_y = 7

# Player Paddle Speed
player_speed = 0
player_speed_increment = 10

# Opponent Paddle Speed
opponent_speed = 7

# Scoring
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x *= -1
    ball_speed_y *= -1

def game_restart():
    global player_score, opponent_score
    player_score = 0
    opponent_score = 0
    ball_restart()

# Start the game
game_restart()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player_speed = player_speed_increment
    elif keys[pygame.K_UP]:
        player_speed = -player_speed_increment
    else:
        player_speed = 0

    # Player Paddle Movement
    player_paddle.y += player_speed
    if player_paddle.top <= 0:
        player_paddle.top = 0
    if player_paddle.bottom >= screen_height:
        player_paddle.bottom = screen_height

    # Opponent Paddle Movement
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += opponent_speed
    elif opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= opponent_speed

    # Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball and Paddle Collision
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Ball Collision with Top and Bottom Walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Ball Out of Bounds
    if ball.left <= 0:
        opponent_score += 1
        ball_restart()
    if ball.right >= screen_width:
        player_score += 1
        ball_restart()

    # Drawing the paddles and ball
    screen.fill((0, 0, 0))  # Clear screen by filling it with black
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Display Score
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (screen_width / 4, 20))
    screen.blit(opponent_text, (3 * screen_width / 4, 20))

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
