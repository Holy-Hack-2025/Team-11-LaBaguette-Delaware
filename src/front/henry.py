import pygame
import sys

pygame.init()

# Load the background image and get its original dimensions.
background_image = pygame.image.load("./foto_map.png")
img_width, img_height = background_image.get_rect().size

# Calculate the cropping values: remove 10% from the top and bottom.
crop_top = int(img_height * 0.1)
crop_height = int(img_height * 0.8)

# Crop the image using subsurface.
cropped_background_image = background_image.subsurface((0, crop_top, img_width, crop_height))

# Create a window using the dimensions of the cropped image.
screen = pygame.display.set_mode((img_width, crop_height))
pygame.display.set_caption("Crossroad with Map Background")

# Example "red ball" properties.
# Set the x-coordinate to the center of the vertical street (adjust as needed).
vertical_road_center = 400  # Modify based on your image layout
# Note: The car's y-coordinate is now relative to the cropped image.
car_pos = [vertical_road_center, 100]
car_speed = 2
car_color = (255, 0, 0)  # red circle
car_radius = 10

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the car vertically.
    car_pos[1] += car_speed

    # Reset to top if the car goes off the bottom of the cropped area.
    if car_pos[1] > crop_height:
        car_pos[1] = -car_radius

    # Draw the cropped background and the car.
    screen.blit(cropped_background_image, (0, 0))
    pygame.draw.circle(screen, car_color, car_pos, car_radius)

    pygame.display.flip()
    clock.tick(600)

pygame.quit()
sys.exit()
