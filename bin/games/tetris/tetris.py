import pygame
import random
from time import sleep

# Farben
COLORS = [
    (0, 0, 0),       # Hintergrund
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (128, 0, 128),   # T
    (255, 0, 0)      # Z
]

# Tetris-Formen
SHAPES = [
    [[1, 1, 1, 1]],
    [[2, 0, 0],
     [2, 2, 2]],
    [[0, 0, 3],
     [3, 3, 3]],
    [[4, 4],
     [4, 4]],
    [[0, 5, 5],
     [5, 5, 0]],
    [[0, 6, 0],
     [6, 6, 6]],
    [[7, 7, 0],
     [0, 7, 7]]
]

# Grid-Konfiguration
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Fenster
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# Funktionen
def create_grid(locked={}):
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked:
                grid[y][x] = locked[(x, y)]
    return grid

def convert_shape(shape, offset):
    positions = []
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                positions.append((offset[0] + j, offset[1] + i))
    return positions

def valid_space(shape, grid, offset):
    accepted = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == 0] for i in range(GRID_HEIGHT)]
    accepted = [j for sub in accepted for j in sub]
    for pos in convert_shape(shape, offset):
        if pos not in accepted:
            if pos[1] >= 0:
                return False
    return True

def clear_rows(grid, locked):
    cleared = 0
    for i in range(len(grid) - 1, -1, -1):
        if 0 not in grid[i]:
            cleared += 1
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, i)]
                except:
                    continue
            for y in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y_val = y
                if y_val < i:
                    new_key = (x, y_val + 1)
                    locked[new_key] = locked.pop((x, y_val))
    return cleared

def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, COLORS[grid[y][x]], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
    for i in range(GRID_HEIGHT):
        pygame.draw.line(screen, (50, 50, 50), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for j in range(GRID_WIDTH):
        pygame.draw.line(screen, (50, 50, 50), (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def rotate_clockwise(shape):
    return [list(row) for row in zip(*shape[::-1])]

def rotate_counter_clockwise(shape):
    return [list(row) for row in zip(*shape)][::-1]

# Main-Loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    locked_positions = {}
    grid = create_grid(locked_positions)

    shape = random.choice(SHAPES)
    shape_pos = [3, 0]
    shape_color = SHAPES.index(shape) + 1

    fall_time = 0
    fall_speed = 0.5

    score = 0
    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            shape_pos[1] += 1
            if not valid_space(shape, grid, shape_pos):
                shape_pos[1] -= 1
                for pos in convert_shape(shape, shape_pos):
                    locked_positions[pos] = shape_color
                shape = random.choice(SHAPES)
                shape_pos = [3, 0]
                shape_color = SHAPES.index(shape) + 1
                if not valid_space(shape, grid, shape_pos):
                    running = False
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape_pos[0] -= 1
                    if not valid_space(shape, grid, shape_pos):
                        shape_pos[0] += 1
                elif event.key == pygame.K_RIGHT:
                    shape_pos[0] += 1
                    if not valid_space(shape, grid, shape_pos):
                        shape_pos[0] -= 1
                elif event.key == pygame.K_DOWN:
                    shape_pos[1] += 1
                    if not valid_space(shape, grid, shape_pos):
                        shape_pos[1] -= 1
                elif event.key == pygame.K_UP:
                    new_shape = rotate_clockwise(shape)
                    if valid_space(new_shape, grid, shape_pos):
                        shape = new_shape
                elif event.key == pygame.K_a:
                    new_shape = rotate_counter_clockwise(shape)
                    if valid_space(new_shape, grid, shape_pos):
                        shape = new_shape
                elif event.key == pygame.K_b:
                    new_shape = rotate_clockwise(shape)
                    if valid_space(new_shape, grid, shape_pos):
                        shape = new_shape

        for pos in convert_shape(shape, shape_pos):
            x, y = pos
            if y >= 0:
                grid[y][x] = shape_color

        cleared = clear_rows(grid, locked_positions)
        if cleared > 0:
            score += (cleared ** 2) * 100

        screen.fill((0, 0, 0))
        draw_grid(screen, grid)
        pygame.display.update()

    pygame.quit()
    print(f"Game Over! Score: {score}")
    if input("Do you want to play again? (y/n)").lower() == 'y':
        main()
    else:
        print("Thanks for playing!")
        sleep(2)

if __name__ == "__main__":
    main()
