import pygame
import sys

pygame.init()

# Load the background image and get its size
background_image = pygame.image.load("/Users/dlx/Desktop/Hackathon_2025/my_crossroad_map.png")
img_width, img_height = background_image.get_rect().size

# Create window using the image dimensions
screen = pygame.display.set_mode((img_width, img_height))
pygame.display.set_caption("Crossroad with Map Background")

# Example "red ball" properties
# Set the x-coordinate to the center of the vertical street (adjust this value as needed)
vertical_road_center = 400  # Modify based on your image layout
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

    # Move the car vertically by updating its y-coordinate only.
    car_pos[1] += car_speed

    # Reset to top if the car goes off the bottom of the screen.
    if car_pos[1] > img_height:
        car_pos[1] = -car_radius

    # Draw the background and the car.
    screen.blit(background_image, (0, 0))
    pygame.draw.circle(screen, car_color, car_pos, car_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
