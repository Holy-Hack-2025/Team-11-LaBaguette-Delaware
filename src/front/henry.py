import pygame
import sys

pygame.init()

# Load the background image and get its original dimensions.
background_image = pygame.image.load("./foto_map.png")
img_width, img_height = background_image.get_rect().size

# Crop 10% from the top and 10% from the bottom.
crop_top = int(img_height * 0.1)
crop_height = int(img_height * 0.8)
cropped_background_image = background_image.subsurface((0, crop_top, img_width, crop_height))

# Save the cropped image's original dimensions.
original_width = img_width
original_height = crop_height
aspect_ratio = original_width / original_height

# Create an initial resizable window using the cropped image's dimensions.
screen = pygame.display.set_mode((original_width, original_height), pygame.RESIZABLE)
pygame.display.set_caption("Crossroad with Map Background")

# Car properties in "original" coordinates (relative to the cropped image).
vertical_road_center = 400   # X coordinate in the cropped image
car_pos = [vertical_road_center, 100]  # Starting position in original coordinates
car_speed = 2                # Movement speed (per frame in original units)
car_color = (255, 0, 0)      # red color
car_radius = 10              # in original coordinates

# Scale factor starts at 1 (initial window equals original dimensions).
scale_factor = 1.0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # When the window is resized, adjust its dimensions to keep the aspect ratio.
            new_width, new_height = event.w, event.h
            # Adjust new_height based on the aspect ratio calculated from the original cropped image.
            new_height = int(new_width / aspect_ratio)
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            scale_factor = new_width / original_width

    # Update the car's vertical position (in original coordinates).
    car_pos[1] += car_speed
    if car_pos[1] > original_height:
        car_pos[1] = -car_radius

    # Scale the background image to the current window size.
    scaled_bg = pygame.transform.smoothscale(cropped_background_image,
                     (int(original_width * scale_factor), int(original_height * scale_factor)))
    
    # Clear the screen.
    screen.fill((0, 0, 0))
    # Blit the scaled background.
    screen.blit(scaled_bg, (0, 0))
    
    # Scale the car's position and radius based on the scale factor.
    scaled_car_pos = (int(car_pos[0] * scale_factor), int(car_pos[1] * scale_factor))
    scaled_car_radius = int(car_radius * scale_factor)
    pygame.draw.circle(screen, car_color, scaled_car_pos, scaled_car_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
