import pygame
import random

# Draw options menu
def drawOptionsMenu(screen, backGround, font, WHITE, screenWidth, screenHeight, winningScore, buttons):
    optionsFont = pygame.font.Font("assets/font.ttf", 65)
    optionsTitle = optionsFont.render('Options', True, WHITE)
    screen.blit(backGround, (0, 0))
    screen.blit(optionsTitle, (screenWidth / 2 - optionsTitle.get_width() / 2, screenHeight / 4 + 55))
    # Display winning score
    scoreText = font.render(f'Winning Score: {winningScore}', True, WHITE)
    screen.blit(scoreText, (screenWidth / 2 - scoreText.get_width() / 2, screenHeight / 2 + 10))

    mousePos = pygame.mouse.get_pos()
    for button in buttons:  # Loop through the buttons and update them
        button.changeColor(mousePos)
        button.update(screen)

# Draw start menu
def drawStartMenu(screen, backGround, font, WHITE, screenWidth, screenHeight, startButton, optionsButton):
    screen.blit(backGround, (0, 0))
    font = pygame.font.Font("assets/font.ttf", 65)
    title = font.render('Pong Game', True, WHITE)
    screen.blit(title, (screenWidth/2 - title.get_width()/2, screenHeight/2 - title.get_height() - 60))
    # Draw buttons
    mousePos = pygame.mouse.get_pos()
    startButton.changeColor(mousePos)
    startButton.update(screen)
    optionsButton.changeColor(mousePos)
    optionsButton.update(screen)

# Reset ball
def ballRestart(ball, screenWidth, screenHeight, playerScore, opponentScore, winningScore):
    ball.center = (screenWidth / 2, screenHeight / 2)
    ballSpeedY = 7 * random.choice((1, -1)) 
    ballSpeedX = 7 * random.choice((1, -1)) 
    newBallMoving = True  # Start the ball
    # Score reset
    if playerScore >= winningScore or opponentScore >= winningScore:
        newBallMoving = False  # Stop the ball for game over or score reset

    return ballSpeedX, ballSpeedY, newBallMoving

