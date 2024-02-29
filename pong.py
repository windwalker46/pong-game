import pygame
import random
from button import Button

# Initialize Pygame
pygame.init()

# Game states variables
gameState = "startMenu" # Tracks current game status (Start menu, main game, game over)
running = True # Main game loop
ballMoving = False # Flag to check if the ball is moving
font = pygame.font.Font("assets/font.ttf", 36) 

# Screen setup
screenWidth = 1280
screenHeight = 720
WHITE = (255, 255, 255) # RGB color for white

screen = pygame.display.set_mode((screenWidth, screenHeight)) # Initialize display window

# Load assets
backGround = pygame.image.load("assets/background.png") # Load background image

# Button setup for the start button
startButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screenWidth / 2, screenHeight / 2 + 40), 
                      textInput="START", font=pygame.font.Font("assets/font.ttf", 28), baseColor= WHITE, hoveringColor=(100, 100, 100))

# Button setup for options button
optionsButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screenWidth / 2, screenHeight / 2 + 130), 
                      textInput="OPTIONS", font=pygame.font.Font("assets/font.ttf", 28), baseColor= WHITE, hoveringColor=(100, 100, 100))

# Color definitions
# Paddle and Ball dimensions
paddleWidth = 15
paddleHeight = 100
ballSize = 25

# Rectangles for game objects
playerPaddle = pygame.Rect(50, (screenHeight - paddleHeight) / 2, paddleWidth, paddleHeight) # Player's paddle
opponentPaddle = pygame.Rect(screenWidth - 50 - paddleWidth, (screenHeight - paddleHeight) / 2, paddleWidth, paddleHeight) # Opponent's paddle
ball = pygame.Rect(screenWidth / 2 - ballSize / 2, screenHeight / 2 - ballSize / 2, ballSize, ballSize) # Ball

# Movement speeds
ballSpeedX = 7 # Horizontal speed of the ball
ballSpeedY = 7 # Vertical speed of the ball
playerSpeed = 0 # Current speed of the player's paddle
playerSpeedIncrement = 10 # Speed increment for player's paddle
opponentSpeed = 5 # Speed of opponent's paddle

# Scoring
playerScore = 0 # Player's score
opponentScore = 0 # Opponent's score

# Function to draw start menu
def drawStartMenu():
   global gameState
   screen.blit(backGround, (0, 0)) # Draw the background image
   
   # Set up the menu text
   font = pygame.font.Font("assets/font.ttf", 65)
   title = font.render('Pong Game', True, WHITE)
   
   # Positioning the menu text
   screen.blit(title, (screenWidth/2 - title.get_width()/2, screenHeight/2 - title.get_height() - 60))

   # Handle the start button
   mousePos = pygame.mouse.get_pos()  # Get current mouse position
   startButton.changeColor(mousePos)  # Change button color on hover
   startButton.update(screen)  # Draw button on the screen

   # Handle the options button
   optionsButton.changeColor(mousePos)  # Change button color on hover
   optionsButton.update(screen)  # Draw button on the screen
   
   pygame.display.update() # Update the display to show the menu

   # Reset Scores
   playerScore = 0
   opponentScore = 0

    # Check for mouse click on the start button
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if startButton.checkForInput(mousePos):
            gameState = "mainGame"
            ballMoving = False

# Funtion to reset the ball position
def ballRestart():
   global ballSpeedX, ballSpeedY, ballMoving
   ball.center = (screenWidth / 2, screenHeight / 2) # Center the ball
   ballSpeedY = 7 * random.choice((1, -1)) # Randomize vertical direction
   ballSpeedX = 7 * random.choice((1, -1)) # Randomize horizontal direction
   ballMoving = True # Start moving the ball

# Function to reset the game to start menu
def gameRestart():
   global playerScore, opponentScore, gameState, ballMoving
   playerScore = 0
   opponentScore = 0
   gameState = "startMenu"
   ballMoving = False

# Initialize the game clock
clock = pygame.time.Clock()

# Main game loop
while running:
  # Event handling
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
      if gameState == "mainGame":
          # Player paddle movement
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_DOWN:
                playerSpeed = playerSpeedIncrement
              elif event.key == pygame.K_UP:
                playerSpeed = -playerSpeedIncrement
          if event.type == pygame.KEYUP:
              if event.key in [pygame.K_DOWN, pygame.K_UP]:
                playerSpeed = 0
  
  # Game state management
  if gameState == "startMenu":
      drawStartMenu() # Draw the start menu
  elif gameState == "mainGame":
      # Start or restart the ball movement
      if not ballMoving:
          ballRestart()
      
      # Player paddle movement
      playerPaddle.y += playerSpeed
      # Boundary checking for player paddle
      if playerPaddle.top < 0:
          playerPaddle.top = 0
      if playerPaddle.bottom > screenHeight:
          playerPaddle.bottom = screenHeight

      # Opponent AI movement
      if ball.y > opponentPaddle.y:
          opponentPaddle.y += opponentSpeed
      elif ball.y < opponentPaddle.y:
          opponentPaddle.y -= opponentSpeed
      
      # Ball movement
      ball.x += ballSpeedX
      ball.y += ballSpeedY
      
      # Ball boundary checking and scoring
      if ball.top <= 0 or ball.bottom >= screenHeight:
          ballSpeedY *= -1 # Invert Y speed
          ball.y = 0 if ball.top <= 0 else screenHeight - ballSize

      if ball.right > screenWidth:
          playerScore += 1
          if playerScore == 5:
              gameRestart()
          else:
              ballRestart()
      elif ball.left < 0:
          opponentScore += 1
          if opponentScore == 5:
                gameRestart()
          else:
              ballRestart()
      
        # Collision detection
      if ball.colliderect(playerPaddle) or ball.colliderect(opponentPaddle):
        ballSpeedX *= -1  # Invert X speed
        # Adjust ball position and speed after collision
        ball.x += ballSpeedX
        # Adjust Y speed based on collision position
        if ball.bottom < playerPaddle.centery or ball.bottom < opponentPaddle.centery:
            ballSpeedY = -abs(ballSpeedY)
        elif ball.top > playerPaddle.centery or ball.top > opponentPaddle.centery:
            ballSpeedY = abs(ballSpeedY)
      
      # Draw the game objects
      screen.fill((0, 0, 0))
      pygame.draw.rect(screen, WHITE, playerPaddle) # Draw player's paddle
      pygame.draw.rect(screen, WHITE, opponentPaddle) # Draw opponent's paddle
      pygame.draw.ellipse(screen, WHITE, ball) # Draw ball

      # Display scores
      playerText = font.render(str(playerScore), True, WHITE)
      opponentText = font.render(str(opponentScore), True, WHITE)
      screen.blit(playerText, (screenWidth / 4, 20))
      screen.blit(opponentText, (3 * screenWidth / 4, 20))

      pygame.display.flip() # Update the display

    
  elif gameState == "game_over":
      drawStartMenu() # Placeholder for game oveer screen here
      
  clock.tick(60) # Set FPS to 60
  
pygame.quit() # Quit Pygame when the loop ends