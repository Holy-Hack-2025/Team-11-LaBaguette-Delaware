import pygame
import sys
import constants
from TrafficLight import TrafficLight
from Car import Car

pygame.init()

# -------------------------------
# SETUP WINDOW AND BACKGROUND IMAGE
# -------------------------------
background_image = pygame.image.load("foto_map.png")
img_width, img_height = background_image.get_size()

# Use half the original image size for the simulation.
crop_width = img_width // 2
crop_height = img_height // 2

screen = pygame.display.set_mode((crop_width, crop_height), pygame.RESIZABLE)
pygame.display.set_caption("Green Lane Traffic Light Simulation")

scaled_background = pygame.transform.scale(background_image, (crop_width, crop_height))
bg_rect = scaled_background.get_rect()

# -------------------------------
# DEFINE A SIMPLE ROUTE CLASS FOR VERTICAL (GREEN) LANE
# -------------------------------
class Route:
    def __init__(self, length, x_position):
        self.length = length            # Vertical length of the lane (in pixels)
        self.x_position = x_position    # Fixed x-coordinate for the lane
        self.cars = []                  # List to hold Car objects on this route
        self.trafic_light = None        # TrafficLight object assigned to this route

# -------------------------------
# SETUP THE GREEN LANE ROUTE AND TRAFFIC LIGHT
# -------------------------------
# The green lane is a vertical line at x = crop_width//2, running from y=0 to y=crop_height.
green_lane_x = crop_width // 2
route_green = Route(length=crop_height, x_position=green_lane_x)

# Place the traffic light at one-quarter of the green lane (y = crop_height//4).
traffic_light = TrafficLight(
    route=route_green,
    position=(green_lane_x, crop_height // 4),
    initial_state="GREEN",
    ticks=constants.DEFAULT_TRAFFIC_LIGHT_DURATION * constants.TICKS_PER_SECOND
)
route_green.trafic_light = traffic_light

# -------------------------------
# CREATE A CAR ON THE GREEN LANE
# -------------------------------
# The Car class (from your imported Car.py) uses a scalar 'position' along the route.
# Here, position represents the vertical distance along the lane.
car_green = Car(route=route_green, reaction_time=30, is_driving=True, position=0)
route_green.cars.append(car_green)

# -------------------------------
# MAIN SIMULATION LOOP
# -------------------------------
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            new_width, new_height = event.w, event.h
            # Maintain the aspect ratio based on the cropped dimensions.
            new_height = int(new_width * (crop_height / crop_width))
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
    
    # Update the traffic light.
    traffic_light.ticks_since_last_change += 1
    if traffic_light.ticks_since_last_change >= traffic_light.ticks_between_changes:
        traffic_light.toggle_state()
    
    # Update the car (its update method will check for red light and obstacles).
    car_green.update()
    
    # -------------------------------
    # DRAWING
    # -------------------------------
    screen.fill((0, 0, 0))
    screen.blit(scaled_background, bg_rect)
    
    # Draw the green lane as a vertical line.
    pygame.draw.line(screen, (0, 255, 0), (green_lane_x, 0), (green_lane_x, crop_height), 3)
    
    # Draw the traffic light as a small circle (ball).
    light_color = (0, 255, 0) if traffic_light.state == "GREEN" else (255, 0, 0)
    pygame.draw.circle(screen, light_color, traffic_light.position, 8)
    
    # Draw the car as a red circle.
    car_radius = constants.CAR_LENGTH if hasattr(constants, "CAR_LENGTH") else 10
    # For a vertical lane, the car's x-coordinate is fixed; its 'position' represents the y-coordinate.
    pygame.draw.circle(screen, (255, 0, 0), (green_lane_x, int(car_green.position)), car_radius)
    
    pygame.display.flip()
    clock.tick(constants.TICKS_PER_SECOND)

pygame.quit()
sys.exit()
