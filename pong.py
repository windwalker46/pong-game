# pong.py
import pygame
import random

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
paddle_height = 100
ball_size = 25

# Create Rects for paddles and ball
player_paddle = pygame.Rect(50, (screen_height - paddle_height) / 2, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(screen_width - 50 - paddle_width, (screen_height - paddle_height) / 2, paddle_width, paddle_height)
ball = pygame.Rect(screen_width / 2 - ball_size / 2, screen_height / 2 - ball_size / 2, ball_size, ball_size)

# Ball Speed
ball_speed_x = 100  # Significantly reduced speed
ball_speed_y = 100  # Significantly reduced speed

# Player Paddle Speed
player_speed = 0
player_speed_increment = 3  # Maintained precise control speed

# Opponent Paddle Speed
opponent_speed = 0.8  # Maintained speed for opponent

# Scoring
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y = 0.5 * random.choice((1,-1))
    ball_speed_x = 0.5 * random.choice((1,-1))

def game_restart():
    global player_score, opponent_score
    player_score = 0
    opponent_score = 0
    ball_restart()

# Start the game
game_restart()

# Initialize the clock
clock = pygame.time.Clock()

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
    if player_paddle.top < 0:
        player_paddle.top = 0
    if player_paddle.bottom > screen_height:
        player_paddle.bottom = screen_height

    # Opponent Paddle Movement
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += opponent_speed
    elif opponent_paddle.centery > ball.centery:
        opponent_paddle.y -= opponent_speed

    # Store the position as floats
    player_paddle_y = float(player_paddle.y)
    opponent_paddle_y = float(opponent_paddle.y)
    ball_x = float(ball.x)
    ball_y = float(ball.y)

    # Update the position using the float values
    player_paddle_y += player_speed
    opponent_paddle_y += opponent_speed
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Assign the integer values to the Rect objects
    player_paddle.y = int(player_paddle_y)
    opponent_paddle.y = int(opponent_paddle_y)
    ball.x = int(ball_x)
    ball.y = int(ball_y)

    # Ball Movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball Collision with Top and Bottom Walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Ball gets stuck behind paddle
    if ball.right >= opponent_paddle.left and ball.left <= opponent_paddle.right:
        if ball.top >= opponent_paddle.bottom or ball.bottom <= opponent_paddle.top:
            ball_restart()

    # Paddle collision with top and bottom
    if player_paddle.top <= 0:
        player_paddle.top = 0
    if player_paddle.bottom >= screen_height:
        player_paddle.bottom = screen_height

    # Ball and Paddle Collision
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1
        # Reverse y direction if ball is moving up and hits the top of the paddle, or if it's moving down and hits the bottom
        if (ball_speed_y < 0 and ball.bottom <= player_paddle.top) or (ball_speed_y > 0 and ball.top >= player_paddle.bottom):
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

    # Control the game speed and adjust the ball speed based on the time that has passed
    timedelta = clock.tick(480) 

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
