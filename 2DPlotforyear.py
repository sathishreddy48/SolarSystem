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
def moon_position(day_of_year):
    t = 2 * np.pi * day_of_year / 27.3  # 27.3-day cycle for Moon's movement

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
    moon_x, moon_y = moon_position(day)
    
    # Store the positions
    sun_path_x.append(sun_x)
    sun_path_y.append(sun_y)
    moon_path_x.append(moon_x)
    moon_path_y.append(moon_y)

    # Add day labels for every 30 days (or adjust as needed)
    if day % 1 == 10:
        ax.text(sun_x, sun_y, str(day), color="red", fontsize=8, ha='center')
        ax.text(moon_x, moon_y, str(day), color="blue", fontsize=8, ha='center')

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

plt.savefig("sun_moon_annual_paths_hd.png", format="png", dpi=300)  # Save with HD resolution

# Display the plot
plt.show()
