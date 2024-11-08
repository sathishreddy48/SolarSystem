import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from mpl_toolkits.mplot3d import Axes3D
from geopy.geocoders import Nominatim

# Function to simulate the Moon's position in 3D Cartesian coordinates
def moon_position(day_of_year, hour):
    t = 2 * np.pi * (day_of_year + hour / 24) / 27.3  # Adjusted for hour in the Moon's cycle
    x = np.cos(t) * 0.5  # Moon orbits further from Earth in the plot
    y = np.sin(t) * 0.5
    z = np.sin(t) * 0.1  # A slight z-component for 3D effect
    return x, y, z

# Set your location to "home" (latitude, longitude)
lat = 17.612778
lon = 80.042167

# Setup a 3D plot
fig = plt.figure(figsize=(50, 50))  # Adjusted figure size for better visual clarity
ax = fig.add_subplot(111, projection='3d')

# Set axis limits
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-0.5, 0.5)
ax.set_xlabel("East-West (x-axis)")
ax.set_ylabel("North-South (y-axis)")
ax.set_zlabel("Up-Down (z-axis)")
ax.set_title(f"Full Moon Paths in 3D (Location: Home - {lat}, {lon})")

# Calculate the first full moon day
first_full_moon_day = 15  # Approximate first full moon of the year (can be adjusted)
full_moon_interval = 29.5  # Days between full moons

# Date for November 15th, 2024 (Kartheeka Pournami)
kartheeka_date = datetime(2024, 11, 15)
start_date = datetime(2024, 1, 1)
kartheeka_day_of_year = (kartheeka_date - start_date).days + 1  # Day of year for November 15th, 2024

# Plot the paths of the Moon on full moon days
for i in range(12):  # Assuming 12 full moons in a year (one every 29.5 days)
    full_moon_day = int(first_full_moon_day + i * full_moon_interval)  # Calculate the full moon day
    moon_path_x = []
    moon_path_y = []
    moon_path_z = []

    # Loop through the 24 hours of the full moon day (00:00 to 23:00)
    for hour in range(24):
        moon_x, moon_y, moon_z = moon_position(full_moon_day, hour)
        moon_path_x.append(moon_x)
        moon_path_y.append(moon_y)
        moon_path_z.append(moon_z)

    # If this is the full moon on November 15th (Kartheeka Pournami), use a special color (red)
    if full_moon_day == kartheeka_day_of_year:
        ax.plot(moon_path_x, moon_path_y, moon_path_z, color='red', lw=3, label=f"Kartheeka Pournami (Nov 15, 2024)")
        ax.text(moon_path_x[12] + 0.05, moon_path_y[12] + 0.05, moon_path_z[12], "Kartheeka Pournami", color="red", fontsize=12, ha='center')
    else:
        ax.plot(moon_path_x, moon_path_y, moon_path_z, color=(0.1, 0.1, 0.1), lw=3, label=f"Full Moon {full_moon_day}")
        ax.text(moon_path_x[12] + 0.05, moon_path_y[12] + 0.05, moon_path_z[12], str(full_moon_day), color="black", fontsize=8, ha='center')

# Plot the Earth at the origin (0, 0, 0)
ax.scatter(0, 0, 0, color='green', s=100, label="Earth (Origin)")

# Add a legend
ax.legend()

# Save the plot with the Full Moon paths
plt.savefig("full_moon_paths_kartheeka_pournami_3d.png", format="png", dpi=300)  # Save with HD resolution

# Display the plot
plt.show()
