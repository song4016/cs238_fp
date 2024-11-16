import pygame
import time

# Initialize Pygame
pygame.init()

# Grid settings
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Pac-Man")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define the game grid
# 0 = empty path
# 1 = wall
# 2 = dot
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1],
    [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Player settings
player_pos = [10, 15]  # Grid coordinates
MOVE_INTERVAL = 0.2
last_move_time = time.time()

# Game variables
running = True
score = 0


def grid_to_pixel(grid_x, grid_y):
    """Convert grid coordinates to pixel coordinates"""
    return (grid_x * CELL_SIZE + CELL_SIZE // 2, grid_y * CELL_SIZE + CELL_SIZE // 2)


def can_move(new_x, new_y):
    """Check if the player can move to the new grid position"""
    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        return grid[new_y][new_x] != 1
    return False


# Main game loop
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle movement every MOVE_INTERVAL seconds
    current_time = time.time()
    if current_time - last_move_time >= MOVE_INTERVAL:
        keys = pygame.key.get_pressed()
        new_x, new_y = player_pos[0], player_pos[1]

        if keys[pygame.K_LEFT]:
            new_x -= 1
        elif keys[pygame.K_RIGHT]:
            new_x += 1
        elif keys[pygame.K_UP]:
            new_y -= 1
        elif keys[pygame.K_DOWN]:
            new_y += 1

        # Update position if movement is valid
        if can_move(new_x, new_y):
            player_pos = [new_x, new_y]
            # Collect dot if present
            if grid[new_y][new_x] == 2:
                grid[new_y][new_x] = 0
                score += 1

            last_move_time = current_time

    # Draw game
    screen.fill(BLACK)

    # Draw grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLUE, cell_rect)
            elif grid[y][x] == 2:  # Dot
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                    CELL_SIZE // 6,
                )

    # Draw player
    player_pixel_pos = grid_to_pixel(player_pos[0], player_pos[1])
    pygame.draw.circle(screen, YELLOW, player_pixel_pos, CELL_SIZE // 2 - 2)

    # Draw score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
