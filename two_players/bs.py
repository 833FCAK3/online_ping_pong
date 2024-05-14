import pygame


# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Manipulation")

# Load the image
image = pygame.image.load("images/life.png")

# Get the width of the image
image_width = image.get_width()

# Draw the image 3 times to the right
for i in range(3):
    SCREEN.blit(image, (i * image_width, 0))

# Create a single image from the three drawn images
combined_image = pygame.Surface((image_width * 3, image.get_height()))
combined_image.blit(SCREEN, (0, 0), (0, 0, image_width * 3, image.get_height()))
rect = combined_image.get_rect()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display the combined image
    SCREEN.blit(combined_image, (0, 0))
    rect.x += 1

    pygame.display.flip()

# Quit Pygame
pygame.quit()
