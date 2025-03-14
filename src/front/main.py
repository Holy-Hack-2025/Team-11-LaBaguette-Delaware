import pygame
import sys
import json

import random


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
BLACK = (0, 0, 0)  # Standard black color
ROSE_FUCHSIA = (255, 0, 127)  # A vibrant pinkish-purple color

lane_width = 3  # Width of the lane lines


# Load the path data from the JSON file
with open('path_data.json', 'r') as f: # à refaire !!
    path1_data = json.load(f)

with open('path3.json', 'r') as f: 
    path3_data = json.load(f)

with open('path2.json', 'r') as f:
    path2_data = json.load(f)

with open('path4.json', 'r') as f:
    path4_data = json.load(f)


with open('path5.json', 'r') as f:
    path5_data = json.load(f)
with open('path6.json', 'r') as f:
    path6_data = json.load(f)

with open('light_c.json', 'r') as f:
    light_c = json.load(f)

with open('light_ab.json', 'r') as f:
    light_ab = json.load(f)

with open('light_d.json', 'r') as f:
    light_d = json.load(f)

# Define a function to draw the path
def draw_path(path_data,color):
    for segment in path_data:
        start = segment['start']
        end = segment['end']
        pygame.draw.line(screen, color, (start['x'], start['y']), (end['x'], end['y']), 2)


# Main loop
running = True

import math

class Car:
    def __init__(self, path_data,position, traffic_light, color=(255, 255, 255), speed=2):
        self.path_data = path_data
        self.traffic_light = traffic_light  # Only one traffic light to check
        self.color = color
        self.speed = speed
        self.position = position
        self.current_index = 0 # Index of the current segment
        self.progress = 0  # Progress along the current segment (0 to 1)
        self.x, self.y = self.path_data[0]['start']['x'], self.path_data[0]['start']['y']
        self.is_stopped = False  # Flag to check if the car is stopped by a red light
        self.is_dead = False
        self.distance_between = 25

    def distance_to_traffic_light(self):
        """Calculate the distance between the car and the traffic light."""
        dx = self.x - self.traffic_light.inner_x
        dy = self.y - self.traffic_light.inner_y
        return math.sqrt(dx**2 + dy**2)

    def check_traffic_light_ahead(self):
        """Check if the car is within a distance of x from the red traffic light."""
        # Calculate the distance from the car to the traffic light
        distance = self.distance_to_traffic_light()

        # If the car is within the specified distance x and the traffic light is red
        if distance <= 25:
            self.is_stopped = True
            return True
        
        self.is_stopped = False
        return False
    
    def check_other_cars_in_front(self, other_cars):
        """Check if there are any cars ahead within a max distance."""
        pos = self.position - 1
        if pos >= 0:
            car = other_cars[pos]
            if car != self and not car.is_dead:  # Don't check the car itself
                # Calculate the distance to the other car
                dx = car.x - self.x
                dy = car.y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                # If the car is in front and within the max_distance, stop the car
                if distance <= self.distance_between:
                    return True

        self.is_stopped = False
        return False
    
    # def is_in_front_of(self, other_car):
    #     """Check if this car is ahead of the other car based on their current positions."""
    #     # This check assumes that cars move along a linear path.
    #     # For a more complex path, this logic should account for direction.
    #     print("OK")
    #     return self.position < other_car.position

    def update_position(self, other_cars):
        """Move the car along the path. Stop at red lights."""
        if self.current_index >= len(self.path_data):
            self.is_dead = True  # Mark car as "dead" when it reaches the end
            return  # Stop moving if we reach the end or the car is stopped at a red light


        # Check if there are other cars ahead and stop if needed
        if self.check_other_cars_in_front(other_cars):
            return  # The car will stop if another car is within max_distance
        
        # Check if the car is approaching a red light and stop ahead of time
        if not self.traffic_light.is_green():
            if self.check_traffic_light_ahead():
                return  # The car will stop if there is a red light ahead

        segment = self.path_data[self.current_index]
        start = segment['start']
        end = segment['end']

        # Compute direction vector
        dx = end['x'] - start['x']
        dy = end['y'] - start['y']
        segment_length = math.sqrt(dx**2 + dy**2)

        # Normalize direction
        if segment_length != 0:
            dx /= segment_length
            dy /= segment_length

        # Move along the segment
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.progress += self.speed / segment_length

        # If we reach the end of the segment, move to the next one
        if self.progress >= 1:
            self.current_index += 1
            self.progress = 0

            # If not at the last segment, snap to the next start position
            if self.current_index < len(self.path_data):
                self.x, self.y = self.path_data[self.current_index]['start']['x'], self.path_data[self.current_index]['start']['y']

    def draw(self, screen):
        """Draw the car as a small circle or rectangle."""
        if not self.is_dead:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)


class TrafficLight:
    def __init__(self, path_data, green_duration=5, red_duration=5, delay=0):
        self.path_data = path_data
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.delay = delay
        self.delay_on = True
        self.timer = 0  # Timer to track time spent in the current state

        # Determine initial state based on delay
        self.state = 'red' if delay > 0 else 'green'

        # Get the position of the traffic light at the end of the path
        self.inner_x, self.inner_y = self.path_data[-1]['start']['x'], self.path_data[-1]['start']['y']
        self.x, self.y = self.path_data[-1]['end']['x'], self.path_data[-1]['end']['y']

    def update(self, delta_time):
        """Update the traffic light's state based on elapsed time."""
        self.timer += delta_time

        # Handle initial delay before the first green light
        if self.delay_on and self.delay > 0:
            if self.timer < self.delay:
                return  # Stay red during the delay
            else:
                self.timer = 0
                self.delay = 0  # Disable delay after first switch
                self.state = 'green'  # Turn green after delay
                self.delay_on = False

        # Normal green/red cycle
        if self.state == 'green' and self.timer >= self.green_duration:
            self.state = 'red'  # Change to red
            self.timer = 0  # Reset timer
        elif self.state == 'red' and self.timer >= self.red_duration:
            self.state = 'green'  # Change to green
            self.timer = 0  # Reset timer

    def draw(self, screen):
        """Draw the traffic light at its position."""
        color = (0, 255, 0) if self.state == 'green' else (255, 0, 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 10)

    def is_green(self):
        """Return whether the light is green."""
        return self.state == 'green'


# Create a car that follows the first path



# Create traffic lights for each path's end (for example, at the end of path1_data)





# def generate_cars(number_of_cars,path,traffic_light,time):
#     cars = []
#     for i in range(number_of_cars):
#         cars.append(Car(path,i,traffic_light,RED,speed=2))
#     return cars

# cars_path1 = generate_cars(20,path1_data,traffic_lights[0],1)
# cars_path2 = generate_cars(10,path2_data,traffic_lights[0],1)
# cars_path3 = generate_cars(5,path3_data,traffic_lights[1],1)
# cars_path4 = generate_cars(5,path4_data,traffic_lights[1],1)
# cars_path5 = generate_cars(4,path5_data,traffic_lights[2],1)
# cars_path6 = generate_cars(4,path6_data,traffic_lights[2],1)    



# cars_paths = [cars_path1,cars_path2,cars_path3,cars_path4,cars_path5,cars_path6]

# cars.append(Car(path1_data,1,traffic_lights[0], RED, speed=2,))
# # cars.append(Car(path2_data,traffic_lights[0], RED, speed=2))
# cars.append(Car(path1_data,2,traffic_lights[0], RED, speed=2,))
# cars.append(Car(path4_data, RED, speed=2))
# cars.append(Car(path5_data, RED, speed=2))
# cars.append(Car(path6_data, RED, speed=2))


def run_simulation(simulation):
    last_time = pygame.time.get_ticks()
    last_spawn_time = [0] * len(simulation.car_fields)
    cars = [[] for _ in range(len(simulation.car_fields)-1)]

    while simulation.running:
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000  # Convert to seconds
        last_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulation.running = False

        # Clear screen
        screen.fill((0, 0, 0))
        screen.blit(scaled_image, image_rect)

        # Update and draw traffic lights
        for traffic_light in simulation.traffic_lights:
            traffic_light.update(delta_time)
            traffic_light.draw(screen)

        # Spawn a car if enough time has passed
        for i in range(len(simulation.car_fields)):
            car_field = simulation.car_fields[i]
            if current_time - last_spawn_time[i] >= (car_field["spawn_time"] * 1000):
                last_spawn_time[i] = current_time  # Reset the timer
                if i ==5:
                    i=4
                new_car = Car(car_field["path"], len(cars[i]), car_field["traffic_light"], RED, speed=1)
                cars[i].append(new_car)
        for i in range(len(cars)):
            car_list = cars[i]
            for car in car_list:
                car.update_position(car_list)
                car.draw(screen)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


import time




class Simulation:
    def __init__(self, traffic_lights, car_fields,sim_delay,sim_loop):
        self.running = True
        self.traffic_lights = traffic_lights  # List of TrafficLight objects
        self.car_fields = car_fields  # List of paths for cars
        self.start_time = time.time()
        self.car_index = 0
        
traffic_lights_sim1 = [
    TrafficLight(light_c, green_duration=6, red_duration=5.5, delay=5),
    TrafficLight(light_ab, green_duration=2, red_duration=9.5, delay=0),  # Fixed the semicolon
    TrafficLight(light_d, green_duration=2, red_duration=9.5, delay=2.5)
]


car_fields_sim1 = [
    {"spawn_time": 0.5, "path": path1_data, "traffic_light": traffic_lights_sim1[0]},
    {"spawn_time": 1.5, "path": path2_data, "traffic_light": traffic_lights_sim1[0]},
    {"spawn_time": 3, "path": path3_data, "traffic_light": traffic_lights_sim1[1]},
    {"spawn_time": 3, "path": path4_data, "traffic_light": traffic_lights_sim1[1]},
    {"spawn_time": 3.5, "path": path5_data, "traffic_light": traffic_lights_sim1[2]},
    {"spawn_time": 3.5, "path": path6_data, "traffic_light": traffic_lights_sim1[2]}
]

traffic_lights_sim2 = [
    TrafficLight(light_c, green_duration=2, red_duration=5.5, delay=5),
    TrafficLight(light_ab, green_duration=2, red_duration=5.5, delay=0),  # Fixed the semicolon
    TrafficLight(light_d, green_duration=2, red_duration=5.5, delay=2.5)
]

car_fields_sim2 = [
    {"spawn_time": 3, "path": path1_data, "traffic_light": traffic_lights_sim2[0]},
    {"spawn_time": 3, "path": path2_data, "traffic_light": traffic_lights_sim2[0]},
    {"spawn_time": 3, "path": path3_data, "traffic_light": traffic_lights_sim2[1]},
    {"spawn_time": 3, "path": path4_data, "traffic_light": traffic_lights_sim2[1]},
    {"spawn_time": 3.5, "path": path5_data, "traffic_light": traffic_lights_sim2[2]},
    {"spawn_time": 3.5, "path": path6_data, "traffic_light": traffic_lights_sim2[2]}
]

traffic_lights_sim3 = [
    TrafficLight(light_c, green_duration=2, red_duration=9.5, delay=0),
    TrafficLight(light_ab, green_duration=6, red_duration=5.5, delay=5),  # Fixed the semicolon
    TrafficLight(light_d, green_duration=2, red_duration=9.5, delay=2.5)
]


car_fields_sim3 = [
    {"spawn_time": 3, "path": path1_data, "traffic_light": traffic_lights_sim3[0]},
    {"spawn_time": 3, "path": path2_data, "traffic_light": traffic_lights_sim3[0]},
    {"spawn_time": 0.50, "path": path3_data, "traffic_light": traffic_lights_sim3[1]},
    {"spawn_time": 1.5, "path": path4_data, "traffic_light": traffic_lights_sim3[1]},
    {"spawn_time": 3.5, "path": path5_data, "traffic_light": traffic_lights_sim3[2]},
    {"spawn_time": 3.5, "path": path6_data, "traffic_light": traffic_lights_sim3[2]}
]
# sim1 = Simulation(traffic_lights_sim1,car_fields_sim1,1,2)
# run_simulation(sim1)


# # sim2 = Simulation(traffic_lights_sim2,car_fields_sim2,1,2)
# # run_simulation(sim2)

# # sim3 = Simulation(traffic_lights_sim3,car_fields_sim3,1,2)
# # run_simulation(sim3)

##################################################################################################


                                # BUTTON MENU


##################################################################################################
# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation Selector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 120, 215)

# Font
font = pygame.font.Font(None, 40)

# Button properties
button_width = 300
button_height = 60
button_x = (WIDTH - button_width) // 2  # Centered horizontally
button_y_start = 200  # First button Y position
button_spacing = 80  # Space between buttons

# Create button rectangles
buttons = [
    pygame.Rect(button_x, button_y_start, button_width, button_height),
    pygame.Rect(button_x, button_y_start + button_spacing, button_width, button_height),
    pygame.Rect(button_x, button_y_start + 2 * button_spacing, button_width, button_height),
]

# Button labels
button_labels = ["Simulation 1", "Simulation 2", "Simulation 3"]

# Define simulations
simulations = [
    Simulation(traffic_lights_sim1, car_fields_sim1, 1, 2),
    Simulation(traffic_lights_sim2, car_fields_sim2, 1, 2),
    Simulation(traffic_lights_sim3, car_fields_sim3, 1, 2),
]


def draw_menu():
    """Draw the menu screen."""
    screen.fill(WHITE)  # Clear screen

    for i, button in enumerate(buttons):
        pygame.draw.rect(screen, BLUE, button, border_radius=10)
        text = font.render(button_labels[i], True, WHITE)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

    pygame.display.flip()  # Update display


def menu_loop():
    """Menu loop to select a simulation."""
    running = True
    while running:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit Pygame

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        return simulations[i]  # Return the selected simulation

    return None


# Main program
while True:
    selected_simulation = menu_loop()  # Show the menu and get the selected simulation
    if selected_simulation:
        run_simulation(selected_simulation)  # Run the chosen simulation
    else:
        break  # Exit if the user closes the menu

pygame.quit()