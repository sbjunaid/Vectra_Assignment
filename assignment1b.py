import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

vertices = np.array([
    (9.05, 7.76),
    (12.5, 3.0),
    (10.0, 0.0),
    (5.0, 0.0),
    (2.5, 3.0)
])

vertices_closed = np.vstack([vertices, vertices[0]])
edges = np.diff(vertices_closed, axis=0)

def shoelace_area(pts):
    x, y = pts[:, 0], pts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

area_shoelace = shoelace_area(vertices)
area_shapely = Polygon(vertices).area
edge_lengths = np.linalg.norm(edges, axis=1)

angles = []
n = len(vertices)
for i in range(n):
    v1 = vertices[(i - 1) % n] - vertices[i]
    v2 = vertices[(i + 1) % n] - vertices[i]
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    cos_theta = np.clip(np.dot(v1_norm, v2_norm), -1.0, 1.0)
    theta = np.degrees(np.arccos(cos_theta))
    angles.append(theta)

is_convex = all(a < 180 for a in angles)
centroid_manual = vertices.mean(axis=0)
centroid_shapely = np.array(Polygon(vertices).centroid.coords[0])

print("Polygon Area (Shoelace):", area_shoelace)
print("Polygon Area (Shapely):", area_shapely)
print("Edge Lengths:", edge_lengths)
print("Interior Angles (degrees):", angles)
print("Is Convex:", is_convex)
print("Centroid (Manual):", centroid_manual)
print("Centroid (Shapely):", centroid_shapely)

plt.figure(figsize=(6,6))
plt.fill(vertices[:,0], vertices[:,1], color='lightblue', alpha=0.7, edgecolor='black')
for i, (x,y) in enumerate(vertices):
    plt.text(x, y, f"V{i+1}", fontsize=10, ha='right')
plt.scatter(*centroid_manual, color='red', zorder=5)
plt.text(centroid_manual[0], centroid_manual[1], "Centroid", color='red')
for i, (x, y) in enumerate(vertices):
    plt.text(x+0.2, y+0.2, f"{angles[i]:.1f}°", fontsize=8, color='darkgreen')
plt.gca().set_aspect('equal', adjustable='box')
plt.title("Polygon Geometry with Centroid & Angles")
plt.show()
