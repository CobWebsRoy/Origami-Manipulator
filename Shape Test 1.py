import numpy as np
import matplotlib.pyplot as plt

# Input array of 2D points (replace this with your own set of points)
points = np.array([
    [0, 8],
    [2, 8],
    [4, 4],
    [6, 8],
    [16, 8],
    [15, 6],
    [12, 6],
    [9, 0],
    [7, 0],
    [10,6],
    [7, 6],
    [4,0]
])

# Extract x and y coordinates of the points
x_coordinates = points[:, 0]
y_coordinates = points[:, 1]

# Connect the points to form the outline
connected_points = np.append(points, [points[0]], axis=0)

# Plot the outline of the shape
plt.figure(figsize=(8, 6))
plt.plot(connected_points[:, 0], connected_points[:, 1], marker='o', linestyle='-', color='b')
plt.grid()
plt.title('Outline of the Object Shape')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.axis('equal')
plt.show()