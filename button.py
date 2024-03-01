import pygame
class Button():
   
    # Constructor
    def __init__(self, image, pos, textInput, font, baseColor, hoveringColor):
        
        # Initialize button properties
        self.image = image  # Image of the button, can be None
        self.x_pos = pos[0]  # X position of the button
        self.y_pos = pos[1]  # Y position of the button
        self.font = font  # Font used for the button's text
        self.baseColor, self.hoveringColor = baseColor, hoveringColor  # Colors for normal and hover states
        self.textInput = textInput  # Text displayed on the button
        
        # Render the text with the base color
        self.text = self.font.render(self.textInput, True, self.baseColor)
        
        # If no image is provided, use the rendered text as the button image
        if self.image is None:
            self.image = self.text
        
        # Create a rect for positioning the button, centered at the provided position
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        # Create a rect for positioning the text, centered at the same position
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Method to display the button on the screen
    def update(self, screen):
        # If image exists, blit it to the screen at the button's rect
        if self.image is not None:
            screen.blit(self.image, self.rect)
        # Blit text to the screen at the text's rect
        screen.blit(self.text, self.text_rect)

    # Method to check if mouse is over the button
    def checkForInput(self, position):
        # Check if mouse position is within the button's rect
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True  # Mouse is over the button
        return False  # Mouse is not over the button

    # Method to change the button's text color based on mouse position
    def changeColor(self, position):
        # Check if mouse position is within the button's rect
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            # Change text color to the hovering color
            self.text = self.font.render(self.textInput, True, self.hoveringColor)
        else:
            # Change text color back to the base color
            self.text = self.font.render(self.textInput, True, self.baseColor)

# Function to initialize and return buttons
def initButton(screen_width, screen_height, font, base_color, hovering_color):

    # Font for the buttons
    fontButton = pygame.font.Font("assets/font.ttf", 28)
    
    # Button setup for the start button
    startButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screen_width / 2, screen_height / 2 + 40),
                          textInput="START", font=fontButton, baseColor=base_color, hoveringColor=hovering_color)

    # Button setup for options button
    optionsButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screen_width / 2, screen_height / 2 + 130),
                            textInput="OPTIONS", font=fontButton, baseColor=base_color, hoveringColor=hovering_color)

    # Increase and decrease buttons for winning score and back button for the options menu
    increaseScoreButton = Button(image=None, pos=(screen_width / 2 + 100, screen_height / 2 + 115),
                                 textInput="+", font=font, baseColor=base_color, hoveringColor=hovering_color)
    decreaseScoreButton = Button(image=None, pos=(screen_width / 2 - 100, screen_height / 2 + 115),
                                 textInput="-", font=font, baseColor=base_color, hoveringColor=hovering_color)
    backButton = Button(image=None, pos=(screen_width / 2, screen_height / 2 + 200),
                        textInput="BACK", font=fontButton, baseColor=base_color, hoveringColor=hovering_color)

    return startButton, optionsButton, increaseScoreButton, decreaseScoreButton, backButton

# # Button setup for the start button
# startButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screenWidth / 2, screenHeight / 2 + 40),
#                       textInput="START", font=pygame.font.Font("assets/font.ttf", 28), baseColor=WHITE, hoveringColor=(100, 100, 100))

# # Button setup for options button
# optionsButton = Button(image=pygame.image.load("assets/playRect2.png"), pos=(screenWidth / 2, screenHeight / 2 + 130),
#                         textInput="OPTIONS", font=pygame.font.Font("assets/font.ttf", 28), baseColor=WHITE, hoveringColor=(100, 100, 100))

# # Increase and decrease buttons for winning score and back button for the options menu
# increaseScoreButton = Button(image=None, pos=(screenWidth / 2 + 100, screenHeight / 2 + 115),
#                              textInput="+", font=pygame.font.Font("assets/font.ttf", 36), baseColor=WHITE, hoveringColor=(100, 100, 100))
# decreaseScoreButton = Button(image=None, pos=(screenWidth / 2 - 100, screenHeight / 2 + 115),
#                              textInput="-", font=pygame.font.Font("assets/font.ttf", 36), baseColor=WHITE, hoveringColor=(100, 100, 100))
# backButton = Button(image=None, pos=(screenWidth / 2, screenHeight / 2 + 200),
#                     textInput="BACK", font=pygame.font.Font("assets/font.ttf", 28), baseColor=WHITE, hoveringColor=(100, 100, 100))
