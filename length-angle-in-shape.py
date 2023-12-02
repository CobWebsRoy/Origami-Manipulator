import numpy as np
import matplotlib.pyplot as plt
import math

# Function to calculate the distance between two points
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to calculate the inner angle between three points
def inner_angle(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    
    vec1 = (x1 - x2, y1 - y2)
    vec2 = (x3 - x2, y3 - y2)
    
    dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    
    cos_theta = dot_product / (magnitude1 * magnitude2)
    return np.arccos(cos_theta)

# Input array of points (2D coordinates)
points = [(0, 0), (3, 0), (3, 2), (1, 3), (0, 2)]

# Initialize the plot
plt.figure()
ax = plt.gca()

# Plot the points
for point in points:
    ax.plot(point[0], point[1], 'o')

# Draw lines and calculate distances and inner angles
total_length = 0

Inner_angle = []
Not_norm_length = []

for i in range(len(points)):
    point1 = points[i]
    point2 = points[(i + 1) % len(points)]  # Circular loop
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r-')
    
    # Calculate and print distance
    dist = distance(point1, point2)
    total_length += dist
    Not_norm_length.append(dist)

    # print(f"Distance from {point1} to {point2}: {dist:.2f} units")
    # print(f"Length: {dist:.2f} units")

    # Calculate and print inner angle (in degrees)
    point3 = points[(i + 2) % len(points)]  # Next point
    angle = math.degrees(inner_angle(point1, point2, point3))
    Inner_angle.append(angle)
    
    # print(f"Inner angle at {point2}: {angle:.2f} degrees")
    # print(f"Angle: {angle:.2f} degrees")

# Print the total length of the shape
print(f"Total length: {total_length:.2f} units")

print(Inner_angle)
print(Not_norm_length/total_length*10)

# Show the plot
plt.grid()
plt.axis('equal')
plt.show()
