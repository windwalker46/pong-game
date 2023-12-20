# pong.py
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
game_state = "start_menu"
running = True
game_running = False
ball_moving = False

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
opponent_speed = 0.6  # Maintained speed for opponent

# Scoring
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def draw_start_menu():
    global game_state, game_running
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('My Game', True, (255, 255, 255))
    start_button = font.render('Start', True, (255, 255, 255))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/2))
    screen.blit(start_button, (screen_width/2 - start_button.get_width()/2, screen_height/2 + start_button.get_height()/2))
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        game_state = "main_game"
        game_running = True
        ball_moving = False

# Reset the ball
def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y = 0.5 * random.choice((1,-1))
    ball_speed_x = 0.5 * random.choice((1,-1))
    ball_moving = True

# Restart the game
def game_restart():
    global player_score, opponent_score, game_state, ball_moving
    player_score = 0
    opponent_score = 0
    game_state = "start_menu"
    ball_moving = False

# Initialize the clock
clock = pygame.time.Clock()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == "start_menu":
        draw_start_menu()
    
    elif game_state == "main_game" and game_running:
        if not ball_moving:
            ball_restart()

        # Event handling, player and opponent movements, ball collision, scoring, etc.

        # Drawing the paddles, ball, and score
        screen.fill((0, 0, 0)) #Clear screen by filling it with black
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, opponent_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        player_text = font.render(str(player_score), True, WHITE)
        opponent_text = font.render(str(opponent_score), True, WHITE)
        screen.blit(player_text, (screen_width / 4, 20))
        screen.blit(opponent_text, (3 * screen_width / 4, 20))

        pygame.display.flip()
    
    clock.tick(60)

pygame.quit()