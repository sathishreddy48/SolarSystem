import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Function to simulate Sun's position in Cartesian coordinates
def sun_position(hour):
    t = hour / 24 * 2 * np.pi  # Normalize hour to radians for smooth movement
    
    # Sun's path: cosine for east-west (x), sine for north-south (y)
    x = np.cos(t)  # East-West movement
    y = np.sin(t)  # North-South movement
    
    return x, y

# Function to simulate Moon's position in Cartesian coordinates (simplified)
def moon_position(hour):
    t = hour / 24 * 2 * np.pi  # Normalize hour to radians for the Moon's movement
    
    # Moon's path: slower eastward movement
    x = np.cos(t * 0.5)  # Moon moves eastward slower
    y = np.sin(t * 0.5)  # Moon moves slightly up/down
    
    return x, y

# Get the current time and extract the hour of the day
current_time = datetime.now()
current_hour = current_time.hour + current_time.minute / 60  # Get the current hour as a float

# Setup a 2D grid plot with the Earth at origin (0,0)
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.5, 1.5)  # x-axis range (East-West)
ax.set_ylim(-1.5, 1.5)  # y-axis range (North-South)
ax.set_aspect('equal', 'box')  # Equal scaling for x and y axes

# Labels and titles
ax.set_xlabel("East-West (x-axis)")
ax.set_ylabel("North-South (y-axis)")
ax.set_title("Sun and Moon Positions in the Sky (Current Time)")

# Plot the Earth at the origin (0, 0)
ax.plot(0, 0, 'go', label="Earth (Origin)", markersize=10)

# Plot the cardinal directions as lines
ax.plot([0, 1.5], [0, 0], 'k-', label="East (E)")  # E (positive x direction)
ax.plot([0, -1.5], [0, 0], 'k-', label="West (W)")  # W (negative x direction)
ax.plot([0, 0], [0, 1.5], 'k-', label="North (N)")  # N (positive y direction)
ax.plot([0, 0], [0, -1.5], 'k-', label="South (S)")  # S (negative y direction)

# Diagonal Directions: SE (Southeast, 120-130°)
ax.plot([0, 1], [0, -1], 'k--', label="Southeast (SE)")

# Get Sun and Moon positions at the current time
sun_x, sun_y = sun_position(current_hour)  # Get Sun's position for the current hour
moon_x, moon_y = moon_position(current_hour)  # Get Moon's position for the current hour

# Plot Sun's path (using current hour)
ax.plot(sun_x, sun_y, 'ro', label=f"Sun at {current_hour:.2f}h")

# Plot Moon's path (using current hour)
ax.plot(moon_x, moon_y, 'bo', label=f"Moon at {current_hour:.2f}h")

# Add a legend
ax.legend()

# Display the plot
plt.show()
