import random
import matplotlib.pyplot as plt

# Grid and environment constants
GRID_WIDTH = 20
GRID_HEIGHT = 20

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
total_dots = sum(row.count(2) for row in grid)


def can_move(new_x, new_y):
    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        return grid[new_y][new_x] != 1
    return False


def move_ghost(ghost_pos):
    # Random movement for ghost
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = ghost_pos[0] + dx, ghost_pos[1] + dy
        if can_move(nx, ny):
            return [nx, ny]
    return ghost_pos


def check_collision(player_pos, ghosts):
    return any(player_pos == ghost for ghost in ghosts)


def run_random_trial():
    player_pos = [10, 15]
    ghosts = [[10, 10], [10, 11], [11, 10]]
    local_grid = [row[:] for row in grid]
    score = 0

    while True:
        # Move player randomly
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = player_pos[0] + dx, player_pos[1] + dy
            if can_move(nx, ny):
                player_pos = [nx, ny]
                break

        # Collect dots
        if local_grid[player_pos[1]][player_pos[0]] == 2:
            local_grid[player_pos[1]][player_pos[0]] = 0
            score += 1

        # Check victory
        if score == total_dots:
            return score

        # Move ghosts
        for i in range(len(ghosts)):
            ghosts[i] = move_ghost(ghosts[i])

        # Check collisions
        if check_collision(player_pos, ghosts):
            return score


def run_experiments(num_trials=10):
    random_scores = []
    for _ in range(num_trials):
        random_scores.append(run_random_trial())

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_trials + 1), random_scores, label="Random", marker="o")
    plt.xlabel("Trial")
    plt.ylabel("Score")
    plt.title("Random Strategy Performance with 3 Ghosts")
    plt.legend()
    plt.grid(True)
    plt.show()


# Run the experiments
run_experiments(num_trials=10)
