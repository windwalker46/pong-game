import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
game_state = "start_menu"
running = True
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
ball_speed_x = 7 # Adjusted for diagonal movement
ball_speed_y = 7

# Player Paddle Speed
player_speed = 0
player_speed_increment = 10

# Opponent Paddle Speed
opponent_speed = 5

# Scoring
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

def draw_start_menu():
   global game_state
   screen.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 50)
   title = font.render('Pong Game', True, (255, 255, 255))
   font_instruction = pygame.font.SysFont('arial', 30)
   press_enter = font_instruction.render('Press Enter To Play', True, (255, 255, 255))
   screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height() - 30))
   screen.blit(press_enter, (screen_width/2 - press_enter.get_width()/2, screen_height/2 + title.get_height() - 30))
   pygame.display.update()

   # Reset Scores
   player_score = 0
   opponent_score = 0

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

def ball_restart():
   global ball_speed_x, ball_speed_y, ball_moving
   ball.center = (screen_width / 2, screen_height / 2)
   ball_speed_y = 7 * random.choice((1, -1))
   ball_speed_x = 7 * random.choice((1, -1))
   ball_moving = True

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
      if game_state == "main_game":
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_DOWN:
                player_speed = player_speed_increment
              elif event.key == pygame.K_UP:
                player_speed = -player_speed_increment
          if event.type == pygame.KEYUP:
              if event.key in [pygame.K_DOWN, pygame.K_UP]:
                player_speed = 0

  if game_state == "start_menu":
      draw_start_menu()
  elif game_state == "main_game":
      if not ball_moving:
          ball_restart()

      player_paddle.y += player_speed
      if player_paddle.top < 0:
          player_paddle.top = 0
      if player_paddle.bottom > screen_height:
          player_paddle.bottom = screen_height

      # Make the opponent's paddle follow the ball
      if ball.y > opponent_paddle.y:
          opponent_paddle.y += opponent_speed
      elif ball.y < opponent_paddle.y:
          opponent_paddle.y -= opponent_speed

      ball.x += ball_speed_x
      ball.y += ball_speed_y

      if ball.top <= 0 or ball.bottom >= screen_height:
          ball_speed_y *= -1
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

      if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
          ball_speed_x *= -1
          # Update ball position immediately after collision
          ball.x += ball_speed_x 
          # Check if ball is hitting top edge
          if ball.bottom < player_paddle.centery:
              ball_speed_y = -abs(ball_speed_y)
          # Check if ball is hitting the bottom edge
          elif ball.top > player_paddle.centery:
              ball_speed_y = abs(ball_speed_y)
      elif ball.colliderect(opponent_paddle):
          ball_speed_x *= -1
          # Update ball position immediately after collision
          ball.x += ball_speed_x
          # Check if ball is hitting top edge
          if ball.bottom < opponent_paddle.centery:
              ball_speed_y = -abs(ball_speed_y)
          # Check if ball is htting the bottom edge
          elif ball.top > opponent_paddle.centery:
              ball_speed_y = abs(ball_speed_y)

      screen.fill((0, 0, 0))
      pygame.draw.rect(screen, WHITE, player_paddle)
      pygame.draw.rect(screen, WHITE, opponent_paddle)
      pygame.draw.ellipse(screen, WHITE, ball)
      player_text = font.render(str(player_score), True, WHITE)
      opponent_text = font.render(str(opponent_score), True, WHITE)
      screen.blit(player_text, (screen_width / 4, 20))
      screen.blit(opponent_text, (3 * screen_width / 4, 20))

      pygame.display.flip()

    
  elif game_state == "game_over":
      draw_start_menu()
      
  clock.tick(60)
  
pygame.quit()