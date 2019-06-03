import pdb
from helpers import normalize, blur

def initialize_beliefs(grid):
    height = len(grid)
    width = len(grid[0])
    area = height * width
    belief_per_cell = 1.0 / area
    beliefs = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

def sense(color, grid, beliefs, p_hit, p_miss):
    new_beliefs = beliefs
    s = 0.0;
    for y, row in enumerate(new_beliefs):
        for x, b in enumerate(row):            
            new_beliefs[y][x] = b * p_hit if grid[y][x] == color else b * p_miss
            s += new_beliefs[y][x]

    for y, row in enumerate(new_beliefs):
        for x, b in enumerate(row):
            new_beliefs[y][x] = b/s

    return new_beliefs

def move(dy, dx, beliefs, blurring):
    height = len(beliefs)
    width = len(beliefs[0])
    new_G = [[0.0 for x in range(width)] for y in range(height)]
    for y, row in enumerate(beliefs):
        for x, cell in enumerate(row):
            new_x = (x + dx ) % width
            new_y = (y + dy ) % height
            new_G[new_y][new_x] = cell
    return blur(new_G, blurring)