import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

# Function to simulate Sun's position in Cartesian coordinates with daily declination adjustment
def sun_position(day_of_year, latitude):
    # Calculate declination angle of the Sun (approximate)
    declination = 23.44 * np.cos((2 * np.pi / 365) * (day_of_year - 173))
    zenith_angle = np.radians(90 - (latitude + declination))  # Adjust Sun's altitude

    # Calculate the Sun's position based on the zenith angle for noon (peak altitude)
    x = np.cos(zenith_angle)
    y = np.sin(zenith_angle)

    return x, y

# Simplified function for Moon's position
def moon_position(day_of_year, hour):
    t = 2 * np.pi * (day_of_year + hour / 24) / 27.3  # Adjusted for hour in the Moon's cycle (27.3-day cycle)

    # Circular path around Earth (illustrative)
    x = np.cos(t) * 0.5  # Moon orbits further from Earth in the plot
    y = np.sin(t) * 0.5

    return x, y

# Geolocation function remains the same
def get_coordinates(location):
    geolocator = Nominatim(user_agent="sun_moon_simulator")

    try:
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            raise ValueError("Location not found.")
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Input location
location_input = input("Enter location (country or latitude,longitude): ")

# Determine if the input is a pair of coordinates or a country name
if ',' in location_input:
    try:
        lat, lon = map(float, location_input.split(','))
    except ValueError:
        print("Invalid coordinates format. Please enter in 'latitude,longitude' format.")
        exit(1)
else:
    lat, lon = get_coordinates(location_input)
    if lat is None or lon is None:
        print("Could not find the location. Please enter a valid location.")
        exit(1)

# Setup a 2D grid plot
fig, ax = plt.subplots(figsize=(100, 100))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal', 'box')
ax.set_xlabel("East-West (x-axis)")
ax.set_ylabel("North-South (y-axis)")
ax.set_title(f"Sun and Moon Annual Paths (Location: {location_input})")

# Initialize arrays to store paths
sun_path_x = []
sun_path_y = []
moon_path_x = []
moon_path_y = []

# Loop through each day of the year
for day in range(1, 366):  # 1 to 365 for a year
    # Get positions at noon for each day
    sun_x, sun_y = sun_position(day, lat)
    moon_x, moon_y = moon_position(day, 12)  # Get Moon's position at noon

    # Store the positions
    sun_path_x.append(sun_x)
    sun_path_y.append(sun_y)
    moon_path_x.append(moon_x)
    moon_path_y.append(moon_y)

    # Draw lines between Sun and Moon for each day (or every 15 days)
    if day % 15 == 0:  # Optional: Change this condition to adjust how frequently you draw lines
        color = plt.cm.viridis(day / 365)  # Change color dynamically based on the day of the year
        ax.plot([sun_x, moon_x], [sun_y, moon_y], color=color, lw=1)  # Line between Sun and Moon

    # Optional: Add day labels for every 30 days
    if day % 15 == 0:
        ax.text(sun_x + 0.03, sun_y + 0.05, str(day), color="red", fontsize=8, ha='center')
        ax.text(moon_x , moon_y + 0.05, str(day), color="blue", fontsize=8, ha='center')

# Plot the paths
ax.plot(sun_path_x, sun_path_y, 'r-', label="Sun's Path (Annual)")
ax.plot(moon_path_x, moon_path_y, 'b-', label="Moon's Path (Annual)")

# Plot the Earth at the origin
ax.plot(0, 0, 'go', label="Earth (Origin)", markersize=10)

# Add cardinal directions
ax.plot([0, 1.5], [0, 0], 'k-', label="East (E)")
ax.plot([0, -1.5], [0, 0], 'k-', label="West (W)")
ax.plot([0, 0], [0, 1.5], 'k-', label="North (N)")
ax.plot([0, 0], [0, -1.5], 'k-', label="South (S)")

# Add a legend
ax.legend()

# Calculate the day of the year for 15th November 2024
date = datetime(2024, 11, 15)
start_date = datetime(2024, 1, 1)
day_of_year = (date - start_date).days + 1

# Initialize arrays to store the Moon's path on 15th November
moon_path_15nov_x = []
moon_path_15nov_y = []

# Loop through the 24 hours of 15th November 2024 (00:00 to 23:00)
for hour in range(24):
    moon_x, moon_y = moon_position(day_of_year, hour)  # Corrected to pass both arguments
    moon_path_15nov_x.append(moon_x)
    moon_path_15nov_y.append(moon_y)

# Plot the Moon's path on 15th November with a dark line
ax.plot(moon_path_15nov_x, moon_path_15nov_y, 'k-', lw=2, label="Moon's Path on 15th Nov 2024")

# Add the label for Kartheeka Pournami
# Assuming Kartheeka Pournami occurs at midnight UTC (0:00 on 15th November)
kartheeka_x = moon_path_15nov_x[0]  # Position at midnight
kartheeka_y = moon_path_15nov_y[0]
ax.text(kartheeka_x + 0.05, kartheeka_y + 0.05, "Kartheeka Pournami", color="orange", fontsize=12, ha='center')

# Save the plot with the Moon's path and Kartheeka Pournami tag
plt.savefig("sun_moon_annual_paths_with_kartheeka_pournami.png", format="png", dpi=300)  # Save with HD resolution

# Display the plot
plt.show()
