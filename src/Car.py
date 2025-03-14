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

# For this simulation, we use half the original image size.
crop_width = img_width // 2
crop_height = img_height // 2

screen = pygame.display.set_mode((crop_width, crop_height), pygame.RESIZABLE)
pygame.display.set_caption("Traffic Light and Car Simulation")

# Scale the background image to the cropped dimensions.
scaled_background = pygame.transform.scale(background_image, (crop_width, crop_height))
bg_rect = scaled_background.get_rect()

# -------------------------------
# DEFINE A SIMPLE ROUTE CLASS
# -------------------------------
class Route:
    def __init__(self, length, y_position):
        self.length = length            # Horizontal length of the route (in pixels)
        self.y_position = y_position    # Fixed y-coordinate for this lane
        self.cars = []                  # List of Car objects on this route
        self.trafic_light = None        # The TrafficLight object for this route

# -------------------------------
# SETUP THE BLUE LANE ROUTE AND TRAFFIC LIGHT
# -------------------------------
# Define a blue horizontal lane at 1/3 of the cropped height.
blue_lane_y = crop_height // 3
route_blue = Route(length=crop_width, y_position=blue_lane_y)

# Create a TrafficLight at the center of the blue lane.
# It will change every 10 seconds: ticks = 10 * TICKS_PER_SECOND.
traffic_light = TrafficLight(
    route=route_blue,
    position=(crop_width // 2, blue_lane_y),
    initial_state="GREEN",
    ticks=constants.DEFAULT_TRAFFIC_LIGHT_DURATION * constants.TICKS_PER_SECOND
)
route_blue.trafic_light = traffic_light

# -------------------------------
# CREATE CARS ON THE BLUE LANE
# -------------------------------
# Create two Car instances along the blue lane.
# The Car constructor takes: (route, reaction_time, is_driving, position).
car1 = Car(route=route_blue, reaction_time=30, is_driving=True, position=0)
car2 = Car(route=route_blue, reaction_time=30, is_driving=True, position=-50)  # Starts slightly behind

# Add the cars to the route (so they can check for obstacles via route.cars).
route_blue.cars.append(car1)
route_blue.cars.append(car2)

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
            # Maintain the original aspect ratio (crop_width : crop_height)
            new_height = int(new_width * (crop_height / crop_width))
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
    
    # Update the traffic light.
    traffic_light.ticks_since_last_change += 1
    if traffic_light.ticks_since_last_change >= traffic_light.ticks_between_changes:
        traffic_light.toggle_state()
    
    # Update the cars.
    car1.update()
    car2.update()
    
    # -------------------------------
    # DRAWING
    # -------------------------------
    screen.fill((0, 0, 0))
    screen.blit(scaled_background, bg_rect)
    
    # Draw the blue lane as a horizontal line.
    pygame.draw.line(screen, (0, 0, 255), (0, blue_lane_y), (crop_width, blue_lane_y), 3)
    
    # Draw the traffic light as a circle.
    # It is green when its state is "GREEN", red otherwise.
    light_color = (0, 255, 0) if traffic_light.state == "GREEN" else (255, 0, 0)
    pygame.draw.circle(screen, light_color, traffic_light.position, 8)
    
    # Draw the cars as circles.
    # Use constants.CAR_LENGTH for the radius if defined, otherwise use 10.
    car_radius = constants.CAR_LENGTH if hasattr(constants, "CAR_LENGTH") else 10
    pygame.draw.circle(screen, (255, 0, 0), (int(car1.position), blue_lane_y), car_radius)
    pygame.draw.circle(screen, (255, 0, 0), (int(car2.position), blue_lane_y), car_radius)
    
    pygame.display.flip()
    clock.tick(constants.TICKS_PER_SECOND)

pygame.quit()
sys.exit()
