import numpy as np
import matplotlib.pyplot as plt
import math

# CONSTANTS
IA = 80 # Actuation input angle
W = 1 # Width
Length = 40

# Function to calculate the DISTANCE between two points
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to calculate the CLOCKWISE ANGLE between three points
def calculate_clockwise_angle(point1, point2, point3):
    # Convert points to vectors
    vector1 = np.array(point2) - np.array(point1)
    vector2 = np.array(point3) - np.array(point2)
    # print(vector1)
    # print(vector2)

    # Calculate dot product and magnitudes
    dot_product = np.dot(vector1, vector2)
    # print(dot_product)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    # print(magnitude1)
    # print(magnitude2)

    # Calculate cosine of the angle
    cos_angle = dot_product / (magnitude1 * magnitude2)

    # Calculate angle in radians
    angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))

    # Convert angle to degrees
    angle_deg = np.degrees(angle_rad)
    # print(angle_deg)

    # Check the orientation (clockwise or counterclockwise)
    cross_product = np.cross(vector1, vector2)
    if cross_product > 0:
        angle_deg = 360 - angle_deg

    # print(angle_deg)
    # print(cross_product)
    return angle_deg

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
    interm = math.cos(math.radians(angle))
    interm = interm/(1-(math.cos(math.radians(IA)))**2 * (math.sin(math.radians(angle))**2))**0.5
    gamma = math.degrees(2 * math.acos(interm))
    # print(180-gamma)
    C = W * math.sin(math.radians(IA)) / math.sin(math.radians(180-gamma))
    return C

# Input array of points (2D coordinates)
# TO BE CHANGED FOR EACH SHAPE
"""
CHANGE THE BELOW POINTS FOR THE SHAPE TO CUT
MAKE SURE THERE ARE ODD NUMBERS OF POINTS
IF THERE ARE EVEN NUMBERS, ADD THE FIRST POINT AGAIN TO THE END
"""
#Original house shape:
#points = [(0, 0), (3, 0), (3, 2), (2, 3), (1, 3), (0, 2), (0, 0)]

#Modified house shape:
#points = [(0, 1), (3, 1), (3, 2), (2, 3), (1, 3), (0, 2), (0, 1)]

#Test Gripper Shape:
#points = [(3,0),(5,0),(8,1),(5,3),(3,3),(0,1),(3,0)]

#Pentagon
'''
points = [ 
          (10*math.cos(math.radians(18)),10*math.sin(math.radians(18))), 
          (10*math.cos(math.radians(-54)),10*math.sin(math.radians(-54))), 
          (-10*math.cos(math.radians(-54)),10*math.sin(math.radians(-54))),
          (-10*math.cos(math.radians(18)),10*math.sin(math.radians(18))),
          (0,10)
        ]
'''
#VT shape:
points = [
    (12,6),
    (9,0),
    (7,0),
    (10,6),
    (7,6),
    (4,0),
    (0,8),
    (2,8),
    (4,4),
    (6,8),
    (16,8),
    (15,6),
    (12,6)
]
#'''

# Plot the input points
plt.figure(1)
ax = plt.gca()
ax.grid()
ax.axis('equal')

for point in points:
    ax.plot(point[0], point[1], 'o')

# Initializing all variables
total_length = 0
Output_angle = []
Fold_angle = []
Norm_length_total = []
Norm_length_fold = []
Fold_coord = []

total_length_covered = 0
Covered_distance = []

# MAIN LOOP
for i in range(len(points)):
    # Draw lines connecting all the points together
    point1 = points[i]
    point2 = points[(i + 1) % len(points)]  # Circular loop
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], 'r-')
    
    # Calculate and collate distance between 2 points
    dist = distance(point1, point2)
    total_length += dist
    Norm_length_total.append(total_length)
    # print(f"L: {dist:.2f}")

    # Calculate and collate inner angle (in degrees)
    point3 = points[(i + 2) % len(points)]  # Next point
    angle = (calculate_clockwise_angle(point1, point2, point3))
    Output_angle.append(angle)
    # print(f"A: {angle:.2f}°")

    # Back-calculate and collate the fold angle (in degrees)
    if i % 2 == 0:
        fold_angle_original = shape_to_fold(angle)
    else:
        fold_angle_original = shape_to_fold(-1*angle)

    Fold_angle.append(fold_angle_original)
    # print(f"FA: {fold_angle_original:.2f}°")

    # Calculate each individual covered distance
    indiv_covered_distance = covered_distance(fold_angle_original)
    if not math.isnan(indiv_covered_distance):
        indiv_covered_distance = indiv_covered_distance
    else:
        indiv_covered_distance = 0
    total_length_covered += indiv_covered_distance
    Covered_distance.append(indiv_covered_distance)

left_or_right = []
left = 0  # <
right = 1 # >

# Calculating < or > folds
for i in range (len(points)):
    if i % 2 == 0:
        if Output_angle[i] > 180:
            left_or_right.append(left)
            #print("<")
        else:
            left_or_right.append(right)
            #print(">")
    else:
        if Output_angle[i] > 180:
            left_or_right.append(right)
            #print(">")
        else:
            left_or_right.append(left)
            #print("<")


temp = 0
# Adding covered distances accordingly
for i in range (len(points)):
    if i == 0:
        temp += Covered_distance[i]
        print("First")

    elif left_or_right[i-1] == 1 and left_or_right[i] == 0:                         # > <
        temp += 0                                                                   # Don't add
        print("> <")
    
    elif left_or_right[i-1] == 0 and left_or_right[i] == 0:                         # < <
        temp += Covered_distance[i-1]                                               # Add previous
        print("< <")
    
    elif left_or_right[i-1] == 1 and left_or_right[i] == 1:                         # > >
        temp += Covered_distance[i]                                                 # Add next
        print("> >")
    
    elif left_or_right[i-1] == 0 and left_or_right[i] == 1:                         # < >
        temp += Covered_distance[i-1] + Covered_distance[i]                         # Add both
        print("< >")
    
    Norm_length_total[i] += temp

# Normalizes the lengths
total_length += total_length_covered
Norm_length_total = Norm_length_total/total_length*Length

# Calculating folding coordinates
for i in range (len(points)):
    # Calculate coordinates for folding on top & bottom
    fold_coord = W/math.tan(math.radians(Fold_angle[i]))
    if i % 2 == 0:
        if Output_angle[i] > 180:
            Norm_length_fold.append(Norm_length_total[i] + fold_coord)
        else:
            Norm_length_fold.append(Norm_length_total[i] - fold_coord)
    else:
        if Output_angle[i] > 180:
            Norm_length_fold.append(Norm_length_total[i] - fold_coord)
        else:
            Norm_length_fold.append(Norm_length_total[i] + fold_coord)


# OUTPUT

print("Clockwise_output_angle: ")
formatted_list = ["{:.3f}".format(num) for num in Output_angle]
print(formatted_list)

print("Fold_angle: ")
formatted_list = ["{:.3f}".format(num) for num in Fold_angle]
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


# Plots the desired Miura-Ori fold pattern
plt.figure("L/W/IA-" + str(Length) + "/" + str(W) + "/" + str(IA))
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