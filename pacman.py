import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

# Set up colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Set up the player and dot properties
player_radius = 15
player_color = YELLOW  # Yellow for Pac-Man
dot_radius = 5
dot_color = WHITE  # White for dots

# Set up the player and dot positions
player_x = 300
player_y = 300
dot_x = 100
dot_y = 100

# Define walls (each wall is a rectangle: [x, y, width, height])
walls = [
    # Outer walls
    [50, 50, 700, 20],  # Top
    [50, 50, 20, 500],  # Left
    [730, 50, 20, 500],  # Right
    [50, 530, 700, 20],  # Bottom
    # Inner walls
    [150, 150, 20, 200],  # Vertical wall
    [150, 150, 200, 20],  # Horizontal wall
    [450, 150, 20, 200],  # Another vertical wall
    [450, 150, 200, 20],  # Another horizontal wall
    [150, 450, 500, 20],  # Bottom horizontal wall
]

# Create wall rectangles for collision detection
wall_rects = [pygame.Rect(wall[0], wall[1], wall[2], wall[3]) for wall in walls]

# Set up the game variables
running = True
score = 0
speed = 5

# Set up movement timer
MOVE_INTERVAL = 0.1
last_move_time = time.time()


def check_collision(new_x, new_y):
    """Check if the player would collide with any wall at the given position"""
    player_rect = pygame.Rect(
        new_x - player_radius,
        new_y - player_radius,
        player_radius * 2,
        player_radius * 2,
    )
    for wall_rect in wall_rects:
        if player_rect.colliderect(wall_rect):
            return True
    return False


# Main game loop
clock = pygame.time.Clock()

while running:
    # Check for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle movement every half second
    current_time = time.time()
    if current_time - last_move_time >= MOVE_INTERVAL:
        # Handle key presses
        keys = pygame.key.get_pressed()
        new_x = player_x
        new_y = player_y

        if keys[pygame.K_LEFT]:
            new_x -= speed
        elif keys[pygame.K_RIGHT]:
            new_x += speed
        elif keys[pygame.K_UP]:
            new_y -= speed
        elif keys[pygame.K_DOWN]:
            new_y += speed

        # Only update position if there's no wall collision
        if not check_collision(new_x, new_y):
            player_x = new_x
            player_y = new_y

        last_move_time = current_time

    # Update game state - collect dots
    if abs(player_x - dot_x) < (player_radius + dot_radius) and abs(
        player_y - dot_y
    ) < (player_radius + dot_radius):
        score += 1
        dot_x = -100
        dot_y = -100

    # Draw game
    screen.fill(BLACK)  # Black background

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)

    # Draw player (Pac-Man) as a yellow circle
    pygame.draw.circle(screen, player_color, (player_x, player_y), player_radius)

    # Draw dot as a white circle
    pygame.draw.circle(screen, dot_color, (dot_x, dot_y), dot_radius)

    # Draw score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Draw movement timer
    time_until_next = max(0, MOVE_INTERVAL - (current_time - last_move_time))
    timer_text = font.render(f"Move in: {time_until_next:.1f}s", True, WHITE)
    screen.blit(timer_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Quit Pygame
pygame.quit()
