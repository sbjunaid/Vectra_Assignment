import matplotlib.pyplot as plt
import numpy as np

def equilateral_triangle(x, y, side, upright=True):
    h = np.sqrt(3) / 2 * side
    if upright:
        return [(x, y), (x + side, y), (x + side/2, y + h)]
    else:
        return [(x, y + h), (x + side, y + h), (x + side/2, y)]

def build_pyramid(side, depth):
    h = np.sqrt(3) / 2 * side
    fig, ax = plt.subplots(figsize=(8, 6))
    for row in range(depth):
        num_triangles = row + 1
        x_offset = (depth - num_triangles) * side / 2
        y_offset = row * h
        upright = (row % 2 == 0)
        for col in range(num_triangles):
            x = x_offset + col * side
            y = y_offset
            tri = equilateral_triangle(x, y, side, upright=upright)
            color = "skyblue" if upright else "salmon"
            poly = plt.Polygon(tri, closed=True, edgecolor="black", facecolor=color)
            ax.add_patch(poly)
    ax.set_aspect('equal')
    ax.set_xlim(0, depth * side)
    ax.set_ylim(0, depth * h + side)
    plt.axis('off')
    plt.title(f"Pyramid of Triangles (Depth {depth})")
    plt.show()

build_pyramid(side=2, depth=5)
