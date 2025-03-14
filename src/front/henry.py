import pygame
import sys
import json
import math

# Initialize Pygame
pygame.init()

# Load the image
image = pygame.image.load('foto_map.png')  # Replace with the path to your image
image_width, image_height = image.get_size()

crop_width = image_width // 2
crop_height = image_height // 2

# Get the screen's width and height (not used further but available if needed)
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Set the initial window size
screen = pygame.display.set_mode((crop_width, crop_height), pygame.RESIZABLE)

# Set window title
pygame.display.set_caption("Resizable Pygame Window")

# Scale the image to half its original size
scaled_image = pygame.transform.scale(image, (crop_width, crop_height))
image_rect = scaled_image.get_rect()

# Define different lane colors
WHITE = (255, 255, 255)       # Standard lane color
YELLOW = (255, 255, 0)        # Special lane (e.g., bus lane)
RED = (255, 0, 0)             # Lane with stop signs
GREEN = (0, 255, 0)           # Lane for pedestrian crossings
BLUE = (0, 0, 255)            # Lane for emergency vehicles
DARK_GRAY = (169, 169, 169)   # Lane for toll booths or other purposes

lane_width = 3  # Width of the lane lines

# Load the path data from the JSON file (if needed for further processing)
with open('path_data.json', 'r') as f:
    path_data = json.load(f)

# Draw the path from JSON (if desired)
def draw_path(path_data):
    for segment in path_data:
        start = segment['start']
        end = segment['end']
        pygame.draw.line(screen, (255, 0, 0), (start['x'], start['y']), (end['x'], end['y']), 2)

# Define a Car class that follows a given route (list of waypoints)
class Car:
    def __init__(self, route, speed=5):
        """
        route: list of (x, y) tuples in the scaled (window) coordinates.
        speed: movement speed (pixels per frame).
        """
        self.route = route
        self.speed = speed
        self.pos = list(route[0])
        self.current_index = 1

    def update(self):
        if self.current_index < len(self.route):
            target = self.route[self.current_index]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            distance = math.hypot(dx, dy)
            if distance < self.speed:
                self.pos = list(target)
                self.current_index += 1
            else:
                self.pos[0] += (dx / distance) * self.speed
                self.pos[1] += (dy / distance) * self.speed
        else:
            # Loop back to start.
            self.current_index = 0
            self.pos = list(self.route[0])

    def draw(self, surface):
        # Draw a larger circle (bigger ball) representing the car.
        pygame.draw.circle(surface, RED, (int(self.pos[0]), int(self.pos[1])), 10)

# --- Define routes based on the drawn lanes ---
# These lanes are drawn on the scaled image (size = crop_width x crop_height)

# Blue horizontal lane: at one-third of the cropped height
blue_lane_y = crop_height // 3
route_blue = [(0, blue_lane_y), (crop_width, blue_lane_y)]

# Red horizontal lane: at two-thirds of the cropped height
red_lane_y = (2 * crop_height) // 3
route_red = [(0, red_lane_y), (crop_width, red_lane_y)]

# Green vertical lane: at half of the cropped width
green_lane_x = crop_width // 2
route_green = [(green_lane_x, 0), (green_lane_x, crop_height)]

# Create one Car instance per lane (one big ball per route)
cars = [
    Car(route_blue, speed=5),
    Car(route_red, speed=5),
    Car(route_green, speed=5)
]

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            new_width, new_height = event.w, event.h
            new_height = int(new_width * (crop_height / crop_width))
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            # We work in scaled coordinates (crop_width x crop_height), so we don't recalc routes here.
    
    screen.fill((0, 0, 0))
    screen.blit(scaled_image, image_rect)
    
    # Draw the lane lines.
    pygame.draw.line(screen, BLUE, (0, crop_height // 3), (crop_width, crop_height // 3), lane_width)
    pygame.draw.line(screen, RED, (0, (2 * crop_height) // 3), (crop_width, (2 * crop_height) // 3), lane_width)
    pygame.draw.line(screen, GREEN, (crop_width // 2, 0), (crop_width // 2, crop_height), lane_width)
    
    # Optionally, draw the JSON path.
    # draw_path(path_data)
    
    # Update and draw each car.
    for car in cars:
        car.update()
        car.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()