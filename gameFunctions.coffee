import pygame
# Draw the options menu
def drawOptionsMenu():
    global winningScore, gameState
    screen.blit(backGround, (0, 0))

    optionsFont = pygame.font.Font("assets/font.ttf", 65)
    optionsTitle = optionsFont.render('Options', True, WHITE)
    screen.blit(optionsTitle, (screenWidth / 2 - optionsTitle.get_width() / 2, screenHeight / 4 + 55))

    scoreText = font.render(f'Winning Score: {winningScore}', True, WHITE)
    screen.blit(scoreText, (screenWidth / 2 - scoreText.get_width() / 2, screenHeight / 2 + 10))

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