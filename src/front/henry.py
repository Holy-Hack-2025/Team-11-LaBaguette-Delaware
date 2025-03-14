import pygame
import sys
import math

# -------------------------------
# CONSTANTS (simulate constants.py)
# -------------------------------
class constants:
    DEFAULT_TRAFFIC_LIGHT_DURATION = 10   # seconds (default cycle duration)
    TICKS_PER_SECOND = 60                 # frames per second
    CAR_SPEED = 20                        # pixels per tick
    CAR_LENGTH = 10                       # for drawing and distance calculations

# -------------------------------
# TRAFFIC LIGHT CLASS (simulate TrafficLight.py)
# -------------------------------
class TrafficLight:
    def __init__(self, route, position, initial_state="RED", ticks=15 * constants.TICKS_PER_SECOND):
        """
        Initiates a traffic light.
        route: a Route object the light is on.
        position: (x, y) position on the route.
        initial_state: "GREEN" or "RED" (here we start with RED for 15 seconds).
        ticks: number of ticks between state changes.
        """
        self.route = route
        self.position = position
        self.state = initial_state  # start as RED
        self.ticks_since_last_change = 0
        self.ticks_between_changes = ticks  # 15 seconds initial red duration

    def get_position(self):
        return self.position

    def update(self):
        if self.ticks_since_last_change >= self.ticks_between_changes:
            self.toggle_state()

    def toggle_state(self):
        if self.state == "GREEN":
            self.state = "RED"
            # After green, use the default duration (10 seconds) for red
            self.ticks_between_changes = constants.DEFAULT_TRAFFIC_LIGHT_DURATION * constants.TICKS_PER_SECOND
        else:
            self.state = "GREEN"
            # After red, use the default duration (10 seconds) for green
            self.ticks_between_changes = constants.DEFAULT_TRAFFIC_LIGHT_DURATION * constants.TICKS_PER_SECOND
        self.ticks_since_last_change = 0

# -------------------------------
# CAR CLASS (simulate Car.py)
# -------------------------------
class Car:
    def __init__(self, route, reaction_time, is_driving=True, position=0):
        """
        Initiates a car.
        route: a Route object.
        reaction_time: (unused in this version) originally the number of ticks the car waits to restart after stopping.
        is_driving: whether the car is currently moving.
        position: the car's starting position along the route (vertical position).
        """
        self.route = route
        self.position = position
        self.reaction_time = reaction_time
        self.is_driving = is_driving
        self.reaction_time_countdown = 0
        self.is_done_driving = False

    def update(self):
        # Check if the car should stop due to a red light or a stopped car in front.
        if self.red_light_ahead() or self.stopped_car_in_front():
            self.is_driving = False
        else:
            # As soon as conditions allow (e.g. light is green), resume driving.
            self.is_driving = True

        if self.is_driving:
            if self.position + constants.CAR_SPEED > self.route.length:
                self.is_done_driving = True
            else:
                self.position += constants.CAR_SPEED

    def red_light_ahead(self):
        """
        Check if the car is approaching the traffic light.
        For a vertical lane, if the car hasn't passed the light (position less than light's y)
        and the distance is within a threshold (1.5 * CAR_LENGTH), and the light is red,
        then return True.
        """
        tl_y = self.route.trafic_light.position[1]
        if self.position < tl_y and (tl_y - self.position) <= 1.5 * constants.CAR_LENGTH:
            if self.route.trafic_light.state == "RED":
                return True
        return False

    def stopped_car_in_front(self):
        # Check if any other car on the route (besides self) is too close and stopped.
        for car in self.route.cars:
            if car is not self:
                if car.position <= self.position + 1.5 * constants.CAR_LENGTH:
                    if not car.is_driving:
                        return True
        return False

# -------------------------------
# ROUTE CLASS
# -------------------------------
class Route:
    def __init__(self, length, x_position):
        """
        length: vertical length of the lane (in pixels).
        x_position: fixed x-coordinate for the lane.
        """
        self.length = length
        self.x_position = x_position
        self.cars = []           # List of Car objects on this route.
        self.trafic_light = None # The TrafficLight assigned to this route.

# -------------------------------
# MAIN SIMULATION SETUP
# -------------------------------
pygame.init()

# Load the background image.
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
# SETUP THE GREEN LANE AND ITS TRAFFIC LIGHT
# -------------------------------
# For a vertical lane, fix the x-coordinate.
green_lane_x = crop_width // 2
route_green = Route(length=crop_height, x_position=green_lane_x)

# Place the traffic light in the center of the lane.
traffic_light = TrafficLight(
    route=route_green,
    position=(green_lane_x + 10, crop_height // 2),  # center of the lane
    initial_state="RED",                        # start as red
    ticks=10 * constants.TICKS_PER_SECOND         # 15 seconds initial red duration
)
route_green.trafic_light = traffic_light

# -------------------------------
# CREATE INITIAL CAR ON THE GREEN LANE
# -------------------------------
# The car's position represents its vertical position along the lane.
car_spawn = Car(route=route_green, reaction_time=30, is_driving=True, position=0)
route_green.cars.append(car_spawn)

# We'll also spawn a new car every 10 seconds.
car_spawn_timer = 600  # counts ticks

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
            new_height = int(new_width * (crop_height / crop_width))
            screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    # Update the traffic light.
    traffic_light.ticks_since_last_change += 1
    if traffic_light.ticks_since_last_change >= traffic_light.ticks_between_changes:
        traffic_light.toggle_state()

    # Update all cars on the lane.
    for car in route_green.cars:
        car.update()

    # Spawn a new car every 10 seconds.
    car_spawn_timer += 1
    if car_spawn_timer >= 10 * constants.TICKS_PER_SECOND:
        new_car = Car(route=route_green, reaction_time=30, is_driving=True, position=0)
        route_green.cars.append(new_car)
        car_spawn_timer = 0

    # -------------------------------
    # DRAWING
    # -------------------------------
    screen.fill((0, 0, 0))
    screen.blit(scaled_background, bg_rect)

    # Draw the green lane as a vertical line.
    pygame.draw.line(screen, (0, 255, 0), (green_lane_x, 0), (green_lane_x, crop_height), 3)

    # Draw the traffic light as a circle.
    light_color = (0, 255, 0) if traffic_light.state == "GREEN" else (255, 0, 0)
    pygame.draw.circle(screen, light_color, traffic_light.position, 8)

    # Draw all cars as circles.
    for car in route_green.cars:
        pygame.draw.circle(screen, (255, 0, 0), (green_lane_x, int(car.position)), constants.CAR_LENGTH)

    pygame.display.flip()
    clock.tick(constants.TICKS_PER_SECOND)

pygame.quit()
sys.exit()
