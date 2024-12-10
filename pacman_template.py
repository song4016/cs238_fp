import pygame
import time
import random

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
pygame.display.set_caption("Grid Pac-Man with Fog of War")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

# Count initial dots
total_dots = sum(row.count(2) for row in grid)

# Initialize visibility grid
# 0 = unseen, 1 = seen but not currently visible, 2 = currently visible
visibility_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Player and ghost settings
player_pos = [10, 15]  # Grid coordinates
ghost_pos = [10, 8]  # Ghost starts in the middle
MOVE_INTERVAL = 0.1
GHOST_MOVE_INTERVAL = 0.3
last_move_time = time.time()
last_ghost_move_time = time.time()

# Game variables
running = True
score = 0
game_over = False
victory = False

# Vision settings
VISION_RADIUS = 5


def grid_to_pixel(grid_x, grid_y):
    """Convert grid coordinates to pixel coordinates"""
    return (grid_x * CELL_SIZE + CELL_SIZE // 2, grid_y * CELL_SIZE + CELL_SIZE // 2)


def can_move(new_x, new_y):
    """Check if movement to the new grid position is possible"""
    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        return grid[new_y][new_x] != 1
    return False


def move_ghost():
    """Move ghost in a random valid direction"""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # possible movements
    random.shuffle(directions)  # randomize directions

    for dx, dy in directions:
        new_x = ghost_pos[0] + dx
        new_y = ghost_pos[1] + dy
        if can_move(new_x, new_y):
            ghost_pos[0] = new_x
            ghost_pos[1] = new_y
            break


def check_collision():
    """Check if ghost caught Pac-Man"""
    return player_pos == ghost_pos


def check_victory():
    """Check if all dots have been collected"""
    return score == total_dots


def reset_game():
    """Reset the game state"""
    global player_pos, ghost_pos, score, game_over, victory, grid, visibility_grid
    player_pos = [10, 15]
    ghost_pos = [10, 8]
    score = 0
    game_over = False
    victory = False
    # Reset grid - restore all dots
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 0 and not (
                y == 8 and x == 8
            ):  # Don't put dots in ghost area
                grid[y][x] = 2
    # Reset visibility grid
    visibility_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    update_visibility()


def draw_game_over():
    """Draw game over screen"""
    font = pygame.font.Font(None, 74)
    if victory:
        text = font.render("YOU WIN!", True, GREEN)
    else:
        text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(score_text, score_rect)


def get_line(x0, y0, x1, y1):
    """Bresenham's Line Algorithm"""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        points.append((x, y))
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        points.append((x, y))
    return points


def move_pacman():
    # NEW CODE HERE - REPLACE THE OLD FUNCTION
    """Move pacman in a random valid direction"""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # possible movements
    random.shuffle(directions)  # randomize directions
    for dx, dy in directions:
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if can_move(new_x, new_y):
            player_pos[0] = new_x
            player_pos[1] = new_y
            break


def update_visibility():
    """Update visibility grid based on player's position"""
    px, py = player_pos[0], player_pos[1]
    # Reset all 'currently visible' cells to 'seen but not currently visible'
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if visibility_grid[y][x] == 2:
                visibility_grid[y][x] = 1
    # Update currently visible cells
    for dy in range(-VISION_RADIUS, VISION_RADIUS + 1):
        for dx in range(-VISION_RADIUS, VISION_RADIUS + 1):
            x = px + dx
            y = py + dy
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                distance = max(abs(dx), abs(dy))
                if distance <= VISION_RADIUS:
                    # Check line of sight
                    line = get_line(px, py, x, y)
                    visible = True
                    for lx, ly in line:
                        if grid[ly][lx] == 1 and (lx, ly) != (x, y):
                            visible = False
                            break
                    if visible:
                        visibility_grid[y][x] = 2  # currently visible


# Main game loop
clock = pygame.time.Clock()

# Initial update of visibility
update_visibility()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and (game_over or victory):
            if event.key == pygame.K_SPACE:
                reset_game()

    if not game_over and not victory:
        # Handle Pac-Man movement
        current_time = time.time()
        if current_time - last_move_time >= MOVE_INTERVAL:
            move_pacman()
            check_collision()
            update_visibility()

            # Collect dot if present
            if grid[player_pos[1]][player_pos[0]] == 2:
                grid[player_pos[1]][player_pos[0]] = 0
                score += 1
                # Check for victory
                if check_victory():
                    victory = True

            last_move_time = current_time

        # Handle ghost movement
        if current_time - last_ghost_move_time >= GHOST_MOVE_INTERVAL:
            move_ghost()
            last_ghost_move_time = current_time

        # Check if ghost caught Pac-Man
        if check_collision():
            game_over = True

    # Update visibility (in case the ghost moves into view)
    update_visibility()

    # Draw game
    screen.fill(BLACK)

    # Draw grid with fog of war
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            visibility = visibility_grid[y][x]
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if visibility == 0:
                # Unseen: Draw black rectangle
                pygame.draw.rect(screen, BLACK, cell_rect)
            else:
                # Cell has been seen
                if visibility == 2:
                    # Currently visible: draw normally
                    if grid[y][x] == 1:  # Wall
                        pygame.draw.rect(screen, BLUE, cell_rect)
                    else:
                        pygame.draw.rect(screen, BLACK, cell_rect)
                        if grid[y][x] == 2:  # Dot
                            pygame.draw.circle(
                                screen,
                                WHITE,
                                (
                                    x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2,
                                ),
                                CELL_SIZE // 6,
                            )
                else:
                    # Seen but not currently visible: draw dimmed
                    if grid[y][x] == 1:  # Wall
                        pygame.draw.rect(screen, (0, 0, 100), cell_rect)  # Dimmed wall
                    else:
                        pygame.draw.rect(screen, (20, 20, 20), cell_rect)  # Dimmed path
                        if grid[y][x] == 2:  # Dot
                            pygame.draw.circle(
                                screen,
                                (100, 100, 100),
                                (
                                    x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2,
                                ),
                                CELL_SIZE // 6,
                            )

    # Draw player
    player_pixel_pos = grid_to_pixel(player_pos[0], player_pos[1])
    pygame.draw.circle(screen, YELLOW, player_pixel_pos, CELL_SIZE // 2 - 2)

    # Draw ghost if game is active and visible
    if not victory and visibility_grid[ghost_pos[1]][ghost_pos[0]] == 2:
        ghost_pixel_pos = grid_to_pixel(ghost_pos[0], ghost_pos[1])
        pygame.draw.circle(screen, RED, ghost_pixel_pos, CELL_SIZE // 2 - 2)

    # Draw score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}/{total_dots}", True, WHITE)
    screen.blit(text, (5, 5))

    # Draw game over or victory screen
    if game_over or victory:
        draw_game_over()
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
        )
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
