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
VISION_RADIUS = 5  # Adjust as needed

# Track last player direction to avoid immediate back-and-forth
last_pacman_dir = None


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
    global player_pos, ghost_pos, score, game_over, victory, grid, visibility_grid, last_pacman_dir
    player_pos = [10, 15]
    ghost_pos = [10, 8]
    score = 0
    game_over = False
    victory = False
    last_pacman_dir = None
    # Reset grid - restore all dots
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 0 and not (y == 8 and x == 8):
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


def normalize_belief(belief):
    total_prob = sum(belief.values())
    if total_prob > 0:
        return {k: v / total_prob for k, v in belief.items()}
    else:
        # Reset belief to uniform distribution
        return {
            (x, y): 1 / (GRID_WIDTH * GRID_HEIGHT)
            for y in range(GRID_HEIGHT)
            for x in range(GRID_WIDTH)
        }


def update_belief_pomdp(belief, observation, ghost_pos, visibility_grid):
    """
    Update belief state based on observation and ghost movement.
    """
    new_belief = {}
    if observation == 2:  # Ghost observed at player's position
        new_belief = {pos: (1 if pos == tuple(ghost_pos) else 0) for pos in belief}
    else:
        # Update belief based on ghost movement
        for (x, y), prob in belief.items():
            neighbors = [
                (x + dx, y + dy)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                if 0 <= x + dx < GRID_WIDTH
                and 0 <= y + dy < GRID_HEIGHT
                and grid[y + dy][x + dx] != 1
            ]
            if neighbors:
                prob_per_neighbor = prob / len(neighbors)
                for nx, ny in neighbors:
                    new_belief[(nx, ny)] = (
                        new_belief.get((nx, ny), 0) + prob_per_neighbor
                    )
            else:
                # If no neighbors, remain in place
                new_belief[(x, y)] = new_belief.get((x, y), 0) + prob

    # Normalize the belief
    return normalize_belief(new_belief)


def get_neighborhood(center_x, center_y, radius=5):
    """
    Get all cells within a given Manhattan distance from a center.
    """
    neighbors = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            x, y = center_x + dx, center_y + dy
            if (
                0 <= x < GRID_WIDTH
                and 0 <= y < GRID_HEIGHT
                and abs(dx) + abs(dy) <= radius
            ):
                neighbors.append((x, y))
    return neighbors


def solve_pomdp(belief, rewards, radius=5, discount=0.9, iterations=50):
    """
    Solve the POMDP by focusing on a neighborhood around Pac-Man.
    """
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left
    # Initialize action_values
    action_values = {((x, y), (dx, dy)): 0 for (x, y) in belief for (dx, dy) in actions}

    # Restrict computation to relevant cells
    # Just a heuristic to not solve entire map every time
    neighborhood = get_neighborhood(player_pos[0], player_pos[1], radius)

    for _ in range(iterations):
        new_action_values = {}
        for x, y in neighborhood:
            if grid[y][x] == 1:  # Skip walls
                continue
            for dx, dy in actions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] != 1:
                    reward = rewards[y][x]
                    future_value = discount * sum(
                        belief.get((sx, sy), 0)
                        * max(action_values.get(((sx, sy), a), 0) for a in actions)
                        for (sx, sy) in neighborhood
                    )
                    new_value = belief.get((x, y), 0) * (reward + future_value)
                    new_action_values[((x, y), (dx, dy))] = (
                        new_action_values.get(((x, y), (dx, dy)), 0) + new_value
                    )
        action_values = new_action_values

    return action_values


def move_pacman_pomdp(player_pos, belief, action_values, last_direction):
    """
    Move Pac-Man based on POMDP by maximizing expected utility.
    Add tie-breaking and avoid immediate backtracking to reduce oscillation.
    """
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left
    best_actions = []
    best_value = float("-inf")

    for dx, dy in actions:
        value = 0
        for (x, y), prob in belief.items():
            state_action = ((x, y), (dx, dy))
            value += prob * action_values.get(state_action, -1000)
        if value > best_value:
            best_value = value
            best_actions = [(dx, dy)]
        elif abs(value - best_value) < 1e-6:
            # Tie: consider multiple best actions
            best_actions.append((dx, dy))

    # Random tie-break among best actions
    if best_actions:
        best_action = random.choice(best_actions)
    else:
        best_action = None

    # Avoid immediate backtracking if possible
    if (
        best_action
        and last_direction
        and (
            best_action[0] == -last_direction[0]
            and best_action[1] == -last_direction[1]
        )
    ):
        # Try to pick another best action that is not opposite
        non_opposites = [
            a
            for a in best_actions
            if not (a[0] == -last_direction[0] and a[1] == -last_direction[1])
        ]
        if non_opposites:
            best_action = random.choice(non_opposites)

    if best_action:
        new_x = player_pos[0] + best_action[0]
        new_y = player_pos[1] + best_action[1]
        if can_move(new_x, new_y):
            return (new_x, new_y), best_action

    # Random fallback movement if no good action found
    random_actions = actions[:]
    random.shuffle(random_actions)
    for dx, dy in random_actions:
        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy
        if can_move(new_x, new_y):
            return (new_x, new_y), (dx, dy)

    # No move possible, stay in place
    return player_pos, None


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


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute_rewards(ghost_pos):
    """
    Compute rewards dynamically:
    - High reward for dots.
    - Slight negative reward for normal paths.
    - Extra reward for exploring unseen areas (visibility == 0).
    - Negative reward for cells near the ghost (increases as get closer).
    """
    new_rewards = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                # Wall - no movement here, can be low or zero
                new_rewards[y][x] = -100
            elif grid[y][x] == 2:
                # Dot
                new_rewards[y][x] = 100
            else:
                # Empty path
                # Base: small negative to encourage moving rather than staying
                new_rewards[y][x] = -5

            # Encourage exploration: unseen cells get an extra positive reward
            if visibility_grid[y][x] == 0:
                new_rewards[y][x] += 20  # unseen cells are highly attractive

            # Penalize proximity to ghost
            d = distance((x, y), ghost_pos)
            if d < 5:
                # The closer to the ghost, the more negative
                new_rewards[y][x] -= (5 - d) * 20  # stronger penalty when closer

    return new_rewards


# Initial update of visibility
update_visibility()

# Initialize belief
belief = {
    (x, y): 1 / (GRID_WIDTH * GRID_HEIGHT)
    for y in range(GRID_HEIGHT)
    for x in range(GRID_WIDTH)
}

clock = pygame.time.Clock()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and (game_over or victory):
            if event.key == pygame.K_SPACE:
                reset_game()

    if not game_over and not victory:
        current_time = time.time()

        # Compute dynamic rewards based on current state
        rewards = compute_rewards(ghost_pos)

        # Handle Pac-Man movement
        if current_time - last_move_time >= MOVE_INTERVAL:
            # Update belief state based on observation
            observation = visibility_grid[player_pos[1]][player_pos[0]]
            belief = update_belief_pomdp(
                belief, observation, ghost_pos, visibility_grid
            )

            # Solve POMDP and move Pac-Man
            action_values = solve_pomdp(belief, rewards)
            (new_x, new_y), chosen_dir = move_pacman_pomdp(
                player_pos, belief, action_values, last_pacman_dir
            )

            # Update position if valid
            if can_move(new_x, new_y):
                player_pos = [new_x, new_y]
                last_pacman_dir = chosen_dir if chosen_dir else last_pacman_dir
                # Update visibility
                update_visibility()
                # Collect dot if present
                if grid[new_y][new_x] == 2:
                    grid[new_y][new_x] = 0
                    score += 1
                    # Check for victory
                    if check_victory():
                        victory = True

            last_move_time = current_time

        # Handle ghost movement
        if current_time - last_ghost_move_time >= GHOST_MOVE_INTERVAL:
            move_ghost()
            belief = normalize_belief(
                update_belief_pomdp(belief, None, ghost_pos, visibility_grid)
            )
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
