import numpy as np
import matplotlib.pyplot as plt

# Convert azimuth and altitude to radians
def degrees_to_radians(degrees):
    return np.radians(degrees)

# Function to calculate the Cartesian coordinates based on Azimuth and Altitude
def calculate_position(azimuth, altitude):
    # Convert azimuth and altitude to radians
    azimuth_rad = degrees_to_radians(azimuth)
    altitude_rad = degrees_to_radians(altitude)
    
    # Calculate Cartesian coordinates
    x = np.cos(altitude_rad) * np.sin(azimuth_rad)  # East-West (x-axis)
    y = np.cos(altitude_rad) * np.cos(azimuth_rad)  # North-South (y-axis)
    
    return x, y

# Given Azimuth and Altitude for Sun and Moon
sun_azimuth = 179.49  # Azimuth in degrees
sun_altitude = 22.35  # Altitude in degrees

moon_azimuth = 89.33  # Azimuth in degrees
moon_altitude = 45.00  # Altitude in degrees

# Calculate positions of Sun and Moon
sun_x, sun_y = calculate_position(sun_azimuth, sun_altitude)
moon_x, moon_y = calculate_position(moon_azimuth, moon_altitude)

# Create a 2D plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.5, 1.5)  # Set x-axis limits
ax.set_ylim(-1.5, 1.5)  # Set y-axis limits
ax.set_aspect('equal', 'box')  # Equal scaling for x and y axes

# Labels and title
ax.set_xlabel("East-West (x-axis)")
ax.set_ylabel("North-South (y-axis)")
ax.set_title(f"Sun and Moon's Position (Azimuth & Altitude)")

# Plot the Earth at the origin (0, 0)
ax.plot(0, 0, 'go', label="Earth (Origin)", markersize=10)

# Draw cardinal direction lines (N, E, S, W)
ax.plot([0, 1.5], [0, 0], 'k-', label="East (E)")  # East (positive x)
ax.plot([0, -1.5], [0, 0], 'k-', label="West (W)")  # West (negative x)
ax.plot([0, 0], [0, 1.5], 'k-', label="North (N)")  # North (positive y)
ax.plot([0, 0], [0, -1.5], 'k-', label="South (S)")  # South (negative y)

# Draw Sun's position line (from Earth to Sun)
ax.plot([0, sun_x], [0, sun_y], 'r-', label=f"Sun's Position: Azimuth {sun_azimuth}°, Altitude {sun_altitude}°")

# Draw Moon's position line (from Earth to Moon)
ax.plot([0, moon_x], [0, moon_y], 'b-', label=f"Moon's Position: Azimuth {moon_azimuth}°, Altitude {moon_altitude}°")

# Plot the Sun's position
ax.plot(sun_x, sun_y, 'ro', label=f"Sun at Azimuth {sun_azimuth}°")

# Plot the Moon's position
ax.plot(moon_x, moon_y, 'bo', label=f"Moon at Azimuth {moon_azimuth}°")

# Display azimuth angle labels
ax.text(sun_x + 0.05, sun_y + 0.05, f'{sun_azimuth}°', color='red', fontsize=12)
ax.text(moon_x + 0.05, moon_y + 0.05, f'{moon_azimuth}°', color='blue', fontsize=12)

# Add a legend
ax.legend()

# Display the plot
plt.show()
