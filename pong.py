import pygame
import random
from button import Button

# Initialize Pygame
pygame.init()

# Game states variables
gameState = "startMenu"  # Tracks current game status (Start menu, main game, game over)
running = True  # Main game loop
ballMoving = False  # Flag to check if the ball is moving
winningScore = 5  # Initialize winning score
font = pygame.font.Font("assets/font.ttf", 36)
clock = pygame.time.Clock()  # Initialize Pygame clock

# Screen setup
screenWidth = 1280
screenHeight = 720
WHITE = (255, 255, 255)  # RGB color for white

screen = pygame.display.set_mode((screenWidth, screenHeight))  # Initialize display window

# Load assets
backGround = pygame.image.load("assets/background.png")  # Load background image

# Button setup for the start button
startButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screenWidth / 2, screenHeight / 2 + 40),
                      textInput="START", font=pygame.font.Font("assets/font.ttf", 28), baseColor=WHITE, hoveringColor=(100, 100, 100))

# Button setup for options button
optionsButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screenWidth / 2, screenHeight / 2 + 130),
                        textInput="OPTIONS", font=pygame.font.Font("assets/font.ttf", 28), baseColor=WHITE, hoveringColor=(100, 100, 100))

# Increase and decrease buttons for winning score and back button for the options menu
increaseScoreButton = Button(image=None, pos=(screenWidth / 2 + 100, screenHeight / 2),
                             textInput="+", font=pygame.font.Font("assets/font.ttf", 36), baseColor=WHITE, hoveringColor=(100, 100, 100))
decreaseScoreButton = Button(image=None, pos=(screenWidth / 2 - 100, screenHeight / 2),
                             textInput="-", font=pygame.font.Font("assets/font.ttf", 36), baseColor=WHITE, hoveringColor=(100, 100, 100))
backButton = Button(image=None, pos=(screenWidth / 2, screenHeight / 2 + 200),
                    textInput="BACK", font=pygame.font.Font("assets/font.ttf", 28), baseColor=WHITE, hoveringColor=(100, 100, 100))

# Paddle and Ball dimensions
paddleWidth = 15
paddleHeight = 100
ballSize = 25

# Rectangles for game objects
playerPaddle = pygame.Rect(50, (screenHeight - paddleHeight) / 2, paddleWidth, paddleHeight)
opponentPaddle = pygame.Rect(screenWidth - 50 - paddleWidth, (screenHeight - paddleHeight) / 2, paddleWidth, paddleHeight)
ball = pygame.Rect(screenWidth / 2 - ballSize / 2, screenHeight / 2 - ballSize / 2, ballSize, ballSize)

# Movement speeds
ballSpeedX = 7  # Initial horizontal speed of the ball
ballSpeedY = 7  # Initial vertical speed of the ball
playerSpeedIncrement = 10  # Speed increment for player's paddle
opponentSpeed = 5  # Speed of opponent's paddle

# Scoring
playerScore = 0  # Player's score
opponentScore = 0  # Opponent's score

def drawOptionsMenu():
    global winningScore, gameState
    screen.blit(backGround, (0, 0))

    optionsFont = pygame.font.Font("assets/font.ttf", 65)
    optionsTitle = optionsFont.render('Options', True, WHITE)
    screen.blit(optionsTitle, (screenWidth / 2 - optionsTitle.get_width() / 2, screenHeight / 4))

    scoreText = font.render(f'Winning Score: {winningScore}', True, WHITE)
    screen.blit(scoreText, (screenWidth / 2 - scoreText.get_width() / 2, screenHeight / 2 - 50))

    mousePos = pygame.mouse.get_pos()
    for button in [increaseScoreButton, decreaseScoreButton, backButton]:
        button.changeColor(mousePos)
        button.update(screen)

def drawStartMenu():
    global gameState
    screen.blit(backGround, (0, 0))

    font = pygame.font.Font("assets/font.ttf", 65)
    title = font.render('Pong Game', True, WHITE)
    screen.blit(title, (screenWidth/2 - title.get_width()/2, screenHeight/2 - title.get_height() - 60))

    mousePos = pygame.mouse.get_pos()
    startButton.changeColor(mousePos)
    startButton.update(screen)
    optionsButton.changeColor(mousePos)
    optionsButton.update(screen)

def ballRestart():
    global ballSpeedX, ballSpeedY, ballMoving, playerScore, opponentScore, gameState
    ball.center = (screenWidth / 2, screenHeight / 2)  # Center the ball
    ballSpeedY = 7 * random.choice((1, -1))  # Randomize vertical direction
    ballSpeedX = 7 * random.choice((1, -1))  # Randomize horizontal direction
    ballMoving = True  # Start moving the ball

    # Check for winning score
    if playerScore >= winningScore:
        print("Player wins!")
        gameState = "startMenu"
    elif opponentScore >= winningScore:
        print("Opponent wins!")
        gameState = "startMenu"

def gameRestart():
    global playerScore, opponentScore, gameState, ballMoving
    playerScore = 0
    opponentScore = 0
    gameState = "startMenu"
    ballMoving = False

# Main game loop
while running:
    mousePos = pygame.mouse.get_pos()
    events = pygame.event.get()  # Retrieve all events once and use this list for processing
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if gameState == "startMenu":
            drawStartMenu()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startButton.checkForInput(mousePos):
                        gameState = "mainGame"
                        ballMoving = True  # Ball should move when the game starts
                        playerScore = 0
                        opponentScore = 0
                    elif optionsButton.checkForInput(mousePos):
                        gameState = "optionsMenu"
        
        elif gameState == "optionsMenu":
            drawOptionsMenu()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if increaseScoreButton.checkForInput(mousePos):
                        winningScore += 1  # Adjust winning score
                    elif decreaseScoreButton.checkForInput(mousePos) and winningScore > 1:
                        winningScore -= 1  # Adjust winning score
                    elif backButton.checkForInput(mousePos):
                        gameState = "startMenu"

    if gameState == "mainGame":
        # Paddle Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            playerPaddle.y -= playerSpeedIncrement
        if keys[pygame.K_DOWN]:
            playerPaddle.y += playerSpeedIncrement

        # Keep paddles within screen bounds
        playerPaddle.clamp_ip(screen.get_rect())
        opponentPaddle.clamp_ip(screen.get_rect())

        # Opponent AI follows the ball
        if ballMoving:
            if opponentPaddle.centery < ball.centery:
                opponentPaddle.y += opponentSpeed
            elif opponentPaddle.centery > ball.centery:
                opponentPaddle.y -= opponentSpeed

        # Ball Movement
        if ballMoving:
            ball.x += ballSpeedX
            ball.y += ballSpeedY

            # Wall Collision
            if ball.top <= 0 or ball.bottom >= screenHeight:
                ballSpeedY = -ballSpeedY

            # Paddle Collision
            if ball.colliderect(playerPaddle) or ball.colliderect(opponentPaddle):
                ballSpeedX = -ballSpeedX

            # Score Update & Ball Reset
            if ball.right >= screenWidth:
                playerScore += 1
                ballRestart()
            elif ball.left <= 0:
                opponentScore += 1
                ballRestart()

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
