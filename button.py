import pygame
class Button():
   
    # Constructor
    def __init__(self, image, pos, textInput, font, baseColor, hoveringColor):
        
        # Initialize button properties
        self.image = image  # Image of the button
        self.x_pos = pos[0]  
        self.y_pos = pos[1]  
        self.font = font  
        self.baseColor, self.hoveringColor = baseColor, hoveringColor  # Colors for normal and hover states
        self.textInput = textInput  
        
        # Render text 
        self.text = self.font.render(self.textInput, True, self.baseColor)
        
        # If no image provided use text as button image
        if self.image is None:
            self.image = self.text
        
        # Create rect to position the image centered at the provided position
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        # Create rect to position the text centered at the same position
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Method to display the button on the screen
    def update(self, screen):
        if self.image is not None:  # If image exists blit it to screen at the button rect
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Method to check if mouse is over the button
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True  
        return False  

    # Method to change the button text color based on mouse position
    def changeColor(self, position):
        # Check if mouse position is within the button's rect
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.textInput, True, self.hoveringColor) # Change text color to the hovering color
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)

# Function to initialize and return buttons
def initButton(screen_width, screen_height, font, base_color, hovering_color):

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

