import pygame
import random
from button import Button, initButton
from gameFunctions import drawStartMenu, drawOptionsMenu, ballRestart

# Initialize Pygame
pygame.init()

# Game states variables
gameState = "startMenu"  # Tracks current game status (Start menu, main game, game over)
running = True  # Main game loop
ballMoving = False  # Flag to check if the ball is moving
winningScore = 3  # Default winning score
font = pygame.font.Font("assets/font.ttf", 36)
clock = pygame.time.Clock()  # Initialize Pygame clock

# Screen setup
screenWidth = 1280
screenHeight = 720
WHITE = (255, 255, 255)  # RGB color for white
screen = pygame.display.set_mode((screenWidth, screenHeight))  # Initialize display window
backGround = pygame.image.load("assets/background.png")  # Load background image

# Initialize buttons
startButton, optionsButton, increaseScoreButton, decreaseScoreButton, backButton = initButton(screenWidth, screenHeight, font, WHITE, (100, 100, 100))

# Paddle and Ball setup
paddleWidth = 15
paddleHeight = 100
ballSize = 25
playerPaddle = pygame.Rect(50, (screenHeight - paddleHeight) / 2, paddleWidth, paddleHeight)
opponentPaddle = pygame.Rect(screenWidth - 50 - paddleWidth, (screenHeight - paddleHeight) / 2, paddleWidth, paddleHeight)
ball = pygame.Rect(screenWidth / 2 - ballSize / 2, screenHeight / 2 - ballSize / 2, ballSize, ballSize) # Initial position of the ball

# Movement speeds and Scoring
ballSpeedX = 7  # Initial horizontal speed of the ball
ballSpeedY = 7  # Initial vertical speed of the ball
playerSpeedIncrement = 10  # Speed increment for player's paddle
opponentSpeed = 5  # Speed of opponent's paddle
playerScore = 0  # Player's score
opponentScore = 0  # Opponent's score

# Main game loop
while running:
    mousePos = pygame.mouse.get_pos()
    events = pygame.event.get()  # Retrieve all events once and use this list for processing
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        # Start menu and options menu handling
        if gameState == "startMenu": 
            drawStartMenu(screen, backGround, font, WHITE, screenWidth, screenHeight, startButton, optionsButton)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startButton.checkForInput(mousePos):
                        gameState = "mainGame"
                        ballMoving = True  # Ball should move when the game starts
                        playerScore, opponentScore = 0, 0
                    elif optionsButton.checkForInput(mousePos):
                        gameState = "optionsMenu"
        elif gameState == "optionsMenu":
            drawOptionsMenu(screen, backGround, font, WHITE, screenWidth, screenHeight, winningScore, [increaseScoreButton, decreaseScoreButton, backButton])
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if increaseScoreButton.checkForInput(mousePos):
                        winningScore += 1  # Adjust winning score
                    elif decreaseScoreButton.checkForInput(mousePos) and winningScore > 1:
                        winningScore -= 1  # Adjust winning score
                    elif backButton.checkForInput(mousePos):
                        gameState = "startMenu"
    # loop to handle main game logic
    if gameState == "mainGame" and ballMoving:
        # Handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            playerPaddle.y -= playerSpeedIncrement
        elif keys[pygame.K_DOWN]:
            playerPaddle.y += playerSpeedIncrement

        # Ensure paddle remains within screen bounds
        playerPaddle.clamp_ip(screen.get_rect())

        # Opponent AI follows the ball
        if opponentPaddle.centery < ball.centery:
            opponentPaddle.y += opponentSpeed
        elif opponentPaddle.centery > ball.centery:
            opponentPaddle.y -= opponentSpeed

        # Ball movement and collision handling
        ball.x += ballSpeedX
        ball.y += ballSpeedY
        if ball.top <= 0 or ball.bottom >= screenHeight or ball.colliderect(playerPaddle) or ball.colliderect(opponentPaddle):
            ballSpeedY = -ballSpeedY if ball.top <= 0 or ball.bottom >= screenHeight else ballSpeedY
            ballSpeedX = -ballSpeedX if ball.colliderect(playerPaddle) or ball.colliderect(opponentPaddle) else ballSpeedX

        # Score update and check for game over
        if ball.right >= screenWidth or ball.left <= 0:
            if ball.right >= screenWidth:
                playerScore += 1
            else:
                opponentScore += 1

            ballSpeedX, ballSpeedY, ballMoving = ballRestart(ball, screenWidth, screenHeight, playerScore, opponentScore, winningScore)

        # Check for winning condition is met to update gameState
        if playerScore >= winningScore:
            print("Player wins!")
            gameState = "startMenu"  # Return to start menu
            playerScore, opponentScore = 0, 0  # Reset scores
        elif opponentScore >= winningScore:
            print("Opponent wins!")
            gameState = "startMenu"
            playerScore, opponentScore = 0, 0

        # Drawing game objects and scores
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, WHITE, playerPaddle)
        pygame.draw.rect(screen, WHITE, opponentPaddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        
        # Display scores
        playerText = font.render(str(playerScore), True, WHITE)
        opponentText = font.render(str(opponentScore), True, WHITE)
        screen.blit(playerText, (screenWidth / 4, 20))
        screen.blit(opponentText, (3 * screenWidth / 4, 20))

    pygame.display.flip() 
    clock.tick(60)

pygame.quit()  # Quit Pygame when the loop ends
