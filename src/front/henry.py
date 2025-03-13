import pygame
import sys
import math
#from constants.py import CAR_SPEED

pygame.init()

# Load the background image and get its original dimensions.
background_image = pygame.image.load("./foto_map.png")
img_width, img_height = background_image.get_rect().size

# Save the image's original dimensions.
original_width = img_width
original_height = int(img_height)
aspect_ratio = original_width / original_height

# Create an initial resizable window using the image's dimensions.
screen = pygame.display.set_mode((original_width, original_height), pygame.RESIZABLE)
pygame.display.set_caption("Crossroad with Map Background")

# Car properties in "original" coordinates.
car_speed = 20              # Movement speed (per frame in original units)
car_color = (255, 0, 0)      # Red color
car_radius = 10              # Radius in original coordinates

# Define a Car class that follows a predefined road and stops in the center.
class Car:
    def __init__(self, road, speed=2):
        self.road = road              # List of (x, y) tuples in original coordinates.
        self.speed = speed
        self.pos = list(road[0])      # Start at the first waypoint.
        self.current_index = 1        # Next waypoint index.
        self.stopped = False          # Flag to indicate if the car is currently stopped.
        self.stop_timer = 0           # Count frames during stop

    def update(self):
        # For a horizontal route, the center is halfway between the start and end x.
        center_x = (self.road[0][0] + self.road[-1][0]) / 2

        # If not already stopped, check if we are at (or near) the center.
        if not self.stopped and abs(self.pos[0] - center_x) < self.speed:
            self.stopped = True
            self.stop_timer = 0

        # If stopped, increment stop timer and resume after ~3 seconds (180 frames).
        if self.stopped:
            self.stop_timer += 1
            if self.stop_timer >= 180:
                # Nudge the car forward so it leaves the center zone.
                self.pos[0] += self.speed
                self.stopped = False
                self.stop_timer = 0
            return  # Do not update further while stopped

        # If there are still waypoints to follow, move toward the next one.
        if self.current_index < len(self.road):
            target = self.road[self.current_index]
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
            distance = math.hypot(dx, dy)
            if distance < self.speed:
                # Snap to the waypoint and advance to the next one.
                self.pos = list(target)
                self.current_index += 1
            else:
                self.pos[0] += (dx / distance) * self.speed
                self.pos[1] += (dy / distance) * self.speed
        else:
            # Loop back to the start.
            self.current_index = 0
            self.pos = list(self.road[0])

    def draw(self, surface, scale_factor, radius, color):
        # Scale position and radius before drawing.
        scaled_pos = (int(self.pos[0] * scale_factor), int(self.pos[1] * scale_factor))
        scaled_radius = int(radius * scale_factor)
        pygame.draw.circle(surface, color, scaled_pos, scaled_radius)

# Define a horizontal road as a list of waypoints (in original coordinates).
# For a horizontal route, we use a fixed y (for example, in the middle of the screen).
fixed_y = original_height // 2
road_waypoints = [
    (0, fixed_y),
    (original_width, fixed_y)
]

# Create a Car instance that follows the horizontal road.
car = Car(road=road_waypoints, speed=car_speed)

# Initial scale factor (window equals original dimensions at start).
scale_factor = 1.0

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Adjust window dimensions to maintain the aspect ratio.
            new_width, new_height = event.w, event.h
            new_height = int(new_width / aspect_ratio)
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            scale_factor = new_width / original_width

    # Update the car's position along its road.
    car.update()

    # Scale the background image to the current window size.
    scaled_bg = pygame.transform.smoothscale(background_image,
                     (int(original_width * scale_factor), int(original_height * scale_factor)))

    # Draw the scaled background and the car.
    screen.fill((0, 0, 0))
    screen.blit(scaled_bg, (0, 0))
    car.draw(screen, scale_factor, car_radius, car_color)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

