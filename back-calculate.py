import numpy as np
import matplotlib.pyplot as plt
import math

# Initialize empty lists to collect values
OA_values = [] 
FA_values = []

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Loop through different values of FA (degrees)
for IA in range(10, 91, 15):
    OA_values = []
    FA_values = []

    # Loop through different values of IA (degrees)
    for OA in range(-180, 180):
        interm = (math.cos(math.radians(IA))**2) * (math.cos(math.radians(OA/2))**2) - 1
        interm = (math.cos(math.radians(OA/2))**2 - 1) / interm
        interm = interm ** 0.5

        if OA<0:
            FA = -math.asin(interm)
        else:
            FA = math.asin(interm)

        OA_values.append(OA)
        FA_values.append(math.degrees(FA))

    # Plot the data for this FA value
    ax.plot(OA_values, FA_values, label=f'Input Angle = {IA}°')

# Add labels and a title
ax.set_xlabel('Output Angle (degrees)')
ax.set_ylabel('Fold Angle (degrees)')

# Set the legend to distinguish between different IA values
ax.legend()

# Set the plot limits
ax.set_xlim(-180, 180) # output angles
ax.set_ylim(-90, 90)

# Display the plot
plt.show()