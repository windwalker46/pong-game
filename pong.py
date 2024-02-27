import pygame
import random

# Initialize Pygame
pygame.init()

# Game states variables
game_state = "start_menu" # Tracks current game status (Start menu, main game, game over)
running = True # Main game loop
ball_moving = False # Flag to check if the ball is moving

# Screen setup
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # Initialize display window

# Load assets
back_ground = pygame.image.load("assets/background.png") # Load background image

# Color definitions
WHITE = (255, 255, 255) # RGB color for white

# Paddle and Ball dimensions
paddle_width = 15
paddle_height = 100
ball_size = 25

# Rectangles for game objects
player_paddle = pygame.Rect(50, (screen_height - paddle_height) / 2, paddle_width, paddle_height) # Player's paddle
opponent_paddle = pygame.Rect(screen_width - 50 - paddle_width, (screen_height - paddle_height) / 2, paddle_width, paddle_height) # Opponent's paddle
ball = pygame.Rect(screen_width / 2 - ball_size / 2, screen_height / 2 - ball_size / 2, ball_size, ball_size) # Ball

# Movement speeds
ball_speed_x = 7 # Horizontal speed of the ball
ball_speed_y = 7 # Vertical speed of the ball
player_speed = 0 # Current speed of the player's paddle
player_speed_increment = 10 # Speed increment for player's paddle
opponent_speed = 5 # Speed of opponent's paddle

# Scoring
player_score = 0 # Player's score
opponent_score = 0 # Opponent's score
font = pygame.font.Font("assets/font.ttf", 36) # Font for displaying scores

# Function to draw start menu
def draw_start_menu():
   global game_state
   screen.blit(back_ground, (0, 0)) # Draw the background image
   
   # Set up the menu text
   font = pygame.font.Font("assets/font.ttf", 60)
   title = font.render('Pong Game', True, (255, 255, 255))
   font_instruction = pygame.font.Font("assets/font.ttf", 20)
   press_enter = font_instruction.render('Press Enter To Play', True, (255, 255, 255))
   
   # Positioning the menu text
   screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height() - 30))
   screen.blit(press_enter, (screen_width/2 - press_enter.get_width()/2, screen_height/2 + title.get_height() - 30))
   
   pygame.display.update() # Update the display to show the menu

   # Reset Scores
   player_score = 0
   opponent_score = 0

   # Wait for the player input to start the game
   waiting_for_key = True
   while waiting_for_key:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_RETURN:
                  game_state = "main_game"
                  ball_moving = False
                  waiting_for_key = False

# Funtion to reset the ball position
def ball_restart():
   global ball_speed_x, ball_speed_y, ball_moving
   ball.center = (screen_width / 2, screen_height / 2) # Center the ball
   ball_speed_y = 7 * random.choice((1, -1)) # Randomize vertical direction
   ball_speed_x = 7 * random.choice((1, -1)) # Randomize horizontal direction
   ball_moving = True # Start moving the ball

# Function to reset the game to start menu
def game_restart():
   global player_score, opponent_score, game_state, ball_moving
   player_score = 0
   opponent_score = 0
   game_state = "start_menu"
   ball_moving = False

# Initialize the game clock
clock = pygame.time.Clock()

# Main game loop
while running:
  # Event handling
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
      if game_state == "main_game":
          # Player paddle movement
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_DOWN:
                player_speed = player_speed_increment
              elif event.key == pygame.K_UP:
                player_speed = -player_speed_increment
          if event.type == pygame.KEYUP:
              if event.key in [pygame.K_DOWN, pygame.K_UP]:
                player_speed = 0
  
  # Game state management
  if game_state == "start_menu":
      draw_start_menu() # Draw the start menu
  elif game_state == "main_game":
      # Start or restart the ball movement
      if not ball_moving:
          ball_restart()
      
      # Player paddle movement
      player_paddle.y += player_speed
      # Boundary checking for player paddle
      if player_paddle.top < 0:
          player_paddle.top = 0
      if player_paddle.bottom > screen_height:
          player_paddle.bottom = screen_height

      # Opponent AI movement
      if ball.y > opponent_paddle.y:
          opponent_paddle.y += opponent_speed
      elif ball.y < opponent_paddle.y:
          opponent_paddle.y -= opponent_speed
      
      # Ball movement
      ball.x += ball_speed_x
      ball.y += ball_speed_y
      
      # Ball boundary checking and scoring
      if ball.top <= 0 or ball.bottom >= screen_height:
          ball_speed_y *= -1 # Invert Y speed
          ball.y = 0 if ball.top <= 0 else screen_height - ball_size

      if ball.right > screen_width:
          player_score += 1
          if player_score == 5:
              game_restart()
          else:
              ball_restart()
      elif ball.left < 0:
          opponent_score += 1
          if opponent_score == 5:
                game_restart()
          else:
              ball_restart()
      
        # Collision detection
      if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1  # Invert X speed
        # Adjust ball position and speed after collision
        ball.x += ball_speed_x
        # Adjust Y speed based on collision position
        if ball.bottom < player_paddle.centery or ball.bottom < opponent_paddle.centery:
            ball_speed_y = -abs(ball_speed_y)
        elif ball.top > player_paddle.centery or ball.top > opponent_paddle.centery:
            ball_speed_y = abs(ball_speed_y)
      
      # Draw the game objects
      screen.fill((0, 0, 0))
      pygame.draw.rect(screen, WHITE, player_paddle) # Draw player's paddle
      pygame.draw.rect(screen, WHITE, opponent_paddle) # Draw opponent's paddle
      pygame.draw.ellipse(screen, WHITE, ball) # Draw ball

      # Display scores
      player_text = font.render(str(player_score), True, WHITE)
      opponent_text = font.render(str(opponent_score), True, WHITE)
      screen.blit(player_text, (screen_width / 4, 20))
      screen.blit(opponent_text, (3 * screen_width / 4, 20))

      pygame.display.flip() # Update the display

    
  elif game_state == "game_over":
      draw_start_menu() # Placeholder for game oveer screen here
      
  clock.tick(60) # Set FPS to 60
  
pygame.quit() # Quit Pygame when the loop ends