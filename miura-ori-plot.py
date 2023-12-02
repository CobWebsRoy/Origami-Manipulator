import numpy as np
import matplotlib.pyplot as plt
import math

# Initialize empty lists to collect values
IA_values = []
OA_values = []

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Loop through different values of FA (degrees)
for FA in range(0, 86, 15):
    IA_values = []
    OA_values = []

    # Loop through different values of IA (degrees)
    for IA in range(-91, 91):
        if IA>0:
            k=1
        elif IA<0:
            k=-1
        interm = 1 - ((math.sin(math.radians(FA))**2) * (math.cos(math.radians(IA))**2))
        OA = 2 * k * math.acos(min(1, (math.cos(math.radians(FA)))/(interm**0.5)))

        IA_values.append(IA)
        OA_values.append(math.degrees(OA))

    # Plot the data for this FA value
    ax.plot(IA_values, OA_values, label=f'FA = {FA}°')

# Add labels and a title
ax.set_xlabel('Input Angle (degrees)')
ax.set_ylabel('Output Angle (degrees)')

# Set the legend to distinguish between different FA values
ax.legend()

# Set the plot limits
ax.set_xlim(-90, 90)
ax.set_ylim(-180, 180)

# Display the plot
plt.show()