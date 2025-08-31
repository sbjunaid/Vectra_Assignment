import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

tiles = {4: "green", 3: "yellow", 2: "blue", 1: "red"}
directions = [(1,0), (0,1), (-1,0), (0,-1)]

def spiral_fill(M, N):
    grid = np.zeros((M, N), dtype=int)
    counts = {1:0, 2:0, 3:0, 4:0}
    cx, cy = M//2, N//2
    x, y = cx, cy
    step, dir_idx = 1, 0
    while np.any(grid == 0):
        for _ in range(2):
            dx, dy = directions[dir_idx % 4]
            for _ in range(step):
                if 0 <= x < M and 0 <= y < N and grid[x,y] == 0:
                    placed = False
                    for size in [4,3,2,1]:
                        if can_place(grid, x, y, size):
                            place_tile(grid, x, y, size)
                            counts[size] += 1
                            placed = True
                            break
                    if not placed:
                        grid[x,y] = 1
                        counts[1] += 1
                x += dx
                y += dy
            dir_idx += 1
        step += 1
    return grid, counts

def can_place(grid, x, y, size):
    M, N = grid.shape
    if x+size > M or y+size > N:
        return False
    if np.any(grid[x:x+size, y:y+size] != 0):
        return False
    return True

def place_tile(grid, x, y, size):
    grid[x:x+size, y:y+size] = size

def visualize(grid, counts):
    M, N = grid.shape
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0, N)
    ax.set_ylim(0, M)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    for i in range(M):
        for j in range(N):
            size = grid[i,j]
            if size != 0:
                rect = patches.Rectangle((j, i), 1, 1, facecolor=tiles[size], edgecolor="black", linewidth=0.3)
                ax.add_patch(rect)
    plt.title("Room Tiling with Squares (Spiral Fill)")
    plt.show()
    print("Tile counts:", counts)

M, N = 12, 10
grid, counts = spiral_fill(M, N)
visualize(grid, counts)
