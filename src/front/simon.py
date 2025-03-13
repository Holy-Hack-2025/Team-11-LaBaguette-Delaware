import pygame
import sys

# Initialize Pygame
pygame.init()

# Load the image
image = pygame.image.load('foto_map.png')  # Replace with the path to your image
image_width, image_height = image.get_size()

crop_width = image_width//2
crop_height = image_height//2



# Get the screen's width and height
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h



# Set the initial window size
screen = pygame.display.set_mode((crop_width, crop_height))

# Set window title
pygame.display.set_caption("Resizable Pygame Window")


# Scale the image to half its original size
scaled_image = pygame.transform.scale(image, (image_width // 2, image_height // 2))

# Update the image_rect to the new dimensions of the scaled image
scaled_image_width, scaled_image_height = scaled_image.get_size()
print(scaled_image_width,scaled_image_height)
image_rect = scaled_image.get_rect()



# Define different lane colors
WHITE = (255, 255, 255)       # Standard lane color
YELLOW = (255, 255, 0)        # Special lane (e.g., bus lane)
RED = (255, 0, 0)             # Lane with stop signs
GREEN = (0, 255, 0)           # Lane for pedestrian crossings
BLUE = (0, 0, 255)            # Lane for emergency vehicles
DARK_GRAY = (169, 169, 169)   # Lane for toll booths or other purposes


lane_width = 3  # Width of the lane lines





# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Fill the screen with a color
    screen.fill((0, 0, 0))

    # Draw the image on the window
    screen.blit(scaled_image,image_rect)

    # Draw horizontal lanes
    pygame.draw.line(screen, BLUE, (0, crop_height // 3), (crop_width, crop_height // 3), lane_width)
    pygame.draw.line(screen, RED, (0, 2 * crop_height // 3), (crop_width, 2 * crop_height // 3), lane_width)

    # Draw vertical lanes (for example, dividing the screen into two sections)
    pygame.draw.line(screen, GREEN, (crop_width // 2, 0), (crop_width // 2, crop_height), lane_width)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
