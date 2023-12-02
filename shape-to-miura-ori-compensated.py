import numpy as np
import matplotlib.pyplot as plt
import math

# CONSTANTS
IA = 45 # Actuation input angle
W = 2 # Width
Length = 30
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

# Function to calculate the miura-ori FOLD ANGLE from the SHAPE ANGLE
def shape_to_fold(angle):
    OA = angle
    interm = (math.cos(math.radians(IA))**2) * (math.cos(math.radians(OA/2))**2) - 1
    interm = (math.cos(math.radians(OA/2))**2 - 1) / interm
    interm = interm ** 0.5
    FA = math.asin(interm)

    return math.degrees(FA)

# Function to calculate COVERED DISTANCE
def covered_distance(angle):
    C = W*math.sin(math.radians(IA))/math.sin(math.radians(angle))
    return C


"""
Input array of points (2D coordinates)

CHANGE THE BELOW POINTS FOR THE SHAPE TO CUT
MAKE SURE THERE ARE ODD NUMBERS OF POINTS
IF THERE ARE EVEN NUMBERS, ADD THE FIRST POINT AGAIN TO THE END
"""
#Original house shape:
#points = [(0, 0), (3, 0), (3, 2), (2, 3), (1, 3), (0, 2)]

#Pentagon:
points = [ 
          (10*math.cos(math.radians(18)),10*math.sin(math.radians(18))), 
          (10*math.cos(math.radians(-54)),10*math.sin(math.radians(-54))), 
          (-10*math.cos(math.radians(-54)),10*math.sin(math.radians(-54))),
          (-10*math.cos(math.radians(18)),10*math.sin(math.radians(18))),
          (0,10)
        ]

#Modified house shape:
#points = [(0, 1), (3, 1), (3, 2), (2, 3), (1, 3), (0, 2), (0, 1)]

#Test Gripper Shape:
#points = [(3,0),(5,0),(8,1),(5,3),(3,3),(0,1),(3,0)]

#VT shape:
#points = [(12,6), (9,0), (7,0), (10,6), (7,6), (4,0), (0,8), (2,8), (4,4), (6,8), (16,8), (15,6)]


# Plot the input points
plt.figure(1)
ax = plt.gca()
ax.grid()
ax.axis('equal')

for point in points:
    ax.plot(point[0], point[1], 'o')

# Draw lines and calculate distances and inner angles
total_length = 0
Shape_angle = []
Fold_angle = []
Fold_angle_norm = []
Norm_length_total = []
Norm_length_fold = []
Fold_coord = []
Covered_distance = []
covered = 0

for i in range(len(points)):
    point1 = points[i]
    point2 = points[(i + 1) % len(points)]  # Circular loop
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r-')
    
    # Calculate OUTPUT/SHAPE ANGLE (in degrees)
    point3 = points[(i + 2) % len(points)]  # Next point
    angle = math.degrees(inner_angle(point1, point2, point3))
    angle = 180 - angle
    Shape_angle.append(angle)
    print(f"A: {angle:.2f}°")

    # Back-calculate and print the FOLD ANGLE REQUIRED (in degrees)
    fold_angle_original = shape_to_fold(angle)
    if i % 2 == 0:
        F_a = fold_angle_original
    else:
        F_a = 180 - fold_angle_original # flip direction for even number
    Fold_angle.append(fold_angle_original) 
    Fold_angle_norm.append(F_a) # fold angle when going from the left
    #print(f"FA: {F_a:.2f}°")

    # Calculate the DISTANCE between 2 points
    dist = distance(point1, point2)
    #print(f"L: {dist:.2f}")

    # Calculate each individual covered distance
    indiv_covered_distance = covered_distance(angle)
    Covered_distance.append(indiv_covered_distance)

    if i == 0:
        #first fold
        total_length = dist + indiv_covered_distance
        Norm_length_total.append(total_length)
    elif i!=0 and i % 2 == 0:
        #even numbers
        covered += indiv_covered_distance
        total_length += dist + covered
        Norm_length_total.append(total_length)
        covered = 0
    else:
        #odd numbers
        covered = indiv_covered_distance
        total_length += dist
        Norm_length_total.append(total_length)

# Print the total length of the shape
print(f"Total length: {total_length:.2f} units")
Norm_length_total = Norm_length_total/total_length*Length

# Calculating folding coordinates
for i in range (len(points)):
    # Calculate coordinates for folding on top & bottom
    fold_coord = W/math.tan(math.radians(Fold_angle[i]))
    if i % 2 == 0:
        Norm_length_fold.append(Norm_length_total[i] - fold_coord)
    else:
        Norm_length_fold.append(Norm_length_total[i] + fold_coord)

print("Shape_angle: ")
formatted_list = ["{:.3f}".format(num) for num in Shape_angle]
print(formatted_list)

print("Fold_angle_norm: ")
formatted_list = ["{:.3f}".format(num) for num in Fold_angle_norm]
print(formatted_list)

print("Norm_length_total: ")
formatted_list = ["{:.3f}".format(num) for num in Norm_length_total]
print(formatted_list)

print("Covered_distnace: ")
formatted_list = ["{:.3f}".format(num) for num in Covered_distance]
print(formatted_list)

print("Norm_length_fold: ")
formatted_list = ["{:.3f}".format(num) for num in Norm_length_fold]
print(formatted_list)




plt.figure(2)
ax = plt.gca()
ax.axis('off')
ax.set_frame_on(False)

for i in range (len(points)):
    # ax.plot(Norm_length_total[i], 0, 'bo')
    # ax.plot(Norm_length_fold[i], W, 'bo')
    # ax.plot(Norm_length_fold[i], -W, 'bo')
    ax.plot([Norm_length_total[i], Norm_length_fold[i]], [0, W], 'r-')
    ax.plot([Norm_length_total[i], Norm_length_fold[i]], [0, -W], 'r-')

ax.plot([0,Length],[0,0],'r-')
ax.plot([0,Length],[W,W],'k-')
ax.plot([0,Length],[-W,-W],'k-')
ax.plot([0,0],[-W,W],'k-')
ax.plot([Length,Length],[-W,W],'k-')

plt.axis('equal')
plt.show()