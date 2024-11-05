import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from geopy.geocoders import Nominatim

# Function to simulate Sun's position in Cartesian coordinates
def sun_position(hour, latitude):
    t = (hour / 24 * 2 * np.pi)  # Normalize hour to radians for smooth movement

    # Sun's path: cosine for east-west (x), sine for north-south (y)
    # Latitude affects how high the Sun is at noon (zenith angle)
    zenith_angle = np.radians(90 - latitude)  # Adjust Sun's altitude based on latitude

    # Calculate the Sun's position based on the zenith angle
    x = np.cos(t)  # East-West movement
    y = np.sin(t) * np.cos(zenith_angle)  # Adjust for latitude

    return x, y

# Function to simulate Moon's position in Cartesian coordinates (simplified)
def moon_position(hour):
    t = (hour / 24 * 2 * np.pi)  # Normalize hour to radians for the Moon's movement

    # Moon's path: slower eastward movement
    x = np.cos(t * 0.5)  # Moon moves eastward slower
    y = np.sin(t * 0.5)  # Moon moves slightly up/down

    return x, y

# Get the current time and extract the hour of the day
current_time = datetime.now()
current_hour = current_time.hour + current_time.minute / 60  # Get the current hour as a float

# Function to get latitude and longitude based on country or coordinates
def get_coordinates(location):
    geolocator = Nominatim(user_agent="sun_moon_simulator")

    try:
        # Try to geocode based on country name
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            raise ValueError("Location not found.")
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Function to adjust the time based on longitude
def adjust_time_for_location(longitude):
    # Longitude influences the time zone; every 15° corresponds to one hour
    utc_offset = longitude / 15  # Time zone offset based on longitude
    local_time = current_hour + utc_offset  # Adjust current hour to local time
    # Normalize the time to 24-hour format (wrap around if needed)
    return local_time % 24

# Input location (can be country or specific coordinates)
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

# Adjust the current time based on the longitude
local_hour = adjust_time_for_location(lon)

# Setup a 2D grid plot with the Earth at origin (0,0)
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.5, 1.5)  # x-axis range (East-West)
ax.set_ylim(-1.5, 1.5)  # y-axis range (North-South)
ax.set_aspect('equal', 'box')  # Equal scaling for x and y axes

# Labels and titles
ax.set_xlabel("East-West (x-axis)")
ax.set_ylabel("North-South (y-axis)")
ax.set_title(f"Sun and Moon Positions (Location: {location_input}, Local Time: {local_hour:.2f}h)")

# Plot the Earth at the origin (0, 0)
ax.plot(0, 0, 'go', label="Earth (Origin)", markersize=10)

# Plot the cardinal directions as lines
ax.plot([0, 1.5], [0, 0], 'k-', label="East (E)")  # E (positive x direction)
ax.plot([0, -1.5], [0, 0], 'k-', label="West (W)")  # W (negative x direction)
ax.plot([0, 0], [0, 1.5], 'k-', label="North (N)")  # N (positive y direction)
ax.plot([0, 0], [0, -1.5], 'k-', label="South (S)")  # S (negative y direction)

# Diagonal Directions: SE (Southeast, 120-130°)
ax.plot([0, 1], [0, -1], 'k--', label="Southeast (SE)")

# Get Sun and Moon positions at the current local time
sun_x, sun_y = sun_position(local_hour, lat)  # Get Sun's position based on location's latitude and time
moon_x, moon_y = moon_position(local_hour)  # Get Moon's position for the current hour

# Plot Sun's position (using local time)
ax.plot(sun_x, sun_y, 'ro', label=f"Sun at {local_hour:.2f}h")

# Plot Moon's position (using local time)
ax.plot(moon_x, moon_y, 'bo', label=f"Moon at {local_hour:.2f}h")

# Add a legend
ax.legend()

# Display the plot
plt.show()
