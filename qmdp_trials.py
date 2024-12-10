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


def can_move(new_x, new_y, grid):
    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        return grid[new_y][new_x] != 1
    return False


def move_ghost(ghost_pos, grid):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = ghost_pos[0] + dx, ghost_pos[1] + dy
        if can_move(nx, ny, grid):
            return [nx, ny]
    return ghost_pos


def check_collision(player_pos, ghosts):
    return any(player_pos == ghost for ghost in ghosts)


def solve_mdp(grid):
    discount = 0.9
    iterations = 200
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rewards = [[100 if cell == 2 else -5 for cell in row] for row in grid]

    values = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for _ in range(iterations):
        new_values = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 1:
                    new_values[y][x] = 0
                    continue
                qs = []
                for dx, dy in actions:
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < GRID_WIDTH
                        and 0 <= ny < GRID_HEIGHT
                        and grid[ny][nx] != 1
                    ):
                        qs.append(rewards[y][x] + discount * values[ny][nx])
                    else:
                        qs.append(rewards[y][x])
                new_values[y][x] = max(qs)
        values = new_values

    q_values = {}
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                continue
            for dx, dy in actions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] != 1:
                    q_values[((x, y), (dx, dy))] = (
                        rewards[y][x] + discount * values[ny][nx]
                    )
                else:
                    q_values[((x, y), (dx, dy))] = rewards[y][x]
    return q_values


def move_pacman_qmdp(player_pos, q_values, grid):
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    best_action = None
    best_q = float("-inf")
    for dx, dy in actions:
        nx, ny = player_pos[0] + dx, player_pos[1] + dy
        if can_move(nx, ny, grid):
            state_action = ((player_pos[0], player_pos[1]), (dx, dy))
            qval = q_values.get(state_action, -1000)
            if qval > best_q:
                best_q = qval
                best_action = (dx, dy)
    if best_action:
        return [player_pos[0] + best_action[0], player_pos[1] + best_action[1]]
    return player_pos


def run_qmdp_trial(grid):
    player_pos = [10, 15]
    ghosts = [[10, 10], [10, 11], [11, 10]]
    local_grid = [row[:] for row in grid]
    score = 0

    q_values = solve_mdp(local_grid)

    while True:
        player_pos = move_pacman_qmdp(player_pos, q_values, local_grid)
        if local_grid[player_pos[1]][player_pos[0]] == 2:
            local_grid[player_pos[1]][player_pos[0]] = 0
            score += 1
        if score == total_dots:
            return score
        for i in range(len(ghosts)):
            ghosts[i] = move_ghost(ghosts[i], local_grid)
        if check_collision(player_pos, ghosts):
            return score


def run_experiments(num_trials=10, grid=None):
    qmdp_scores = []
    for _ in range(num_trials):
        print("Running trial", _ + 1)
        qmdp_scores.append(run_qmdp_trial(grid))

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_trials + 1), qmdp_scores, label="QMDP", marker="o")
    plt.xlabel("Trial")
    plt.ylabel("Score")
    plt.title("QMDP Strategy Performance with 3 Ghosts")
    plt.legend()
    plt.grid(True)
    plt.show()


# Run experiments
run_experiments(num_trials=10, grid=grid)
