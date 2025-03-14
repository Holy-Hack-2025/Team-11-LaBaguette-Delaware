import pygame


# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SVG Path Display")


# Define a function to draw the path
def draw_path(path_data):
    for segment in path_data:
        start = segment['start']
        end = segment['end']
        pygame.draw.line(screen, (255, 0, 0), (start['x'], start['y']), (end['x'], end['y']), 2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill((255, 255, 255))

    # Draw the path
    draw_path(path_data)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
