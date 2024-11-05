import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta  # Add timedelta import
from geopy.geocoders import Nominatim
import pytz

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

# Function to get latitude and longitude based on country or coordinates
def get_coordinates(location):
    geolocator = Nominatim(user_agent="sun_moon_simulator")
    try:
        # Try to geocode based on country name or coordinates (latitude,longitude)
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            raise ValueError("Location not found.")
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Function to adjust the time based on longitude (Longitude affects the time zone)
def adjust_time_for_location(longitude):
    # Longitude influences the time zone; every 15° corresponds to one hour
    utc_offset = longitude / 15  # Time zone offset based on longitude
    current_time = datetime.utcnow()  # Get current UTC time
    local_time = current_time + timedelta(hours=utc_offset)  # Adjust current time to local time
    return local_time

# Get the current time and extract the hour of the day
def get_local_time(location):
    latitude, longitude = get_coordinates(location)
    if latitude is None or longitude is None:
        return None
    local_time = adjust_time_for_location(longitude)
    return local_time.hour + local_time.minute / 60  # Convert time to decimal hours

# Given Azimuth and Altitude for Sun and Moon
def get_sun_and_moon_positions(hour, latitude):
    # Sun's position (simplified model for illustration)
    sun_t = (hour / 24) * 2 * np.pi  # Normalize hour to radians for smooth movement
    sun_azimuth = (sun_t + np.pi) % (2 * np.pi)  # Azimuth calculation (relative to local time)
    sun_altitude = 90 - latitude  # Altitude based on latitude (simplified)
    
    # Moon's position (simplified model for illustration)
    moon_t = (hour / 24) * np.pi  # Moon moves more slowly than the Sun
    moon_azimuth = (moon_t + np.pi) % (2 * np.pi)  # Azimuth calculation
    moon_altitude = 90 - latitude + 10 * np.sin(moon_t)  # Some variation in altitude
    
    return np.degrees(sun_azimuth), 90 - np.degrees(sun_altitude), np.degrees(moon_azimuth), 90 - np.degrees(moon_altitude)

# Input location (can be country or specific coordinates)
location_input = input("Enter location (country or latitude,longitude): ")

# Get the local time (in decimal hours)
local_hour = get_local_time(location_input)

# If location not found, exit
if local_hour is None:
    print("Invalid location, unable to get local time.")
    exit()

# Get the latitude from the location input
latitude, longitude = get_coordinates(location_input)

# Get Sun and Moon azimuth and altitude at the current local time
sun_azimuth, sun_altitude, moon_azimuth, moon_altitude = get_sun_and_moon_positions(local_hour, latitude)

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
ax.set_title(f"Sun and Moon's Position (Location: {location_input}, Time: {local_hour:.2f}h)")

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
ax.text(sun_x + 0.05, sun_y + 0.05, f'{sun_azimuth:.2f}°', color='red', fontsize=12)
ax.text(moon_x + 0.05, moon_y + 0.05, f'{moon_azimuth:.2f}°', color='blue', fontsize=12)

# Add a legend
ax.legend()

# Display the plot
plt.show()
